from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY']='4b4d81f7ef1fd0e05b738dbe9cd924f5'
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/hom")
def hom():
    return render_template('hom.html')

@app.route("/signup")
def register():
    form=RegistrationForm()
    return render_template('signup.html',title='Sign up',form=form)

@app.route("/login")
def login():
    form=LoginForm()
    return render_template("login.html", title='login', form=form)

if __name__=='__main__':
    app.run()

