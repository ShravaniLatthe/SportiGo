from flask import *
import mysql.connector
from werkzeug.utils import secure_filename
import os
from fileinput import filename

from flask import Flask, render_template,request,redirect,session,flash
from flask_mysqldb import MySQL
from mysql.connector import cursor

app=Flask(__name__)

UPLOAD_FOLDER='static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'SportiGo'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/category',methods=['GET','POST'])
def category():
    if request.method=='POST':
        detail=request.form
        c_name=detail['c_name']
        c_image=request.files['c_image']
        file_path=os.path.join(app.config['UPLOAD_FOLDER'],c_image.filename)
        c_image.save(file_path)
        c_desc=detail['c_desc']

        cur=mysql.connection.cursor()
        cur.execute("insert into db_addcategory (category_name,category_image,category_desc)values(%s,%s,%s)",(c_name,file_path,c_desc))
        mysql.connection.commit()
        cur.close()
        return "<script>alert('Record Inserted Sucessfully !!!');</script>"+render_template('add_category.html')
        return c_name,c_image,c_desc

    return render_template('add_category.html')


@app.route('/category_list')
def category_list():
    cur=mysql.connection.cursor()
    cur.execute("select * from db_addcategory")
    data=cur.fetchall()
    return render_template('category_list.html',value=data)

@app.route('/delete_category',methods=['GET','POST'])
def delete_category():
    if request.method=='POST':
        details=request.form
        c_id=details['c_id']
        cur=mysql.connection.cursor()
        cur.execute("delete from db_addcategory where id=%s",(c_id))
        mysql.connection.commit()
        cur.close()
        return redirect('category_list')

@app.route('/update_category',methods=['GET','POST'])
def update_category():
    if request.method=='POST':
        details=request.form
        c_id=details['c_id']
        c_name=details['c_name']
        c_image=details['c_image']
        c_desc=details['c_desc']
        cur=mysql.connection.cursor()
        cur.execute("update db_addcategory set c_name=%s,c_image=%s,c_desc=%s where id=%s",(c_name,c_image,c_desc,c_id))
        mysql.connection.commit()
        cur.close()
        return redirect('category_list')


@app.route('/view_category',methods=['GET','POST'])
def view_category():
    cur=mysql.connection.cursor()
    cur.execute("select * from db_addcategory")
    data=cur.fetchall()
    cur.close()
    return render_template('view_category.html',value=data)

@app.route('/category_products/<int:category_id>')
def category_products(category_id):

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM db_addproduct WHERE product_category=%s",
        (category_id,)
    )

    products = cur.fetchall()

    cur.execute(
        "SELECT category_name FROM db_addcategory WHERE id=%s",
        (category_id,)
    )

    category = cur.fetchone()

    cur.close()

    return render_template(
        'category_products.html',
        products=products,
        category_name=category[0]
    )

@app.route('/product',methods=['GET','POST'])
def product():
    cur = mysql.connection.cursor()

    # get categories
    cur.execute("SELECT * FROM db_addcategory")
    categories = cur.fetchall()

    if request.method == 'POST':
        p_name = request.form['p_name']
        p_size = request.form['p_size']
        p_price = request.form['p_price']
        p_brand = request.form['p_brand']

        #
        p_image = request.files['p_image']

        if p_image and p_image.filename != "":
            filename = p_image.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            p_image.save(file_path)
        else:
            filename = ""

        p_discount = request.form['p_discount']
        p_category = request.form['p_category']

        cur.execute("""INSERT INTO db_addproduct (product_name,product_size,product_price,product_brand,product_image,product_discountprice,product_category)VALUES (%s,%s,%s,%s,%s,%s,%s)""",(p_name,p_size,p_price,p_brand,filename,p_discount,p_category))

        mysql.connection.commit()

        return "<script>alert('Product Added');</script>" + render_template('add_product.html', categories=categories)

    cur.close()
    return render_template('add_product.html', categories=categories)

@app.route('/product_list')
def product_list():
    cur=mysql.connection.cursor()
    cur.execute("select * from db_addproduct")
    data=cur.fetchall()
    return render_template('product_list.html',value=data)

@app.route('/delete_product',methods=['GET','POST'])
def delete_product():
    if request.method=='POST':
        details=request.form
        p_id=details['p_id']
        cur=mysql.connection.cursor()
        cur.execute("delete from db_addproduct where id=%s",(p_id))
        mysql.connection.commit()
        cur.close()
        return redirect('product_list')

@app.route('/update_product',methods=['GET','POST'])
def update_product():
    if request.method=='POST':
        details=request.form
        p_id=details['p_id']
        p_name=details['p_name']
        p_size=details['p_size']
        p_price=details['p_price']
        p_brand = details['p_brand']
        p_image = details['p_image']
        p_discount = details['p_discount']
        p_category = details['p_category']
        cur=mysql.connection.cursor()
        cur.execute("update db_addcategory set p_name=%s,p_size=%s,p_price=%s,p_brand=%s,p_image=%s,p_discount=%s,p_category=%s where id=%s",(p_name,p_size,p_price,p_brand,p_image,p_discount,p_category,p_id))
        mysql.connection.commit()
        cur.close()
        return redirect('product_list')

@app.route('/view_product',methods=['GET','POST'])
def view_product():
    cur=mysql.connection.cursor()
    cur.execute("select * from db_addproduct")
    data=cur.fetchall()
    cur.close()
    return render_template('view_product.html',value=data)

@app.route('/product_details/<int:p_id>',)
def product_details(p_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM db_addproduct WHERE id=%s", (p_id,))
    product = cur.fetchone()
    cur.close()

    return render_template('product_details.html', product=product)




@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():

    if request.method=='POST':
        details=request.form
        email=details['email']
        password=details['pass']
        cur=mysql.connection.cursor()
        cur.execute("select * from db_adminreg where email=%s and password=%s",(email,password))
        data=cur.fetchone()
        if data:

            session['email']=email
            session['fname']=data[1]
            session['lname'] = data[1]
            session['user']="Admin"
            return redirect('category')

        else:
            return "<script>alert('Login Failed')</script>" + render_template('admin_login.html')
    return render_template('admin_login.html')

@app.route('/adminregister',methods=['GET','POST'])
def adminregister():
    if request.method == 'POST':
        detail = request.form
        first_name = detail['fname']
        last_name = detail['lname']
        address = detail['address']
        contact = detail['cno']
        email = detail['email']
        password = detail['pass']
        cur = mysql.connection.cursor()
        cur.execute("insert into db_adminreg (first_name,last_name,address,contact,email,password)values(%s,%s,%s,%s,%s,%s)",
                    (first_name, last_name, address,contact,email,password))
        mysql.connection.commit()
        cur.close()
        flash("Suceessfulyy registered")
        return redirect('adminlogin')
    return render_template('admin_register.html')

@app.route('/userlogin',methods=['GET','POST'])
def userlogin():
    if request.method=='POST':
        details=request.form
        email=details['email']
        password=details['pass']
        cur=mysql.connection.cursor()
        cur.execute("select * from db_userreg where email=%s and password=%s",(email,password))
        data=cur.fetchone()
        if data:

            session['email']=email
            session['fname']=data[1]
            session['lname'] = data[1]
            session['user']="User"
            return redirect('view_product')

        else:
            return "<script>alert('Login Failed')</script>" + render_template('user_login.html')
    return render_template('user_login.html')

@app.route('/userregister',methods=['GET','POST'])
def userregister():
    if request.method == 'POST':
        detail = request.form
        first_name = detail['fname']
        last_name = detail['lname']
        address = detail['address']
        contact = detail['cno']
        email = detail['email']
        password = detail['pass']
        cur = mysql.connection.cursor()
        cur.execute("insert into db_userreg (first_name,last_name,address,contact,email,password)values(%s,%s,%s,%s,%s,%s)",(first_name, last_name, address, contact, email, password))
        mysql.connection.commit()
        cur.close()
        flash("Suceessfulyy registered")
        return redirect('userlogin')
    return render_template('user_register.html')


@app.route('/cart')
def cart():
    if 'cart' not in session:
        session['cart'] = []

    cart_items = []
    total = 0

    cur = mysql.connection.cursor()

    for pid in session['cart']:
        cur.execute("SELECT * FROM db_addproduct WHERE id=%s", (pid,))
        product = cur.fetchone()

        if product:
            cart_items.append(product)
            total += float(product[3])   # product_price column

    cur.close()

    return render_template(
        'cart.html',
        cart_items=cart_items,
        total=total
    )
@app.route('/add_to_cart/<int:p_id>')
def add_to_cart(p_id):

    if 'email' not in session:
        flash("Please Login First!")
        return redirect(url_for('userlogin'))

    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(p_id)
    session.modified = True

    flash("Product Added To Cart!")

    return redirect(request.referrer)  
@app.route('/checkout')
def checkout():

    if 'cart' not in session:
        session['cart'] = []

    original_total = 0
    discount_total = 0

    cur = mysql.connection.cursor()

    for pid in session['cart']:

        cur.execute(
            "SELECT * FROM db_addproduct WHERE id=%s",
            (pid,)
        )

        product = cur.fetchone()

        if product:

            price = float(product[3])

            discount = float(product[6])

            original_total += price

            discount_total += (price * discount) / 100

    cur.close()

    total = original_total - discount_total

    return render_template(
        'checkout.html',
        original_total=original_total,
        discount_total=discount_total,
        total=total
    )
@app.route('/buy_now/<int:p_id>')
def buy_now(p_id):

    session['direct_buy'] = p_id

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM db_addproduct WHERE id=%s",
        (p_id,)
    )

    product = cur.fetchone()

    cur.close()

    original_total = float(product[3])

    discount = float(product[6])

    discount_total = (original_total * discount) / 100

    total = original_total - discount_total

    return render_template(
        'checkout.html',
        original_total=original_total,
        discount_total=discount_total,
        total=total
    )
@app.route('/your_orders')
def your_orders():

    if 'orders' not in session:
        session['orders'] = []

    orders = []

    cur = mysql.connection.cursor()

    for pid in session['orders']:

        cur.execute(
            "SELECT * FROM db_addproduct WHERE id=%s",
            (pid,)
        )

        product = cur.fetchone()

        if product:
            orders.append(product)

    cur.close()

    return render_template(
        'your_orders.html',
        orders=orders
    )

@app.route('/cancel_order/<int:p_id>')
def cancel_order(p_id):

    if 'orders' in session:

        if p_id in session['orders']:
            session['orders'].remove(p_id)

        session.modified = True

    flash("Order Cancelled Successfully!")

    return redirect(url_for('your_orders'))

@app.route('/remove_from_cart/<int:p_id>')
def remove_from_cart(p_id):

    if 'cart' in session:

        if p_id in session['cart']:
            session['cart'].remove(p_id)

        session.modified = True

    flash("Product Removed Successfully!")

    return redirect(url_for('your_orders'))

@app.route('/place_order')
def place_order():

    if 'orders' not in session:
        session['orders'] = []

    # Direct Buy
    if 'direct_buy' in session:

        session['orders'].append(
            session['direct_buy']
        )

        session.pop('direct_buy')

    # Cart Checkout
    elif 'cart' in session:

        for pid in session['cart']:

            session['orders'].append(pid)

        session['cart'] = []

    session.modified = True

    flash("🎉 Order Placed Successfully!")

    return redirect(url_for('your_orders'))

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about_admin')
def about_admin():
    return render_template('about_admin.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    return redirect('/')
app.config['MYSQL_DB']='SportiGo'
app.config['SECRET_KEY']='secret'


if __name__=='__main__':
    app.run(debug=True)