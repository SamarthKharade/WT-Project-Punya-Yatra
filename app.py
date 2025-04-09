from flask import Flask, render_template,request

app = Flask(__name__)

# Route to main page 
@app.route('/')
def home():
    return render_template('index2.html')

# Route to login page
@app.route('/login')
def login():
    return render_template('login.html')

# Route to signup page
@app.route('/signup')
def signup():
    return render_template('signUp.html')

# Route to hotel
@app.route('/hotel')
def hotel():
    return render_template('hotels.html')

# Route to hotel booking
@app.route('/hotelBooking')
def hotelBooking():
    return render_template('hotelBooking.html')

# Route to Restaurant 
@app.route('/restaurant')
def restaurant():
    return render_template('restaurant2.html')

# Route to transport
@app.route('/transport')
def transport():
    return render_template('index.html')

# Route to Restaurant Booking
@app.route('/restaurantBooking')
def restaurantBooking():
    return render_template('booking.html')

@app.route('/results')
def results():
    transport_type = request.args.get('transportType')
    from_location = request.args.get('from')
    to_location = request.args.get('to')
    date = request.args.get('date')

    return render_template('results.html', transport_type=transport_type, from_location=from_location, to_location=to_location, date=date)


app.run(debug=True)