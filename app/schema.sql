DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS cart;
DROP TABLE IF EXISTS product;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    flag_admin INTEGER NOT NULL
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

insert into product(title, description, price, discount,category)
values ('Мандарины','Мандарны свежие 1 кг',60,0,'Фрукты')