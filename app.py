from model import (Base, session, Product, engine)
import datetime
import csv
import time


def menu():
    while True:
        print('''
            \nPRODUCTS INVENTORY
            \rV) View Product
            \rA) Add Product
            \rB) Backup
            \rQ) Quit''')
        choice = input("What would you like to do?\n").upper()
        if choice in ['V', 'A', 'B', 'Q']:
            return choice
        else:
            input('''
                    \rPlease choose one of the options above.
                    \rV, A, B or Q
                    \rPress enter to try again.''')


def clean_date(date_str):
    split_date = date_str.split('/')
    month = int(split_date[0])
    day = int(split_date[1])
    year = int(split_date[2])
    return_date = datetime.date(year, month, day)
    return return_date


def clean_price(price_str):
    try:
        split_price = price_str.split('$')
        price_float = float(split_price[1])
    except (ValueError, IndexError):
        input('''
            \n***** PRICE ERROR *****
            \rThe price should be a number with a currency symbol
            \rEx: $5.99
            \rPress enter to try again
            \r***********************''')
    else:
        return int(price_float * 100)


def clean_id(id_str, options):
    try:
        product_id = int(id_str)
    except ValueError:
        input('''
            \n***** ID ERROR *****
            \rThe ID should be a number.
            \rPress enter to try again.
            \r********************''')
        return
    else:
        if product_id in options:
            return product_id
        else:
            input(f'''
                \n***** ID ERROR *****
                \rOptions: {options}
                \rPress enter to try again.
                \r********************''')
            return


def view_product():
    product_id_options = []
    for product in session.query(Product):
        product_id_options.append(product.product_id)
    product_id_error = True
    while product_id_error:
        product_id_choice = input(f'''
            \nProduct ID options: {product_id_options}
            \nProduct ID: ''')
        product_id_choice = clean_id(product_id_choice, product_id_options)
        if type(product_id_choice) == int:
            product_id_error = False
    the_product = session.query(Product).filter(
        Product.product_id==product_id_choice).first()
    print(f'''
        \nProduct Name = {the_product.product_name},
        \rProduct Price = ${the_product.product_price/100},
        \rQuantity = {the_product.product_quantity},
        \rLast Updated = {the_product.date_updated.strftime("%m/%d/%Y")}''')
    time.sleep(1.5)


def add_product():
    product_name = input('What is the product name? ')
    price_error = True
    while price_error:
        product_price = input('How much is the product (Ex $4.99)? ')
        product_price = clean_price(product_price)
        if type(product_price) == int:
            price_error = False
    quantity_error = True
    while quantity_error:
        product_quantity = input('How many are there in stock? ')
        try:
            int(product_quantity)
        except ValueError:
            input('''
                \n***** QUANTITY ERROR *****
                \rThe quantity should be a whole number
                \rEx: 83
                \rPress enter to try again
                \r***********************''')
        else:
            quantity_error = False
    now = datetime.datetime.now()
    date_updated = clean_date(now.strftime("%m/%d/%Y"))
    new_product = Product(product_name=product_name,
        product_price=product_price,
        product_quantity=product_quantity,
        date_updated=date_updated)
    # code to check whether product already exists
    # if it exists it updates that entry with the new price, quantity and
    # date updated
    product_in_db = session.query(Product).filter(
        Product.product_name==new_product.product_name).one_or_none()
    if product_in_db != None:
            session.query(Product).filter(
                Product.product_name==new_product.product_name).update({
                Product.product_price: new_product.product_price,
                Product.product_quantity: new_product.product_quantity,
                Product.date_updated: new_product.date_updated
            })
    else:
        session.add(new_product)
    session.commit()
    print('Product added or updated!')
    time.sleep(1.5)


def backup_database():
    backup_choice = input('''
        \n***** WARNING *****
        \rYou are about to make a backup of the database
        \rAre you sure you wish to proceed? ('Y' or 'N')\n''').upper()
    if backup_choice == 'Y':
        now = datetime.datetime.now().date()
        # I've added the now_timestamp as this felt like a good idea
        # for a production environment. After all, you want to know
        # when the backup was created.
        file = open(f"backup_database_{now}.csv", "a")
        file.write('product_name,product_price,product_quantity,date_updated\n')
        for product in session.query(Product):
            file.write(f'{product}\n')
        file.close()
        print('\n*** BACKUP CREATED ***')
    else:
        return


def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        # we need to skip the first row
        # https://www.kite.com/python/answers/how-to-skip-the-first-line-of-a-csv-file-in-python
        next(data)
        for row in data:
            # here we check if the product is already in the db
            # returns one if there is one or none if there is none
            product_in_db = session.query(Product).filter(
                Product.product_name==row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = int(row[2])
                date_updated = clean_date(row[3])
                new_product = Product(
                    product_name=product_name,
                    product_price=product_price,
                    product_quantity=product_quantity,
                    date_updated=date_updated)
                session.add(new_product)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'V':
            view_product()
        elif choice == 'A':
            add_product()
        elif choice == 'B':
            backup_database()
        else:
            print('GOODBYE')
            app_running = False
            return


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
