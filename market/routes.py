from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required

from market import app
# db is located in __init__
from market import db
from market.forms import RegisterForm, LoginForm, PurchaseItemForm
from market.models import Item, User


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    if purchase_form.validate_on_submit():
        print(request.form.get('purchased_item'))
    items = Item.query.all()

    return render_template("market.html", item_name=items, purchase_form=purchase_form)


# In order to allow the route receive and share data, specify methods as arguments.
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        # gets data from forms.py which gets info form register.html
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        # Passing pulled data to data-base
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category="success")

        # after registration gets redirected to market page
        return redirect(url_for('market_page'))
    if form.errors != {}:  # If there are no errors from the validations
        for err_msg in form.errors:
            flash(f"There was an error with creating a user: {err_msg}", category='danger')
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    # checks the correctness of username and password satisfying. func validate_on_submit checks and submits data
    if form.validate_on_submit():
        # getting data entered in login.html
        attempted_user = User.query.filter_by(username=form.username.data).first()
        # method check_password_correction is used for instance
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            # built-in function
            login_user(attempted_user)
            flash(f'Success! Logged in as: {attempted_user.username} ', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password do not match. Please try again.', category='danger')

    return render_template('login.html', form=form)

@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logout!", category='info')
    return redirect(url_for("home_page"))

