import streamlit as st
#from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
from tabulate import tabulate

con = mysql.connector.connect(host="localhost", user="root", password="root", database="xyz")
res = con.cursor()

def product():
    st.title("Available Products")
    sql = "SELECT * FROM product_details"
    res.execute(sql)
    result = res.fetchall()
    st.text(tabulate(result, headers=["product_id", "product_name", "quantity", "price"], tablefmt="fancy_grid"))
    
def emp_update_product():
    def add_product():
        st.subheader("Add Product")
        qry = "SELECT MAX(product_id) FROM product_details"
        res.execute(qry)
        max_product_id = res.fetchone()[0]
        if max_product_id is None:
            product_id = 100
        else:
            product_id = max_product_id + 1
        product_id = st.text_input("Product Id", product_id) 
        product_name = st.text_input("Product Name")
        quantity = st.number_input("Quantity", value=1)
        price = st.number_input("Price")
        if st.button("Add Product"):
            qry = "INSERT INTO product_details (product_id,product_name, quantity, price) VALUES (%s, %s, %s, %s)"
            product_data = (product_id,product_name, quantity, price)
            res.execute(qry, product_data)
            con.commit()
            st.success("Product added successfully")
    def delete_product():
        st.subheader("Delete Product")
        product_id = st.text_input("Product ID")
        if st.button("Delete Product"):
            qry = "DELETE FROM product_details WHERE product_id = %s"
            product_data = (product_id,)
            res.execute(qry, product_data)
            con.commit()
            st.success("Product deleted successfully")
    def update_quantity():
        st.subheader("Update Product Quantity")
        product_id = st.text_input("Product ID")
        new_quantity = st.number_input("New Quantity", value=1)
        if st.button("Update Quantity"):
            qry = "UPDATE product_details SET quantity = %s WHERE product_id = %s"
            product_data = (new_quantity, product_id)
            res.execute(qry, product_data)
            con.commit()
            st.success("Quantity updated successfully")
    with st.sidebar:
        options = ["Add Product", "Delete Product", "Update Quantity"]
        default_index = 0
        selected = option_menu(
           menu_title= "Product Management",
           options=options,
           icons=["Plus-circle-fill", "Trash", "Arrow-repeat"],
           menu_icon="cast",
           default_index=default_index,
        )
    if selected == "Add Product":
        add_product()
    elif selected == "Delete Product":
        delete_product()
    elif selected == "Update Quantity":
        update_quantity()
    else:
        pass

def orders():
    def new_booking():
        global order_id  
        
    qry = "SELECT MAX(order_id) FROM order_details"
    res.execute(qry)
    max_order_id = res.fetchone()[0]

    if max_order_id is None:
        order_id = 10000
    else:
        order_id = max_order_id + 1

    st.subheader("Book your order")
    order_id = st.text_input("Order Id", order_id)
    product_name = st.text_input("Product Name")
    ord_quantity = st.number_input("Quantity", value=1)
    price = 0

    if st.button("Book Now"):
        # Check if the product is available and has enough quantity
        qry = "SELECT price, quantity FROM product_details WHERE product_name = %s"
        res.execute(qry, (product_name,))
        product_data = res.fetchone()

        if product_data:
            price = product_data[0]
            available_quantity = product_data[1]

            if available_quantity >= ord_quantity:
                total_price = ord_quantity * price

                # Deduct the ordered quantity from product quantity
                updated_quantity = available_quantity - ord_quantity
                update_query = "UPDATE product_details SET quantity = %s WHERE product_name = %s"
                res.execute(update_query, (updated_quantity, product_name))

                qry = "INSERT INTO order_details (customer_id, order_id, product_name, quantity, price, total_price) VALUES (%s, %s, %s, %s, %s, %s)"
                product_data = (customer_id, order_id, product_name, ord_quantity, price, total_price)
                res.execute(qry, product_data)
                con.commit()
                st.text(f"Total Price: {total_price}")
                st.success("Your product has been successfully placed!")
            else:
                st.error("Not enough quantity available for the selected product.")
        else:
            st.error("Product not found or unavailable.")

    def view_booking():
        st.title("Your Order")
        customer_id = st.text_input("Enter your Customer ID:")
        if st.button("View My Orders"):
            sql = "SELECT * FROM order_details WHERE customer_id = %s"
            res.execute(sql, (customer_id,))
            results = res.fetchall()
            if results:
                st.subheader("Your Orders:")
                for order in results:
                    st.write(f"Order ID: {order[1]}\n Product: {order[2]}\n Quantity: {order[3]}\n Price: {order[4]}\n Total Price: {order[5]}\n")
            else:
                st.warning("No orders found for the provided customer ID.")

    def cancel_booking():
        global order_id  # Declare order_id as global
        st.subheader("Cancel Booking")
        customer_id = st.text_input("Enter your Customer ID:")
        order_id = st.text_input("Enter your Order ID:")
        if st.button("Cancel Booking"):
            qry = "SELECT * FROM order_details WHERE customer_id = %s AND order_id = %s"
            res.execute(qry, (customer_id, order_id))
            order_data = res.fetchone()
            if order_data:
                product_name = order_data[2]
                quantity = order_data[3]
                delete_query = "DELETE FROM order_details WHERE customer_id = %s AND order_id = %s"
                res.execute(delete_query, (customer_id, order_id))
                update_query = "UPDATE product_details SET quantity = quantity + %s WHERE product_name = %s"
                res.execute(update_query, (quantity, product_name))
                con.commit()
                st.success("Booking canceled successfully.")
            else:
                st.warning("No order found with the provided customer_id and order_id.")

    book_pro = st.sidebar.radio("BOOKING", ["New Booking", "View Booking", "Cancel Booking"])
    if book_pro == "New Booking":
        new_booking() 
    elif book_pro == "View Booking":
        view_booking()
    elif book_pro == "Cancel Booking":
        cancel_booking()  
    else:
        pass
            
    
st.header('COOL GADGETS')
pro = st.sidebar.radio("SignIn/Login",["SignIn", "Login"])
if pro == "SignIn":
    st.header("SIGN-IN")
    rad = st.radio("User",["Customer", "Employee"])
    if rad == "Customer":
        st.title("Customer SignIn")
        qry = "SELECT MAX(customer_id) FROM Customer"
        res.execute(qry)
        max_customer_id = res.fetchone()[0]
        if max_customer_id is None:
            customer_id = 100
        else:
            customer_id = max_customer_id + 1
        customer_id = st.text_input("Customer Id", customer_id) 
        first, last = st.columns(2)
        first_name = first.text_input("First Name")
        last_name = last.text_input("Last Name")
        mail, no = st.columns([3, 1])
        email_id = mail.text_input("Mail Id")
        phone_input = no.text_input("Mobile Number")
        phone_num = int(phone_input) if phone_input else None
        us, pw, pw1 = st.columns(3)
        user_name = us.text_input("User Name")
        user_password = pw.text_input("Password", type="password")
        user_password_reenter = pw1.text_input("Reenter the Password", type="password")
        button = st.button("Submit")
        if button:
            if user_password == user_password_reenter:
                qry = "INSERT INTO Customer (customer_id, first_name, last_name, email_id, phone_num, user_name, user_password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                user = (customer_id, first_name, last_name, email_id, phone_num, user_name, user_password)
                res.execute(qry, user)
                con.commit()
                st.success("Register successful!")
                st.balloons()
            else:
                st.error("Passwords do not match")
        booking_order = orders()
        st.write(booking_order)
                
    elif rad == "Employee":
        st.header("Employee SignIn")
        qry = "SELECT MAX(emp_id) FROM employee_details"
        res.execute(qry)
        max_emp_id = res.fetchone()[0]
        if max_emp_id is None:
            emp_id = 1000
        else:
            emp_id = max_emp_id + 1
        emp_id = st.text_input("Employee Id", emp_id) 
        first, last = st.columns(2)
        first_name = first.text_input("First Name")
        last_name = last.text_input("Last Name")
        mail, no = st.columns([3, 1])
        email_id = mail.text_input("Mail Id")

        phone_input = no.text_input("Mobile Number")
        phone_num = int(phone_input) if phone_input else None
        en, epw, epw1 = st.columns(3)
        emp_name = en.text_input("Emp User Name")
        emp_password = epw.text_input("Password", type="password")
        emp_password_reenter = epw1.text_input("Reenter the Password", type="password")
        button = st.button("Submit")
        if button:
            if emp_password == emp_password_reenter:
                qry = "INSERT INTO employee_details (emp_id,emp_first_name, emp_last_name, emp_email_id, emp_phone_num, emp_name, emp_password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                user = (emp_id,first_name, last_name, email_id, phone_num, emp_name, emp_password)
                res.execute(qry, user)
                con.commit()
                st.success("Register successful!")
                st.balloons()
            else:
                st.error("Passwords do not match")
                
                
elif pro == "Login":
    st.header("LOGIN-IN")
    rad = st.radio("User",["Customer", "Employee"])
    if rad == "Customer":
        st.title(" Customer Login")
        cursor = con.cursor()
        us,pw1 = st.columns(2)
        user_name = us.text_input("User name")
        user_password = pw1.text_input("Password", type="password")
        login_query = "SELECT * FROM Customer WHERE user_name = %s AND user_password = %s"
        user_data = (user_name, user_password)
        cursor.execute(login_query, user_data)
        result = cursor.fetchone()
        button = st.button("Login")
        if button:
            if result:
                st.success("Login successful!")
                st.balloons()
            else:
                st.error("Invalid ")
                
    elif rad == "Employee":
        st.header("Employee Login")
        cursor = con.cursor()
        us,pw1 = st.columns(2)
        emp_name = us.text_input("Emp ID")
        emp_password = pw1.text_input("Password", type="password")
        login_query = "SELECT * FROM employee_details WHERE emp_name = %s AND emp_password = %s"
        user_data = (emp_name, emp_password)
        cursor.execute(login_query, user_data)
        result = cursor.fetchone()
        button = st.button("Login")
        if button:
            if result:
                st.success("Login successful!")
                st.balloons()
            else:
                st.error("Invalid ")
        
        st.title("Update Product")
        update_product = emp_update_product()
        st.write(update_product)

else:
    pass

products = product()
st.write(products)



con.close()