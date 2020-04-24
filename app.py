import os
from os import path
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect, request, url_for, session, flash
from forms import LoginForm
import bcrypt

if path.exists('env.py'):
    import env

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config["MONGO_DBNAME"] = os.environ.get('MONGO_DBNAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)

# Route for index
@app.route('/')
@app.route('/index')
def index():
    skills = mongo.db.skills.find()
    return render_template('pages/index.html', skills=skills)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})
        if existing_user:
            if request.form['password'] == existing_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            else:
                flash('Login Unsuccessful. Please check username and password',
                      'success')
        else:
            flash('Login Unsuccessful. Please check username and password',
                  'success')

    return render_template('pages/login.html', form=form)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=(os.environ.get('PORT')),
            debug=True)
