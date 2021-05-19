from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# redirect to the login/registration form
@app.route("/")
def index():
    if "logged_in" in session:
        return redirect("/success")

    return render_template("index.html")


# Login and registration routes
@app.route("/register", methods = ["POST"])
def register():
    # Verify the inputs - if invalid input, redirect to the form and tell the user what they did wrong
    if not User.valid_registration(request.form):
        return redirect("/")

    # If the input is valid, hash the password and store the hashed password in the database
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    # if the data is valid, create the user
    user_id = User.create_user(data) 

    session["logged_in"] = user_id

    return redirect("/success")


@app.route("/login", methods = ["POST"])
def login():
    # if user is not registered in the db
    if not User.valid_login(request.form):
        return redirect("/")

    #otherwise look up the user by their email
    user = User.get_by_email({"email": request.form['email']})

    # if we get False after checking the password
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')

    # if the passwords matched, we set the user_id into session
    session["logged_in"] = user.id

    # never render on a post!!!
    return redirect("/success")   


@app.route("/success")
def success():
    #check to see if the user is logged in and redirect if not
    if "logged_in" not in session:
        return redirect("/")
    
    logged_user = User.get_by_id( {"id": session['logged_in'] } )

    return render_template("success.html", user = logged_user)


@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")


#CRUD

#Read Many



# Read One



# Create - requires 2 routes



# Update - requires 2 routes



# Delete