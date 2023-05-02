CREATE TABLE customer (
    customer_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    loginid VARCHAR(10) UNIQUE,
    passwd VARCHAR(20) UNIQUE,
    contact_num VARCHAR
);

CREATE TABLE aboutorder (
    order_id VARCHAR(20) PRIMARY KEY,
    order_num INTEGER,
    ship_via VARCHAR(20),
    shipper_ID VARCHAR(20),
    order_date DATE,
    shipped_date DATE,
    customer VARCHAR(20) REFERENCES customer(customer_id)
);

CREATE TABLE billinginfo (
    billing_id VARCHAR(40) PRIMARY KEY,
    credit_card_pin INTEGER,
    credit_card_num INTEGER,
    bill_date DATE,
    billing_addr VARCHAR,
    credit_card_expiry DATE,
    customer VARCHAR(20) REFERENCES customer(customer_id),
    aboutorder VARCHAR(20) REFERENCES aboutorder(order_id)
);

CREATE TABLE shipper (
    shipper_id VARCHAR(40) PRIMARY KEY,
    phone VARCHAR(20),
    company_name VARCHAR(20),
    aboutorder VARCHAR(20) REFERENCES aboutorder(order_id)
);

CREATE TABLE category (
    category_id VARCHAR(20) PRIMARY KEY,
    category_name VARCHAR(20),
    description VARCHAR(50)
);

CREATE TABLE product (
    product_id VARCHAR(20) PRIMARY KEY,
    quantity_pu INTEGER,
    product_name VARCHAR(20),
    stock_units INTEGER,
    product_image VARCHAR,
    unit_weight FLOAT,
    discount FLOAT,
    reorder_level INTEGER,
    product_description VARCHAR(30),
    supplier_ID VARCHAR(20),
    category VARCHAR(20) REFERENCES category(category_id)
);

CREATE TABLE cart (
    cart_id VARCHAR(20) PRIMARY KEY,
    nop INTEGER,
    total_price INTEGER,
    customer VARCHAR(20) REFERENCES customer(customer_id)
);

CREATE TABLE orderdetails (
    useless_id INTEGER PRIMARY KEY,
    unit_price FLOAT,
    discount FLOAT,
    order_num INTEGER,
    quantity INTEGER,
    product VARCHAR(20) REFERENCES product(product_id),
    aboutorder VARCHAR(20) REFERENCES aboutorder(order_id)
);

CREATE TABLE trackinginfo (
    tracking_id VARCHAR(20) PRIMARY KEY,
    delivery_date DATE,
    shipped_date DATE,
    product VARCHAR(20) REFERENCES product(product_id),
    aboutorder VARCHAR(20) REFERENCES aboutorder(order_id)
);

CREATE TABLE supplier (
    supplier_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20)
);

CREATE TABLE personal_info (
    dummy_id VARCHAR(20) PRIMARY KEY,
    phone VARCHAR(20),
    address VARCHAR(80),
    city VARCHAR(10),
    country VARCHAR(20),
    postal_code INTEGER,
    email VARCHAR(30) UNIQUE,
    passwd VARCHAR(20),
    login_id VARCHAR(20) UNIQUE,
    customer VARCHAR(20) REFERENCES customer(customer_id)
);

CREATE TABLE admin (
    admin_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    login_ID VARCHAR(20) UNIQUE
);

INSERT INTO category (category_id, category_name, description)
VALUES ('C001', 'Electronics', 'Products related to electronic devices and gadgets');

INSERT INTO product (product_id, quantity_pu, product_name, stock_units, unit_weight, discount, reorder_level, product_description, supplier_ID, category) 
VALUES ('12345', 10, 'Example Product', 100, 0.5, 0.1, 5, 'This is an example product', 'ABC123', 'C001');

CREATE TABLE cart_products (
    cart_id VARCHAR(20) REFERENCES cart(cart_id),
    product_id VARCHAR(20) REFERENCES product(product_id),
    PRIMARY KEY (cart_id, product_id)
);

ALTER TABLE product ADD price numeric;
UPDATE product SET price = 100;


CREATE TABLE orders (
  order_id SERIAL PRIMARY KEY,
  order_date DATE NOT NULL,
  shipped_date DATE,
  shipper_id text REFERENCES shipper(shipper_id),
  customer_id text REFERENCES customer(customer_id)
);

CREATE TABLE order_items (
  order_id INTEGER REFERENCES orders(order_id),
  product_id text REFERENCES product(product_id),
  unit_price FLOAT NOT NULL,
  quantity INTEGER NOT NULL,
  discount FLOAT NOT NULL,
  PRIMARY KEY (order_id, product_id)
);
