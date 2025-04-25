import os
from datetime import datetime
from logging import exception
from flask import Flask, redirect, render_template,request, session, url_for
import mysql.connector # type: ignore
import json
import bcrypt
from mysql.connector import Error # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message


app = Flask(__name__)

app.secret_key = 'punya_yatra_2025_flask_secret'

# Configure Flask-Mail directly in code
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'kharadesamarth64@gmail.com'         
app.config['MAIL_PASSWORD'] = 'vecx mitg irjn isps'               
app.config['MAIL_DEFAULT_SENDER'] = 'kharadesamarth64@gmail.com'      

mail = Mail(app)

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
        user_email = email
        
     
            

    # Email content
        subject = f"Welcome to Punya Yatra!"
        body = f"""Dear {name},

Thank you for registering with Punya Yatra - Your Complete Pilgrimage Planner...

We are delighted to help you to plan your spiritual journey...

1. Book Darshan Passes for temples across Maharashtra  
2.Reserve comfortable Hotels near your pilgrimage site  
3.Find and book nearby Restaurants offering authentic cuisine  
4.Plan and manage your Travel with reliable transport services


Punya Yatra is here to take care of every detail, so you can focus solely on your devotion.

Let your pilgrimage be as divine as your faith...

Jai Jai Ram Krishna Hari !


Warm regards,  
Team Punya Yatra

"""

    # Send email
        msg = Message(subject=subject, recipients=[user_email], body=body)
        mail.send(msg)
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


@app.route('/search_results', methods=['GET'])
def search_results():



    source = request.args.get('from')
    destination = request.args.get('to')
    transport_type = request.args.get('transportType')

    if not source or not destination or not transport_type:
        return "Please provide all search parameters.", 400

        
    

    cursor = db.cursor(dictionary=True)

    
    query = """
        SELECT * FROM travel 
        WHERE SourcePlace = %s AND DestinationPlace = %s AND TravelType = %s
    """
    cursor.execute(query, (source, destination, transport_type))
    results = cursor.fetchall()

    return render_template('results.html', results=results, source=source, destination=destination, transport_type=transport_type)

@app.route('/darshan', methods=['GET'])
def darshan():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('darshan_pass.html')

@app.route('/darshanbooking', methods=['GET', 'POST'])
def darshanbooking():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        temple = request.form['temple']
        name= request.form['name']
       
        email= request.form['email']
        people= request.form['people']
        price= request.form['totalFare']
        date= request.form['date']


     

        try:
            query= "INSERT INTO darshanpassinfo (Temple_Name,Person_name,Email,People,Amount,PassDate) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(query,(temple,name,email,people,price,date))
            db.commit()

              # Simulate booking task
            user_email = email
            temple_name = temple 
            visit_date = date
            

    # Email content
            subject = f"Darshan Pass Confirmation - {temple_name}"
            body = f"""Dear {name},

Your Darshan Pass booking for {temple_name} on {visit_date} has been successfully confirmed...

Date of Visit : {visit_date}
Number of People : {people}
Total Amount : {price} INR

Please carry this email on the day of your visit...

Thank you for using Punya Yatra !
Wishing you a peaceful and blessed darshan...

Regards,  
Punya Yatra Team
"""

    # Send email
            msg = Message(subject=subject, recipients=[user_email], body=body)
            mail.send(msg)
            return redirect(url_for('home'))
        
        except mysql.connector.Error as err:
            return f"Error: {err}"
        

@app.route('/send_email', methods=['POST'])
def send_email():
    # Simulate booking task
    user_email = 'kharadesamarth2004@gmail.com' 
    temple_name = "Swami Samarth Temple"  
    visit_date = "2025-05-01"

    # Email content
    subject = f"Temple Booking Confirmation - {temple_name}"
    body = f"""Dear Devotee,

Your booking for {temple_name} on {visit_date} is confirmed.

Thank you for using Punya Yatra!
Swami Om !!! 
"""

    # Send email
    msg = Message(subject=subject, recipients=[user_email], body=body)
    mail.send(msg)

    return f"Confirmation email sent to {user_email}!"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
