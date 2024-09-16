CREATE DATABASE arun_icecream_;
CREATE USER 'your_db_'@'localhost' IDENTIFIED BY 'namrata_';
GRANT ALL PRIVILEGES ON arun_icecream.* TO 'your_db_'@'localhost';
FLUSH PRIVILEGES;

use arun_icecream_;
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    phone VARCHAR(20),
    description TEXT,
    items TEXT
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10, 2),
    image_url VARCHAR(255)
);

INSERT INTO products (name, price, image_url) VALUES 
('Trio Ice Cream', 150, 'images/trio.jpg');

INSERT INTO products (name, price, image_url) VALUES 
('Almond Crunch', 150, 'images/Almond Crunch.jpg');

INSERT INTO products (name, price, image_url) VALUES 
('Bazooka', 30, 'images/Bazooka.jpg');

INSERT INTO products (name, price, image_url) VALUES 
('Belgian Chocolate', 90, 'images/Belgian Chocolate.jpg');

select * from products;
drop table products;

