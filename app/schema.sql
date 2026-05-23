DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS cart;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_products;
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    flag_admin INTEGER(1) NOT NULL DEFAULT(0),
    flag_confirmed INTEGER(1) NOT NULL DEFAULT(0),
    created_at REAL NOT NULL DEFAULT 0
);

CREATE TABLE cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (user_id) REFERENCES user (id)
);
CREATE TABLE product(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    discount integer,
    category TEXT NOT NULL,
    image TEXT
);
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone_number TEXT,
    user_id INTEGER NOT NULL,
    email TEXT NOT NULL,
    address_delivery TEXT,
    pay_method INTEGER(1) NOT NULL DEFAULT(0),
    comment TEXT,
    FOREIGN KEY (user_id) REFERENCES user (id)
);
CREATE TABLE order_products(
    order_id INTEGER NOT NULL,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price INTEGER NOT NULL,
    PRIMARY KEY(order_id,product),
    FOREIGN KEY (order_id) REFERENCES orders (id)
);
insert into product(title, description, price, discount,category,image)
values ('Мандарины','Мандарины свежие 1 кг',60,0,'Фрукты','/static/images/oranges.jpg'),
 ('Ботинки','Ботинки крутые зимние',4000,15,'Обувь','/static/images/boots.jpg')