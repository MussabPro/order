from flask import Flask, render_template, request, redirect,url_for, session, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from config import ADMIN_USERNAME, ADMIN_PASSWORD, Config
import re
import string
import random

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DataBase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def generate_order_number():
    characters = string.digits  # You can include additional characters if needed
    order_number = ''.join(random.choices(characters, k=4))
    return order_number


class Gig(db.Model):
    __tablename__ = 'gig'
    no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    info = db.Column(db.String(10000), nullable=False)
    UpAcc = db.Column(db.String(3), nullable=False)
    NatureOfWork = db.Column(db.String(100), nullable=False)
    Cost = db.Column(db.String(50), nullable=False)
    Status = db.Column(db.String(100), nullable=False, default="Ordered")
    DateCreated = db.Column(db.String(80), default=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    DateCompleted = db.Column(db.String(80))
    OrderNumber = db.Column(db.String(10))

    def __repr__(self) -> str:
        return f"{self.no}-{self.name}-{self.email}-{self.UpAcc}-{self.NatureOfWork}-{self.Status}-{self.DateCompleted}"


@app.before_request
def check_if_logged_in():
    if (
        not request.path.startswith('/admin') and
        not request.path.startswith('/delete') and
        not request.path.startswith('/change') and
        'logged_in' in session
    ):
        session.pop('logged_in', None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Validate the username and password
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect('/admin')
        else:
            return render_template('login.html', error='Invalid User Name or Password')
    return render_template('login.html')
@app.route('/Home', methods=["GET", "POST"])
def home():
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M')
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        info = request.form['info']
        selected_services = request.form.getlist('selected_services[]')
        cost = request.form.get('costInput')

        for service in selected_services:
            match = re.search(r'\((\d+\.\d+)\$\/hr\)', service)
            if match:
                rate = float(match.group(1))
                cost += rate
        Cost = str(cost) + "$/hr"

        UpAcc = request.form.get('upacc')
        NatureOfWork = ', '.join(selected_services) if selected_services else ""
        DateCompleted = request.form['datec']
        # Generate an order number
        order_number = generate_order_number()
        # Store the order number in the session
        session['order_number'] = order_number

        gig = Gig(name=name, email=email, info=info, UpAcc=UpAcc, NatureOfWork=NatureOfWork,
                  DateCompleted=DateCompleted, Cost=Cost, OrderNumber=order_number)
        db.session.add(gig)
        db.session.commit()

        return render_template('OrderComplete.html', URL=url_for('home'), order_number=order_number, gig=gig)
    else:
        return render_template('index.html', current_time=current_time)



@app.route('/order-complete/<order_number>')
def order_complete(order_number):
    gig = Gig.query.filter_by(OrderNumber=order_number).first()
    return render_template('OrderComplete.html', order_number=order_number,gig=gig)

@app.route('/Status', methods=['GET', 'POST'])
def status():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        OrderNumber = request.form['Order_number']
        gigs = Gig.query.all()
        order_number = None  # Assign a default value
        Error = True  # Assign a default value
        for gig in gigs:
            if name == gig.name and email == gig.email:
                if OrderNumber == gig.OrderNumber:
                    order_number = OrderNumber
                    Error = False
                    break  # Exit the loop since a match is found
        if Error:
            return render_template('CheckStatus.html', Error=Error)
        else:
            gig = Gig.query.filter_by(OrderNumber=order_number).first()
            return render_template('OrderComplete.html',URL=request.referrer ,order_number=order_number,gig=gig)

    return render_template('CheckStatus.html')
    

@app.route('/print/<order_number>')
def PrintReceipt(order_number):
    gig = Gig.query.filter_by(OrderNumber=order_number).first()
    # Date completed
    input_datecom_str = getattr(gig, 'DateCompleted')  # or gig.DateCompleted
    input_datecom = datetime.strptime(input_datecom_str, "%Y-%m-%dT%H:%M")
    output_datecom_str = input_datecom.strftime("%d-%m-%Y %I:%M:%S %p")
    # Date created
    input_datecre_str = getattr(gig, 'DateCreated')  # or gig.DateCompleted
    input_datecre = datetime.strptime(input_datecre_str, "%Y-%m-%d %H:%M:%S")
    output_datecre_str = input_datecre.strftime("%d-%m-%Y %I:%M:%S %p")
    return render_template('Print.html',gig=gig,datecom=output_datecom_str,datecre=output_datecre_str)

@app.route('/admin/', methods=["GET", "POST"])
def admin():
    if session.get('logged_in'):
        # Update last activity time
        session['last_activity_time'] = datetime.now().timestamp()
        allgig = Gig.query.all()
        formatted_gigs = []
        for gig in allgig:
            input_datecom_str = getattr(gig, 'DateCompleted')  # or gig.DateCompleted
            input_datecom = datetime.strptime(input_datecom_str, "%Y-%m-%dT%H:%M")
            output_datecom_str = input_datecom.strftime("%d-%m-%Y %I:%M:%S %p")
            gig.datecom = output_datecom_str

            input_datecre_str = getattr(gig, 'DateCreated')  # or gig.DateCreated
            input_datecre = datetime.strptime(input_datecre_str, "%Y-%m-%d %H:%M:%S")
            output_datecre_str = input_datecre.strftime("%d-%m-%Y %I:%M:%S %p")
            gig.datecre = output_datecre_str

            formatted_gigs.append(gig)
        return render_template("admin.html", allgig=formatted_gigs)
    else:
        return redirect('/login')
    
@app.route('/delete/<int:no>')
def delete(no):
      if session.get('logged_in'):
        gig = Gig.query.filter_by(no=no).first()
        db.session.delete(gig)
        db.session.commit()
      return redirect('/admin/')


@app.route('/change/<int:no>', methods=["GET", "POST"])
def change(no):
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        info = request.form['info']
        UpAcc = request.form['upacc']
        NatureOfWork = request.form['services']
        Status = request.form['status']
        Cost = request.form['cost']
        DateCompleted = request.form['datec']
        gig = Gig.query.filter_by(no=no).first()
        gig.name = name
        gig.email = email
        gig.info = info
        gig.UpAcc = UpAcc
        gig.Status = Status
        gig.NatureOfWork = NatureOfWork
        gig.Cost = Cost
        gig.DateCompleted = DateCompleted
        db.session.add(gig)
        db.session.commit()
        return redirect('/admin/')
    gig = Gig.query.filter_by(no=no).first()
    return render_template("change.html", gig=gig)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)
