'''import joblib
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Home_1.html')

@app.route('/Predict')
def prediction():
    return render_template('Index.html')


@app.route('/form', methods=["POST"])
def brain():
    Nitrogen=float(request.form['Nitrogen'])
    Phosphorus=float(request.form['Phosphorus'])
    Potassium=float(request.form['Potassium'])
    Temperature=float(request.form['Temperature'])
    Humidity=float(request.form['Humidity'])
    Ph=float(request.form['ph'])
    Rainfall=float(request.form['Rainfall'])
     
    values=[Nitrogen,Phosphorus,Potassium,Temperature,Humidity,Ph,Rainfall]
    
    if Ph>0 and Ph<=14 and Temperature<100 and Humidity>0:
        joblib.load('C:\\Users\91721\\Downloads\\Crop-Recommendation-system--main\\Crop recommendation system\\crop_app\\crop_app','r')
        model = joblib.load(open('C:\\Users\\91721\\Downloads\\Crop-Recommendation-system--main\\Crop recommendation system\\crop_app\\crop_app','rb'))
        

        arr = [values]
        acc = model.predict(arr)
        print(acc)
        return render_template('prediction.html', prediction=str(acc))
    else:
        return "Sorry...  Error in entered values in the form Please check the values and fill it again"

@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
    #old code..................!!!**********!!!................
'''
'''
from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
import joblib

app = Flask(__name__)
app.secret_key = 'gwil psbz xpnn xgln'

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ganeshsalke02@gmail.com'
app.config['MAIL_PASSWORD'] = 'gwil psbz xpnn xgln'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail .com'

mail = Mail(app)

@app.route('/')
def home():
    return render_template('Home_1.html')

@app.route('/Predict')
def prediction():
    return render_template('Index.html')
##rendering the templete of the page of data
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')
#############################################################

@app.route('/form', methods=["POST"])
def brain():
    Nitrogen = float(request.form['Nitrogen'])
    Phosphorus = float(request.form['Phosphorus'])
    Potassium = float(request.form['Potassium'])
    Temperature = float(request.form['Temperature'])
    Humidity = float(request.form['Humidity'])
    Ph = float(request.form['ph'])
    Rainfall = float(request.form['Rainfall'])
    
    values = [Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Ph, Rainfall]
    
    if 0 < Ph <= 14 and Temperature < 100 and Humidity > 0:
        model = joblib.load('C:\\Users\\91721\\Downloads\\Crop-Recommendation-system--main\\Crop recommendation system\\crop_app\\crop_app')
        arr = [values]
        acc = model.predict(arr)
        return render_template('prediction.html', prediction=str(acc))
    else:
        flash("Error in entered values in the form. Please check the values and fill it again.")
        return redirect('/Predict')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        msg = Message('Contact Form Submission', 
                      recipients=['ganeshsalke02@gmail.com'])
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        mail.send(msg)
        
        flash("Your message has been sent successfully.")
        return redirect('/contact')
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

'''
#2nd code

'''
from flask import Flask, render_template, request, redirect, flash,session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import joblib


app = Flask(__name__)
app.secret_key = 'gwil psbz xpnn xgln'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()


# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ganeshsalke02@gmail.com'
app.config['MAIL_PASSWORD'] = 'gwil psbz xpnn xgln'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail .com'

mail = Mail(app)

@app.route('/')
def home():
    return render_template('Home_1.html')

@app.route('/Predict')
def prediction():
    return render_template('Index.html')
##rendering the templete of the page of data
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/Home_1.html')
        else:
            return render_template('login.html',error='Invalid user')

    return render_template('login.html')


@app.route('/Home_1')
def Home_1():
    if session['name']:
        return render_template('Home_1.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


@app.route('/form', methods=["POST"])
def brain():
    Nitrogen = float(request.form['Nitrogen'])
    Phosphorus = float(request.form['Phosphorus'])
    Potassium = float(request.form['Potassium'])
    Temperature = float(request.form['Temperature'])
    Humidity = float(request.form['Humidity'])
    Ph = float(request.form['ph'])
    Rainfall = float(request.form['Rainfall'])
    
    values = [Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Ph, Rainfall]
    
    if 0 < Ph <= 14 and Temperature < 100 and Humidity > 0:
        model = joblib.load('C:\\Users\\91721\\Downloads\\Crop-Recommendation-system--main\\Crop recommendation system\\crop_app\\crop_app')
        arr = [values]
        acc = model.predict(arr)
        return render_template('prediction.html', prediction=str(acc))
    else:
        flash("Error in entered values in the form. Please check the values and fill it again.")
        return redirect('/Predict')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        msg = Message('Contact Form Submission', 
                      recipients=['ganeshsalke02@gmail.com'])
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        mail.send(msg)
        
        flash("Your message has been sent successfully.")
        return redirect('/contact')
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

'''
#2nd code
from flask import Flask, render_template, request, redirect, flash, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import joblib

app = Flask(__name__)
app.secret_key = 'gwil psbz xpnn xgln'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ganeshsalke02@gmail.com'
app.config['MAIL_PASSWORD'] = 'gwil psbz xpnn xgln'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'

mail = Mail(app)

@app.route('/')
def index():
    if 'email' in session:
        return redirect('/home')
    return redirect('/login')

@app.route('/home')
def home():
    if 'email' in session:
        return render_template('Home_1.html')
    else:
        return redirect('/login')

@app.route('/Predict')
def prediction():
    return render_template('Index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/home')
        else:
            return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/form', methods=["POST"])
def brain():
    Nitrogen = float(request.form['Nitrogen'])
    Phosphorus = float(request.form['Phosphorus'])
    Potassium = float(request.form['Potassium'])
    Temperature = float(request.form['Temperature'])
    Humidity = float(request.form['Humidity'])
    Ph = float(request.form['ph'])
    Rainfall = float(request.form['Rainfall'])
    
    values = [Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Ph, Rainfall]
    
    if 0 < Ph <= 14 and Temperature < 100 and Humidity > 0:
        model = joblib.load('C:\\Users\\91721\\Downloads\\Crop-Recommendation-system--main\\Crop recommendation system\\crop_app\\crop_app')
        arr = [values]
        acc = model.predict(arr)
        return render_template('prediction.html', prediction=str(acc))
    else:
        flash("Error in entered values in the form. Please check the values and fill it again.")
        return redirect('/Predict')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        msg = Message('Contact Form Submission', recipients=['ganeshsalke02@gmail.com'])
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        mail.send(msg)
        
        flash("Your message has been sent successfully.")
        return redirect('/contact')
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
