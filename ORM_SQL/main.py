import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json

from models import create_tables, drop_tables, Publishers, Books, Shops, Stocks, Sales

DBMS = "postgresql"
LOGIN = "postgres"
PASSWORD = "admin"
HOST = "localhost"
PORT = "5432"
DATABASE = "netology_db"


def add_data(session):
    with open("tests_data.json", "r") as data:
        test_data = json.load(data)
    for data in test_data:
        if data.get("model") == "publisher":
            session.add(
                Publishers(
                    publisher_id=data.get("pk"),
                    publisher_name=data.get("fields").get("name"),
                )
            )
        elif data.get("model") == "book":
            session.add(
                Books(
                    book_id=data.get("pk"),
                    book_title=data.get("fields").get("title"),
                    publisher_id=data.get("fields").get("id_publisher"),
                )
            )
        elif data.get("model") == "shop":
            session.add(
                Shops(shop_id=data.get("pk"), shop_name=data.get("fields").get("name"))
            )
        elif data.get("model") == "stock":
            session.add(
                Stocks(
                    stock_id=data.get("pk"),
                    shop_id=data.get("fields").get("id_shop"),
                    book_id=data.get("fields").get("id_book"),
                    count=data.get("fields").get("count"),
                )
            )
        elif data.get("model") == "sale":
            session.add(
                Sales(
                    sale_id=data.get("pk"),
                    price=data.get("fields").get("price"),
                    date_sale=data.get("fields").get("date_sale"),
                    count=data.get("fields").get("count"),
                    stock_id=data.get("fields").get("id_stock"),
                )
            )
        session.commit()


def get_sales(session, publisher_to_find):
    selected = (
        session.query(
            Books.book_title,
            Shops.shop_name,
            Sales.price * Sales.count,
            Sales.date_sale,
        )
        .join(Publishers)
        .join(Stocks)
        .join(Shops)
        .join(Sales)
        .filter(Publishers.publisher_name.like(f"{publisher_to_find}"))
    )
    result = ""
    for s in selected.all():
        result += "{:<40} | {:<10} | {:<6} | {}\n".format(
            s[0], s[1], s[2], s[3].strftime("%d.%m.%y")
        )
    result = result.strip()
    if not result:
        result = f"Издатель с именем {publisher_to_find} не найден!"
    return result


if __name__ == "__main__":

    DNS = f"{DBMS}://{LOGIN}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    engine = sqlalchemy.create_engine(DNS)

    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # add_data(session)
    publisher_to_find = input("Введите наименование издателя: ")
    print(get_sales(session, publisher_to_find))

    session.close()
