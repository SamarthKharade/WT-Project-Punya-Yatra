import os
from datetime import datetime
from logging import exception
from flask import Flask, redirect, render_template,request, session, url_for
import mysql.connector # type: ignore
import json
import bcrypt
from mysql.connector import Error # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.secret_key = 'punya_yatra_2025_flask_secret'

# Database connection function (chainge your connection credencial before running)
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Samarth@2004",
        database="punyayatra",
        auth_plugin='mysql_native_password',
        port=3306
    )
   
    cursor = db.cursor()

    print("Database connected successfully!")
except Exception as e:
    print("Database not connected!!!")
    print("Error:", e)


# Route to main page 
@app.route('/')
def home():
    username = session.get('username')  # Check if user is logged in
    return render_template('index2.html', username=username)
# Route to login page

@app.route('/login',methods=['GET','POST'])
def login():
    error_message = None  # default to no message

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor2 = db.cursor()
        query = "SELECT password FROM users WHERE username = %s"
        cursor2.execute(query, (username,))
        user = cursor2.fetchone()
        #and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8'))
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error_message = "Invalid username or password!"

    return render_template('login.html', error_message=error_message)

# Route to signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():

  if request.method == 'POST':
    cursor = db.cursor()
    name = request.form['name']
    gender = request.form['gender']
    age = request.form['age']
    countrycode = request.form['countrycode']
    mobile = request.form['mobile']
    email = request.form['email']
    address = request.form['address']
    username = request.form['username']
    password = request.form['password']

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    print(name,password)

    try:
        query= "INSERT INTO users (name, gender, age, countrycode, mobile, email, address, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
 
   
   
        cursor.execute(query,(name,gender,age,countrycode,mobile,email,address,username,hashed_password))
        db.commit()
       # return "User registered successfully!"
        return redirect(url_for('login'))
    except Exception as e:
        return str(e)
    finally:
        cursor.close()

  else:
    return render_template('signup.html')

    

# Route to hotel
@app.route('/hotel',methods=['GET', 'POST'])
def hotel():
    if 'username' not in session:
        return redirect(url_for('login'))
   
    if request.method == 'GET':
        name = request.args.get('name', '')
        location = request.args.get('location', '')
        return render_template('hotelBooking.html', name=name, location=location)
    else:
        return render_template('hotels.html')


@app.route('/hotelinfo')
def hotelinfo():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('hotels.html')

# Route to hotel booking

@app.route('/userbookinghotel', methods=['GET', 'POST'])
def userbookinghotel():
    if 'username' not in session:
        return redirect(url_for('login'))
    bookings = []

    if request.method == 'GET':
        # Get the username from the query parameters
        username = request.args.get('username')
        
        if username:
            try:
                # Fetch user-specific bookings from the database
                cursor = db.cursor(dictionary=True)
                cursor.execute("SELECT * FROM hotel_booking WHERE name = %s", (username,))
                bookings = cursor.fetchall()

            except mysql.connector.Error as err:
                print(f"Error: {err}")
            
            # Render the template with the bookings for the username
            return render_template('hotel_user_booking.html', bookings=bookings, username=username)

        else:
            # If no username is provided, return an error or redirect
            return "No username provided", 400

    elif request.method == 'POST':
        # Here, you can handle the POST request, such as adding new bookings or processing a form submission
        # For now, redirecting to the restaurant booking page (restaurant2.html)
        return render_template('hotel.html')


# Route to hotel booking
@app.route('/hotelBooking',methods=['GET', 'POST'])
def hotelBooking():
     if 'username' not in session:
        return redirect(url_for('login'))
     if request.method == 'POST':
        # Get form data
        name = request.form['customerName']
        hname = request.form['hotelName']
        location = request.form['location']
        email= request.form['emailID']

        room_type = request.form['roomType']
        ac_type = request.form['acType']
        total_people = request.form['numPeople']
        total_room = request.form['numTables']
        reporting_date = request.form['date']
        reporting_time = request.form['bookingTime']
        exit_date = request.form['exitdate']
        exit_time = request.form['exittime']

        try:
            query = """INSERT INTO hotel_booking 
                       (name,hotel_name,hotel_location,email,room_type, ac_type, total_people, total_room, 
                        reporting_date, reporting_time, exit_date, exit_time)
                       VALUES (%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query,(name,hname,location,email, room_type, ac_type, total_people, total_room,
                                   reporting_date, reporting_time, exit_date, exit_time))
            db.commit()

            return redirect(url_for('hotelinfo'))  # Assuming you have a 'hotel' route
        except mysql.connector.Error as err:
            return f"Error: {err}"

     else:
        return render_template('hotelbooking.html, name=rname, location=location)')


@app.route('/restaurantinfo')
def restaurantinfo():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('restaurant2.html')


# Restaurant Search and Booking Page
@app.route('/restaurant', methods=['GET', 'POST'])
def restaurant():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        name = request.args.get('name', '')
        location = request.args.get('location', '')
        return render_template('booking.html', name=name, location=location)
    else:
        return render_template('restaurant2.html')
    

@app.route('/userbookingrestaurant', methods=['GET', 'POST'])
def userbookingrestaurant():
    if 'username' not in session:
        return redirect(url_for('login'))
    bookings = []

    if request.method == 'GET':
        # Get the username from the query parameters
        username = request.args.get('username')
        
        if username:
            try:
                # Fetch user-specific bookings from the database
                cursor = db.cursor(dictionary=True)
                cursor.execute("SELECT * FROM restaurant_booking WHERE name = %s", (username,))
                bookings = cursor.fetchall()

            except mysql.connector.Error as err:
                print(f"Error: {err}")
            
            # Render the template with the bookings for the username
            return render_template('restaurant_user_booking.html', bookings=bookings, username=username)

        else:
            # If no username is provided, return an error or redirect
            return "No username provided", 400

    elif request.method == 'POST':
        # Here, you can handle the POST request, such as adding new bookings or processing a form submission
        # For now, redirecting to the restaurant booking page (restaurant2.html)
        return render_template('restaurant2.html')


# Route to Restaurant Booking
@app.route('/restaurantBooking',methods=['GET', 'POST'])
def restaurantBooking():
     if 'username' not in session:
        return redirect(url_for('login'))

     if request.method == 'POST':
        name2 = request.form['customerName']
        rname= request.form['restaurantName']
        email= request.form['emailID']
        location = request.form['location']
        date_of_booking = request.form['date']
        time_of_booking = request.form['bookingTime']
        total_people = request.form['numPeople']
        total_table = request.form['numTables']

        try:
            query= "INSERT INTO restaurant_booking (name,restaurant_name,restaurant_location,email, date_of_booking, time_of_booking,total_people ,total_table) VALUES (%s, %s,%s,%s,%s, %s, %s, %s)"
            cursor.execute(query,(name2,rname,location,email,date_of_booking,time_of_booking,total_people,total_table))
            db.commit()
        
           
            return redirect(url_for('restaurantinfo'))
        except mysql.connector.Error as err:
            return f"Error: {err}"
        
     else:
       return render_template('booking.html')
     
# Route to transport
@app.route('/transport')
def transport():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')





@app.route('/results')
def results():
    if 'username' not in session:
        return redirect(url_for('login'))
    transport_type = request.args.get('transportType')
    from_location = request.args.get('from')
    to_location = request.args.get('to')
    date = request.args.get('date')

    return render_template('results.html', transport_type=transport_type, from_location=from_location, to_location=to_location, date=date)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT name, gender, age, countrycode, mobile, email, address, username FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return render_template('profile.html', user=user)
    else:
        return "User not found!"



@app.route('/blog/<int:place_id>')
def blog(place_id):
    try:
        file_path = os.path.join(app.root_path, 'static', 'json', 'temples.json')
        with open(file_path, 'r') as f:
            places = json.load(f)
            place = next((p for p in places if p['id'] == place_id), None)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return f"Error loading data: {e}", 500

    if not place:
        return "Place not found!", 404

    return render_template('blogTemp.html', place=place)


@app.route('/payment', methods=['GET'])
def payment():
    service = request.args.get('service')  # gets from ?service=...
    amount = request.args.get('amount')    # gets from ?amount=...

    # Render the payment page with this info
    return render_template('payment.html', service=service, amount=amount)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
