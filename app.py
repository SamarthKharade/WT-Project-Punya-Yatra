from logging import exception
from flask import Flask, redirect, render_template,request, session, url_for
import mysql.connector # type: ignore
import json

app = Flask(__name__)

app.secret_key = 'punya_yatra_2025_flask_secret'
db = None
cursor = None
# Database connection function (chainge your connection credencial before running)
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
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
@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            session['username'] = username # Store username in session
            return redirect(url_for('home'))
        else:
            return "Invalid username or password!"

    return render_template('login.html')

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

    print(name,password)

    try:
        query= "INSERT INTO users (name, gender, age, countrycode, mobile, email, address, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
 
   
   
        cursor.execute(query,(name,gender,age,countrycode,mobile,email,address,username,password))
        db.commit()
       # return "User registered successfully!"
        return redirect(url_for('login'))
    except Exception as e:
        return "Username already exists!"
    finally:
        cursor.close()

  else:
    return render_template('signup.html')

    

# Route to hotel
@app.route('/hotel')
def hotel():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('hotels.html')

# Route to hotel booking
@app.route('/hotelBooking')
def hotelBooking():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('hotelBooking.html')

# Route to Restaurant 
@app.route('/restaurant')
def restaurant():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('restaurant2.html')

# Route to transport
@app.route('/transport')
def transport():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# Route to Restaurant Booking
@app.route('/restaurantBooking',methods=['GET', 'POST'])
def restaurantBooking():
     if 'username' not in session:
        return redirect(url_for('login'))
     
     if request.method == 'POST':
        name2 = request.form['customerName']
        date_of_booking = request.form['date']
        time_of_booking = request.form['bookingTime']
        total_people = request.form['numPeople']
        total_table = request.form['numTables']

        try:
            query= "INSERT INTO restaurant_booking (name, date_of_booking, time_of_booking,total_people ,total_table) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query,(name2,date_of_booking,time_of_booking,total_people,total_table))
            db.commit()
        
           
            return redirect(url_for('restaurant'))
        except mysql.connector.Error as err:
            return f"Error: {err}"
        
     else:
       return render_template('booking.html')

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
    with open('places.json', 'r') as f:
        places = json.load(f)

    # Find the place with the matching ID
    place = next((p for p in places if p['id'] == place_id), None)

    if not place:
        return "Place not found!"

    return render_template('blogTemp.html', place=place)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

