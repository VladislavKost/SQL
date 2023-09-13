CREATE TABLE IF NOT EXISTS employees (
	employee_id serial PRIMARY KEY,
	employee_name varchar(50) NOT NULL,
	department varchar(50) NOT NULL,
	manager_id int NULL,
	FOREIGN KEY (manager_id) REFERENCES employees (employee_id));