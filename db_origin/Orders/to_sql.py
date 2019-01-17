#!/usr/bin/python

customer_insert = "INSERT INTO customer(city, company, dob, phone, ssn, state, street, zip, id, email, firstname, gender, lastname) VALUES ('%s', '%s', TO_TIMESTAMP('%s', 'YYYY-MM-DD\"T\"HH24:MI:SS.FF\"Z\"'), '%s', '%s', '%s', '%s', %s, %s, '%s', '%s', '%s', '%s');\n"
product_insert = "INSERT INTO product(image, id, color, price, priceDate, productName) VALUES ('%s', %s, '%s', %s, TO_TIMESTAMP('%s', 'YYYY-MM-DD\"T\"HH24:MI:SS.FF\"Z\"'), '%s');\n"
order_insert = "INSERT INTO orders(id, customerId, orderDate, orderStatus) VALUES (%s, %s, TO_TIMESTAMP('%s', 'YYYY-MM-DD\"T\"HH24:MI:SS.FF\"Z\"'), %s);\n"
position_insert = "INSERT INTO position(itemCount, orderId, productId) VALUES (%s, %s, %s);\n"


with open('query.sql', 'w') as output:
    with open('create.sql') as create:
        output.writelines(create.readlines())

    def read_csv(file, insert):
        with open(file) as csv_input:
            csv_input.readline()
            for line in csv_input.readlines():
                split = line.replace('\'', '\'\'').split(';')
                split[-1] = split[-1].strip()
                output.write(insert % tuple(split))
            output.write('')

    read_csv('Customers.csv', customer_insert)
    read_csv('Products.csv', product_insert)
    read_csv('Orders.csv', order_insert)
    read_csv('Positions.csv', position_insert)
