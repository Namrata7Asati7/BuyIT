from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from flask import jsonify
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'namrata_sql',
    'database': 'arunicecream'
}

# Establish a connection to the MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    class Product(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80))
        price = db.Column(db.Float)
        image = db.Column(db.String(120))

    db.create_all()

# Create the orders table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    phone VARCHAR(20),
    description TEXT,
    items TEXT
)''')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    # Fetch product data from the database
    cursor.execute("SELECT id, name, price, image_url FROM products")
    products = cursor.fetchall()
    product_list = [{'id': p[0], 'name': p[1], 'price': p[2], 'image_url': p[3]} for p in products]
    return render_template('products.html', products=product_list)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()  # Receive data from JavaScript fetch
    product_id = data.get('product_id')

    # Get product from database
    product = Product.query.get(product_id)

    if product:
        # Check if cart exists in session, otherwise create it
        if 'cart' not in session:
            session['cart'] = []

        cart = session['cart']

        # Check if the product is already in the cart
        for item in cart:
            if item['id'] == product.id:
                item['quantity'] += 1
                break
        else:
            # Add the new product to the cart
            cart.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image': url_for('static', filename=f'images/{product.image}'),
                'quantity': 1
            })

        session['cart'] = cart

        return jsonify({"message": "Product added to cart", "status": "success"})
    
    return jsonify({"message": "Product not found", "status": "error"})

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)  # Calculate total price
    return render_template('cart.html', cart_items=cart, total=total)

@app.route('/order', methods=['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        description = request.form['description']
        items = ', '.join([f"{p['name']} - ₹{p['price']}" for p in session.get('cart', [])])

        # Insert order into MySQL database
        cursor.execute("INSERT INTO orders (name, address, phone, description, items) VALUES (%s, %s, %s, %s, %s)", 
                       (name, address, phone, description, items))
        conn.commit()

        # Clear the cart after placing the order
        session.pop('cart', None)
        return redirect(url_for('payment'))

    # If GET request, render the order page
    return render_template('order.html')


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    cart_items = session.get('cart', [])
    
    if not cart_items:
        return render_template('payment.html', cart_items=None, total_price=0)

    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    if request.method == 'POST':
        # Clear the cart after payment
        session.pop('cart', None)

        # Redirect to a success page or order confirmation
        return redirect(url_for('success'))

    return render_template('payment.html', cart_items=cart_items, total_price=total_price)


@app.route('/order_confirmation')
def order_confirmation():
    return "Thank you for your order!"




if __name__ == '__main__':
    app.run(debug=True)
