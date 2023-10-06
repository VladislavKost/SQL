import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publishers(Base):
    __tablename__ = "publishers"

    publisher_id = sq.Column(sq.Integer, primary_key=True)
    publisher_name = sq.Column(sq.String(length=40), unique=True)


class Books(Base):
    __tablename__ = "books"

    book_id = sq.Column(sq.Integer, primary_key=True)
    book_title = sq.Column(sq.String(length=40), nullable=False)
    publisher_id = sq.Column(
        sq.Integer, sq.ForeignKey("publishers.publisher_id"), nullable=False
    )

    publisher = relationship(Publishers, backref="books")


class Shops(Base):
    __tablename__ = "shops"

    shop_id = sq.Column(sq.Integer, primary_key=True)
    shop_name = sq.Column(sq.String(length=40), unique=True)


class Stocks(Base):
    __tablename__ = "stocks"

    stock_id = sq.Column(sq.Integer, primary_key=True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey("books.book_id"), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey("shops.shop_id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship(Books, backref="stocks")
    shop = relationship(Shops, backref="stocks")
    __table_args__ = (sq.UniqueConstraint("book_id", "shop_id", name="unique_ids"),)


class Sales(Base):
    __tablename__ = "sales"

    sale_id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey("stocks.stock_id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stocks, backref="sales")


def create_tables(engine):
    Base.metadata.create_all(engine)


def drop_tables(engine):
    Base.metadata.drop_all(engine)
