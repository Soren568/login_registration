from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.users import User
from flask import flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/home_page')

@app.route('/home_page')
def home():
    return render_template("index.html")

@app.route('/user/register', methods=["POST"])
def register():
    # Form validation
    if not User.validate_user(request.form):
        return redirect('/')
    else:
        print(request.form)
    # print("dob: " + request.form['dob'])
    #  PW hashing
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        #  hashed pw into data dict
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": pw_hash,
            "dob": request.form['dob'],
            "gender": request.form['gender'],
            "account_type": request.form['account_type'],
        }
        print(data)
        User.save(data)
        flash("Account created! Please login with your credentials.", "success")
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    user_data = User.get_by_email(request.form)
    print(user_data)
    if not user_data:
        flash("Email not found.", "email_not_found")
        return redirect('/')
    if not bcrypt.check_password_hash(user_data["password"], request.form['password']):
        flash("Incorrect password.", "pw")
        return redirect('/')
    session['user_id'] = user_data["id"]
    return redirect('/login/success')

@app.route('/login/success')
def login_success():
    active_user = User.get_by_id({"id":session['user_id']})
    if active_user == False:
        flash("Something went wrong with the id.", "bad_id")
        return redirect('/')
    print(active_user)
    return render_template("success.html")

@app.route('/logout')
def clear_session():
    session.clear()
    flash("You are logged out. Have a good day!", "logout")
    return redirect('/')