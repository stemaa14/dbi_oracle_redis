DROP TABLE customer CASCADE CONSTRAINTS;
DROP TABLE orders CASCADE CONSTRAINTS;
DROP TABLE product CASCADE CONSTRAINTS;
DROP TABLE position CASCADE CONSTRAINTS;

CREATE TABLE customer(
    id NUMBER (10, 0) PRIMARY KEY,
    city VARCHAR2(100),
    company VARCHAR2(100),
    dob TIMESTAMP,
    phone VARCHAR2(20),
    ssn VARCHAR2(30),
    state VARCHAR2(60),
    street VARCHAR2(100),
    zip NUMBER(8,0),
    email VARCHAR2(60) NOT NULL,
    firstname VARCHAR2(60) NOT NULL,
    gender VARCHAR2(30),
    lastname VARCHAR2(60) NOT NULL
);

CREATE TABLE orders(
    id NUMBER(10, 0) PRIMARY KEY,
    customerId NUMBER(10, 0) NOT NULL,
    orderDate TIMESTAMP NOT NULL,
    orderStatus NUMBER(2, 0) NOT NULL
);

CREATE TABLE product(
    id NUMBER(10, 0) PRIMARY KEY,
    price NUMBER(7, 2) NOT NULL,
    priceDate TIMESTAMP NOT NULL,
    productName VARCHAR2(200) NOT NULL,
    image VARCHAR2(200),
    color VARCHAR2(30)
);

CREATE TABLE position(
    orderId NUMBER(10, 0) NOT NULL,
    id NUMBER(5, 0) NOT NULL,
    productId NUMBER(10, 0) NOT NULL,
    itemCount NUMBER(8, 0) NOT NULL,
    PRIMARY KEY (orderId, id)
);

ALTER TABLE orders
ADD FOREIGN KEY (customerId) REFERENCES customer(id);

ALTER TABLE position
ADD FOREIGN KEY (orderId) REFERENCES orders(id);

ALTER TABLE position
ADD FOREIGN KEY (productId) REFERENCES product(id);

CREATE TRIGGER positionId
  BEFORE INSERT ON position
  FOR EACH ROW
DECLARE
  lastId NUMBER(5, 0) := 0;
BEGIN
  SELECT MAX(p.id) INTO lastId
    FROM position p INNER JOIN orders o ON p.orderId = o.id
    WHERE o.id = :new.orderId;
  :new.id := lastId + 1;
END;
