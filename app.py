from model import (Base, session, Product, engine)
import datetime
import csv


def menu():
    while True:
        print('''
            \nPRODUCTS INVENTORY
            \rV) View Product
            \rA) Add Product
            \rB) Backup''')
        choice = input("What would you like to do?\n")
        if choice.upper() in ['V', 'A', 'B']:
            return choice
        else:
            input('''
                    \rPlease choose one of the options above.
                    \rV, A or B
                    \rPress enter to try again.''')


def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
            \n***** DATE ERROR *****
            \rThe date format shout include a valid Month Date, from the past
            \rEx: 11/1/2018
            \rPress enter to try again
            \r**********************''')
        return
    else:
        return return_date


def clean_price(price_str):
    try:
        split_price = price_str.split('$')
        price_float = float(split_price[1])
    except ValueError:
        input('''
            \n***** PRICE ERROR *****
            \rThe price should be a number with a currency symbol
            \rEx: $5.99
            \rPress enter to try again
            \r***********************''')
    else:
        return int(price_float * 100)


def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        # we need to skip the first row
        # https://www.kite.com/python/answers/how-to-skip-the-first-line-of-a-csv-file-in-python
        next(data)
        for row in data:
            # here we check if the product is already in the db
            # returns one if there is one or none if there is none
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = int(row[2])
                date_updated = clean_date(row[3])
                new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date_updated)
                session.add(new_product)
            #print(row)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'V':
            # view product details
            pass
        elif choice == 'A':
            # add product
            pass
        else:
            # backup database
            pass



if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
