# Class 2 Thabo Setsubi
# Flask End of Module Project
# Point of Sale API
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from smtplib import SMTPRecipientsRefused
import sqlite3


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


class Products(object):
    def __init__(self, product_id, name, price, desc, product_type):
        self.id = product_id
        self.name = name
        self.price = price
        self.desc = desc
        self.type = product_type


# class Database:
#     def __init__(self):
#         self.conn = sqlite3.connect("shoppers.db")
#         self.cursor = self.conn.cursor()

# function that initialises the user table
def init_users_table():
    conn = sqlite3.connect('shoppers.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "first_name TEXT NOT NULL,"
                 "last_name TEXT NOT NULL,"
                 "address TEXT NOT NULL,"
                 "email TEXT NOT NULL,"
                 "username TEXT NOT NULL,"
                 "password TEXT NOT NULL)")
    print("user table created successfully")
    conn.close()
    return init_users_table


# Initialising the products table
def init_products_table():
    with sqlite3.connect("shoppers.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS product (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "name TEXT NOT NULL,"
                     "price INTEGER NOT NULL,"
                     "description TEXT NOT NULL,"
                     "type TEXT NOT NULL,"
                     "quantity TEXT NOT NULL)")
        print("products table created successfully")
    return init_products_table


# Initialising the admin table
def init_admin_table():
    with sqlite3.connect("shoppers.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS admin (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "first_name TEXT NOT NULL,"
                     "last_name TEXT NOT NULL,"
                     "address TEXT NOT NULL,"
                     "email TEXT NOT NULL,"
                     "username TEXT NOT NULL,"
                     "password TEXT NOT NULL)")
        print("admin table created successfully")
    return init_admin_table


# function that fetches the users and puts it into a list
def fetch_users():
    with sqlite3.connect('shoppers.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        shoppers = cursor.fetchall()

        new_data = []

        for data in shoppers:
            print(data)
            new_data.append(User(data[0], data[5], data[6]))
    return new_data


def fetch_products():
    with sqlite3.connect("shoppers.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product")
        items = cursor.fetchall()

        new_item = []

        for data in items:
            print(data)
            new_item.append(Products(data[0], data[1], data[2], data[3], data[4]))
        return new_item


def fetch_admin():
    with sqlite3.connect('shoppers.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin")
        shoppers = cursor.fetchall()

        new_data = []

        for data in shoppers:
            print(data)
            new_data.append(User(data[0], data[5], data[6]))
    return new_data


# calling the functions
init_users_table()
init_admin_table()
init_products_table()
users = fetch_users()
products = fetch_products()
fetch_admin()


# to start the flask app
app = Flask(__name__)
# to make sure that the front end can fetch the api
CORS(app)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
# this is for the flask mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lifechoiceslotto147@gmail.com'
app.config['MAIL_PASSWORD'] = 'lifechoices2021'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# a route that register a new user
@app.route('/user-registration/', methods=["POST"])
def user_registration():
    response = {}

    try:
        # using a POST method to create a new user
        if request.method == "POST":
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            address = request.form['address']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            # connecting to the database
            with sqlite3.connect('shoppers.db') as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO user("
                               "first_name,"
                               "last_name,"
                               "address,"
                               "email,"
                               "username,"
                               "password) VALUES(?, ?, ?, ?, ?, ?)",
                               (first_name, last_name, address, email, username, password))
                conn.commit()
                # this response sent to the frontend
                response["message"] = "success"
                response["status_code"] = 201
                # email will be sent to users email
                msg = Message("Welcome new user!!!", sender="lifechoiceslotto147@gmail.com", recipients=[email])
                msg.body = "You have successfully registered an account. Welcome " + first_name
                mail.send(msg)
            return response
    # error handling for the email
    except SMTPRecipientsRefused:
        response["message"] = "Invalid email used"
        response["status_code"] = 400
        return response


@app.route('/admin-registration/', methods=['POST'])
def admin_registration():
    response = {}
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect("shoppers.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO admin("
                           "first_name,"
                           "last_name,"
                           "address,"
                           "email,"
                           "username,"
                           "password) VALUES(?, ?, ?, ?, ?, ?)",
                           (first_name, last_name, address, email, username, password))
            conn.commit()
            response["message"] = " admin registered successfully"
            response["status_code"] = 201
            # email will be sent to users email
            msg = Message("Welcome new user!!!", sender="lifechoiceslotto147@gmail.com", recipients=[email])
            msg.body = "You have successfully registered an account. Welcome " + first_name
            mail.send(msg)
        return response


# a route to view a single users profile
@app.route('/view-profile/<int:user_id>')
def view_profile(user_id):
    response = {}

    # connecting to the database
    with sqlite3.connect("shoppers.db") as conn:
        cursor = conn.cursor()
        # Select statement to view all the details about a certain user
        cursor.execute("SELECT * FROM user WHERE user_id=" + str(user_id))

        # message to the front end
        response["status_code"] = 200
        response["description"] = "Profile retrieved successfully"
        response["data"] = cursor.fetchone()
    # putting the in a JSON format
    return jsonify(response)


# a route to add new products
@app.route('/create-products', methods=["POST"])
def create_products():
    response = {}

    # using post method to create products
    if request.method == "POST":
        # the user fill in certain details about the product
        name = request.form['name']
        price = request.form['price']
        desc = request.form['description']
        product_type = request.form['type']
        quantity = request.form['quantity']

        # CONNECTING TO THE DATABASE
        with sqlite3.connect("shoppers.db") as conn:
            cursor = conn.cursor()
            # using the insert statement to create a product
            cursor.execute("INSERT INTO product("
                           "name,"
                           "price,"
                           "description,"
                           "type,"
                           "quantity) VALUES (?, ?, ?, ?, ?)",
                           (name, price, desc, product_type, quantity))
            conn.commit()
            # sending a message to the front end developer
            response["status_code"] = 201
            response["description"] = "Product created successfully"
        return response


@app.route('/show-users/')
def show_users():
    response = {}
    with sqlite3.connect("shoppers.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")

        response["status_code"] = 200
        response["description"] = "Displaying all users for the admin"
        response['data'] = cursor.fetchall()
    return jsonify(response)


# a route to show all the products
@app.route('/show-products')
def show_products():
    response = {}

    # connecting to the database
    with sqlite3.connect("shoppers.db") as conn:
        cursor = conn.cursor()
        # Using select statement to display the information
        cursor.execute("SELECT * FROM product")

        response["status_code"] = 200
        response["description"] = "Displaying all products successfully"
        response["data"] = cursor.fetchall()
    return jsonify(response)


# a route to delete a specific product
@app.route('/delete-products/<int:product_id>')
def delete_products(product_id):
    response = {}

    # connecting to the database
    with sqlite3.connect("shoppers.db") as conn:
        cursor = conn.cursor()
        # using the delete statement to delete the product
        cursor.execute("DELETE FROM product WHERE id=" + str(product_id))
        conn.commit()
        # a message that gets sent to the front end
        response['status_code'] = 200
        response['message'] = "Product successfully deleted"

    return response


@app.route('/delete-profile/<int:user_id>')
def delete_user(user_id):
    response = {}

    with sqlite3.connect("shoppers.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user WHERE id=" + str(user_id))
        conn.commit()

        response['status_code'] = 200
        response['message'] = "User successfully deleted"

    return response


# a route that allows the user to edit certain details about the product
@app.route('/edit-products/<int:product_id>', methods=["PUT"])
def edit_products(product_id):
    response = {}
    # using the PUT method to update certain details of a certain product
    if request.method == "PUT":
        # connecting to a database
        with sqlite3.connect("shoppers.db") as conn:
            # making the data a dictionary
            incoming_data = dict(request.json)

            put_data = {}
            # changing the specific details
            if incoming_data.get("price") is not None:
                put_data["price"] = incoming_data.get("price")
                with sqlite3.connect("shoppers.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE product SET price=? WHERE id=?", (put_data["price"], product_id))
                    conn.commit()
                    # a message that gets sent to the front end
                    response['message'] = "Update was successful"
                    response['status_code'] = 200
                return response
            if incoming_data.get("quantity") is not None:
                put_data["quantity"] = incoming_data.get("quantity")
                with sqlite3.connect("shoppers.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE product SET quantity=? WHERE id=?", (put_data["quantity"], product_id))
                    conn.commit()
                    response['message'] = "Update was successful"
                    response['status_code'] = 200

                return response
            # trying to update the new total price
            new_price = int(incoming_data.get("price"))
            new_quantity = int(incoming_data.get("quantity"))
            new_total = new_price * new_quantity
            if incoming_data.get("total") is not None:
                put_data["total"] = incoming_data.get("total")
                with sqlite3.connect("shoppers.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE product SET total WHERE id=?", (new_total, product_id))
                    response['status_code'] = 200
                    response['message'] = "Update was successful"
                return response


@app.route('/edit-users/<int:user_id>', methods=['PUT'])
def edit_users(user_id):
    response = {}

    if request.method == "PUT":
        with sqlite3.connect("shoppers.db") as conn:
            incoming_data = dict(request.json)

            put_data = {}
            if incoming_data.get("first_name") is not None:
                put_data["first_name"] = incoming_data.get("first_name")
                with sqlite3.connect("shoppers.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE user SET first_name=? WHERE user_id=?", (put_data["first_name"], user_id))
                    conn.commit()

                    response['message'] = "Update was successful"
                    response['status_code'] = 200
                return response
            if incoming_data.get("last_name") is not None:
                put_data["last_name"] = incoming_data.get("last_name")
                with sqlite3.connect("shoppers.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE user SET last_name=? WHERE user_id=?", (put_data["last_name"], user_id))
                    conn.commit()

                    response['message'] = "Update was successful"
                    response['status_code'] = 200
                return response
            if incoming_data.get("email") is not None:
                put_data["email"] = incoming_data.get("email")
                with sqlite3.connect("shoppers.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE user SET email=? WHERE user_id=?", (put_data["email"], user_id))
                    conn.commit()

                    response['message'] = "Update was successful"
                    response['status_code'] = 200
                return response


# a route that sends an email to the user
@app.route('/send-email/<int:user_id>', methods=['GET', 'POST'])
def send_email(user_id):
    response = {}
    products = 'You have successfully registered an account'

    try:
        if request.method == "POST":
            with sqlite3.connect("shoppers.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM user WHERE user_id=?", str(user_id))
                receiver = cursor.fetchall()
                print(receiver)
                for data in receiver:
                    print(data)
                    msg = Message("Product received", sender="lifechoiceslotto147@gmail.com", recipients=[data[4]])
                    msg.body = products
                    mail.send(msg)
            response['status_code'] = 200
            response['message'] = "Email was sent successful"
        return response
    except SMTPRecipientsRefused:
        response["message"] = "Invalid email used"
        response["status_code"] = 400
        return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    response = {}
    username = users
    new = []
    if request.method == "GET":
        with sqlite3.connect('shoppers.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user")
            data = cursor.fetchall()
            for i in data:
                print(i)
                if request.form['username'] == i[5] and request.form['password'] == i[6]:
                    response['message'] = "Login successful"
                    response['status_code'] = 200
        return response


@app.route('/admin-login')
def admin_login():
    response = {}
    username = users
    new = []
    if request.method == "GET":
        with sqlite3.connect('shoppers.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admin")
            data = cursor.fetchall()
            for i in data:
                print(i)
                if request.form['username'] == i[5] and request.form['password'] == i[6]:
                    response['message'] = "Login successful"
                    response['status_code'] = 200
        return response


# This statement helps run the flask app instead of using the terminal
if __name__ == '__main__':
    app.run()

