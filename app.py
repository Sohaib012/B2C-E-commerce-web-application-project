from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash,render_template,request,session, redirect, url_for
from strgen import StringGenerator as SG
from sqlalchemy import create_engine  
from sqlalchemy import Column, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload
import uuid
from flask import Flask
import logging



app = Flask(__name__)



#configure app to enable it to interact with your database
#format: 'postgresql://user:password@localhost/database name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@localhost:5433/ecommsite'

db = SQLAlchemy(app)

# Database relational models based on flask-SQLAlchemy ORM syntax
class Aboutorder(db.Model):
    __tablename__ = 'aboutorder'

    order_id = db.Column(db.String(20), primary_key=True)
    order_num = db.Column(db.Integer)
    ship_via = db.Column(db.String(20))
    shipper_id = db.Column(db.String(20))
    order_date = db.Column(db.Date)
    shipped_date = db.Column(db.Date)
    customer = db.Column(db.ForeignKey('customer.customer_id'))

    customer1 = db.relationship('Customer', primaryjoin='Aboutorder.customer == Customer.customer_id', backref='aboutorders')



class Admin(db.Model):
    __tablename__ = 'admin'

    admin_id = db.Column(db.String(20), primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    login_id = db.Column(db.String(20), unique=True)



class Billinginfo(db.Model):
    __tablename__ = 'billinginfo'

    billing_id = db.Column(db.String(40), primary_key=True)
    credit_card_pin = db.Column(db.Integer)
    credit_card_num = db.Column(db.Integer)
    bill_date = db.Column(db.Date)
    billing_addr = db.Column(db.String)
    credit_card_expiry = db.Column(db.Date)
    customer = db.Column(db.ForeignKey('customer.customer_id'))
    aboutorder = db.Column(db.ForeignKey('aboutorder.order_id'))

    aboutorder1 = db.relationship('Aboutorder', primaryjoin='Billinginfo.aboutorder == Aboutorder.order_id', backref='billinginfos')
    customer1 = db.relationship('Customer', primaryjoin='Billinginfo.customer == Customer.customer_id', backref='billinginfos')



class Cart(db.Model):
    __tablename__ = 'cart'

    cart_id = db.Column(db.String(20), primary_key=True)
    nop = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    customer = db.Column(db.ForeignKey('customer.customer_id'))

    #customer1 = db.relationship('Customer', primaryjoin='Cart.customer == Customer.customer_id', backref='carts')
    
class CartProduct(db.Model):
    __tablename__ = 'cart_products'
    
    cart_id = db.Column(db.String(20), db.ForeignKey('cart.cart_id'), primary_key=True)
    product_id = db.Column(db.String(20), db.ForeignKey('product.product_id'), primary_key=True)
    quantity = db.Column(db.Integer) 

class Category(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.String(20), primary_key=True)
    category_name = db.Column(db.String(20))
    description = db.Column(db.String(50))



class Customer(db.Model):
    __tablename__ = 'customer'

    customer_id = db.Column(db.String(20), primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    loginid = db.Column(db.String(10), unique = True)
    passwd = db.Column(db.String(20), unique=True)
    contact_num = db.Column(db.String)



class Orderdetail(db.Model):
    __tablename__ = 'orderdetails'

    useless_id = db.Column(db.Integer, primary_key=True)
    unit_price = db.Column(db.Float(53))
    discount = db.Column(db.Float(53))
    order_num = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    product = db.Column(db.ForeignKey('product.product_id'))
    aboutorder = db.Column(db.ForeignKey('aboutorder.order_id'))

    aboutorder1 = db.relationship('Aboutorder', primaryjoin='Orderdetail.aboutorder == Aboutorder.order_id', backref='orderdetails')
    product1 = db.relationship('Product', primaryjoin='Orderdetail.product == Product.product_id', backref='orderdetails')



class PersonalInfo(db.Model):
    __tablename__ = 'personal_info'

    dummy_id = db.Column(db.String(20), primary_key=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(80))
    city = db.Column(db.String(10))
    country = db.Column(db.String(20))
    postal_code = db.Column(db.Integer)
    email = db.Column(db.String(30), unique=True)
    passwd = db.Column(db.String(20))
    login_id = db.Column(db.String(20), unique=True)
    customer = db.Column(db.ForeignKey('customer.customer_id'))

    customer1 = db.relationship('Customer', primaryjoin='PersonalInfo.customer == Customer.customer_id', backref='personal_infos')



class Product(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.String(20), primary_key=True)
    quantity_pu = db.Column(db.Integer)
    product_name = db.Column(db.String(20))
    stock_units = db.Column(db.Integer)
    unit_weight = db.Column(db.Float(53))
    discount = db.Column(db.Float(53))
    reorder_level = db.Column(db.Integer)
    price = db.Column(db.Integer)
    product_description = db.Column(db.String(30))
    supplier_id = db.Column(db.String(20))
    category = db.Column(db.ForeignKey('category.category_id'))

    category1 = db.relationship('Category', primaryjoin='Product.category == Category.category_id', backref='products')



class Shipper(db.Model):
    __tablename__ = 'shipper'

    shipper_id = db.Column(db.String(40), primary_key=True)
    phone = db.Column(db.String(20))
    company_name = db.Column(db.String(20))
    aboutorder = db.Column(db.ForeignKey('aboutorder.order_id'))

    aboutorder1 = db.relationship('Aboutorder', primaryjoin='Shipper.aboutorder == Aboutorder.order_id', backref='shippers')



class Supplier(db.Model):
    __tablename__ = 'supplier'

    supplier_id = db.Column(db.String(20), primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))



class Trackinginfo(db.Model):
    __tablename__ = 'trackinginfo'

    tracking_id = db.Column(db.String(20), primary_key=True)
    delivery_date = db.Column(db.Date)
    shipped_date = db.Column(db.Date)
    product = db.Column(db.ForeignKey('product.product_id'))
    aboutorder = db.Column(db.ForeignKey('aboutorder.order_id'))

    aboutorder1 = db.relationship('Aboutorder', primaryjoin='Trackinginfo.aboutorder == Aboutorder.order_id', backref='trackinginfos')
    product1 = db.relationship('Product', primaryjoin='Trackinginfo.product == Product.product_id', backref='trackinginfos')

    

#set secret key for the app in order to use sessions 
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#routing the app to the login page.(In this case this is my starting page for now)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
         return render_template('login.html', error=None)
    
    # Verify reCAPTCHA
    # response = request.form.get('g-recaptcha-response')
    # if not response:
    #     return render_template('login.html', error='Please complete the reCAPTCHA.')
    
    usr = request.form.get('username')
    entered_password = request.form.get('password')

    if usr and entered_password:
        customer = Customer.query.filter_by(loginid=usr).first()
        if customer and customer.passwd == entered_password:
            session['username'] = usr
            session['customer_id'] = customer.customer_id
            flash('You are successfully logged in')
            return redirect(url_for('login'))
        else:
            error = 'Invalid Credentials. Please try again.'
    else:
        error = 'Missing username or password. Please try again.'

    return render_template('login.html', error=error)


#routing to createuser page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        fn=request.form['first_name']
        ln=request.form['last_name']
        usr=request.form['loginid']
        cno=request.form['contact_num']
        pwd=request.form['passwd']

        error = None

        if not (fn and ln and usr and cno and pwd):
            error = "Failure: Credentials are not filled in properly."
            return render_template('createuser.html', error)

        usr_exists = Customer.query.filter_by(loginid=usr).first()
        if usr_exists:
            error = "Failure: Username already exists"  
            return render_template('createuser.html', error)
                
        c_id = str(uuid.uuid4())[:8]
        new_customer = Customer(customer_id=c_id, first_name=fn, last_name=ln, loginid=usr, passwd=pwd, contact_num=cno)
        db.session.add(new_customer)
        db.session.commit()
        flash('User successfully created')
        return redirect(url_for('login'))
    
    return render_template('register.html', error = None)


def getLoginDetails():
    loggedIn = False
    firstName = ''
    noOfItems = 0

    if 'username' in session:
        loggedIn = True
        usr = session['username']

        # get the number of items in the cart for the current user
        user = Customer.query.filter_by(loginid=usr).first()
        if user:
            cart = Cart.query.filter_by(customer_id=user.customer_id).all()
            noOfItems = len(cart)

    return loggedIn, firstName, noOfItems

@app.route("/loco")
def loco():
    return render_template('loco.html')

@app.route("/category")
def displayCategory():
    category_id = request.args.get('categoryId')
    category = Category.query.filter_by(category_id=category_id).first()
    products = db.session.query(Product).join(Category, Product.category == Category.category_id).filter(Category.category_id == category_id).all()
    return render_template('category.html', products=products, category = category)

@app.route("/productDescription")
def productDescription():
    product_id = request.args.get('productId')
    productData = Product.query.filter_by(product_id=product_id).first()
    return render_template("product.html", productdata=productData)

@app.route("/addToCart", methods=["POST"])
def addToCart():
    if 'username' not in session:
        return redirect(url_for('login'))

    else:
        product_id = request.args.get('productId')
        cust_id = session['customer_id']
    
        productData = Product.query.filter_by(product_id=product_id).first()
        # Check if the product is already in the cart
        cart = Cart.query.filter_by(customer=cust_id).first()

        if not cart:
            # If the customer doesn't have a cart, create a new one
            cart = Cart(cart_id=str(uuid.uuid4())[:20], customer=cust_id, nop=0, total_price=0)
            db.session.add(cart)


        # Check if the product is already in the cart
        cart_product = CartProduct.query.filter_by(cart_id=cart.cart_id, product_id=product_id).first()

        if cart_product:
            cart_product.quantity += int(request.form['quantity'])
            cart.nop += int(request.form['quantity'])  
            productData.quantity_pu -= int(request.form['quantity'])  
        else:
            cart_product = CartProduct(cart_id=cart.cart_id, product_id=product_id, quantity=int(request.form['quantity']))
            cart.nop += int(request.form['quantity'])
            db.session.add(cart_product)
            productData.quantity_pu -= int(request.form['quantity'])

        # Update the total price
        product = Product.query.get(product_id)
        cart.total_price += product.price * int(request.form['quantity'])

        db.session.commit()

        msg = "Added successfully"
        return redirect(url_for('cart'))
    
@app.route("/cart")
def cart():
    if 'username' not in session:
        return redirect(url_for('login'))

    cust_id = session['customer_id']
    cust = Customer.query.filter_by(customer_id=cust_id).first()

    products = (
        db.session.query(Product, CartProduct.quantity)
        .join(CartProduct)
        .join(Cart)
        .filter(Cart.customer == cust_id)
        .all()
        )

    cart = Cart.query.filter_by(customer=cust_id).first()
    if cart:
        total_price = cart.total_price
        nop = cart.nop
    else:
        return render_template("cart.html", totalPrice=0, noOfItems=0)
    return render_template("cart.html", products=products, totalPrice=total_price, noOfItems=nop)


@app.route("/removeFromCart", methods=["POST"])
def removeFromCart():
    if 'username' not in session:
        return redirect(url_for('login'))

    usr = session['username']
    cust_id = session['customer_id']
    product_id = request.form['productId']

    cust = Customer.query.filter_by(loginid=usr).first()
    cart = Cart.query.filter_by(customer=cust_id).first()

    try:
        cart_product = CartProduct.query.filter_by(cart_id=cart.cart_id, product_id=product_id).first()
        db.session.delete(cart_product)
        cart.nop -= cart_product.quantity
        product = Product.query.get(product_id)
        product.quantity_pu += cart_product.quantity
        cart.total_price -= product.price * cart_product.quantity
        db.session.commit()
        msg = "removed successfully"
    except Exception as e:
        db.session.rollback()
        msg = "error occurred"
        logging.error(f"Error removing item from cart: {msg}. Exception: {e}")

    return redirect(url_for('cart'))

@app.route("/")
def index():

    productData = db.session.query(Product).all()
    categoryData = db.session.query(Category).all()

    return render_template('index.html', productData=productData, categoryData=categoryData)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
