from . import db
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from .forms import sign_up_form, login_form
from .models import customer

auth = Blueprint('auth', __name__)


@auth.route('/Sign-up', methods=['GET', 'POST'])
def Sign_up():
    form = sign_up_form()

    if form.validate_on_submit():
        email = form.email.data
        fullname = form.fullname.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return render_template('signup.html', form=form)

        # Check if email already exists
        if customer.query.filter_by(email=email).first():
            flash("Email already exists! Try another.", "error")
            return render_template('signup.html', form=form)

        # Create new customer
        new_customer = customer()
        new_customer.email = email
        new_customer.full_name = fullname
        new_customer.password = password 

        try:
            db.session.add(new_customer)
            db.session.commit()
            flash("New account created successfully!", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            print("Database Error:", e)
            flash("Something went wrong. Please try again.", "error")

    return render_template('signup.html', form=form)


@auth.route('/Login', methods=['GET', 'POST'])
def login():
    form = login_form()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = customer.query.filter_by(email=email).first()

        if user:
            if user.verify_password(password):
                login_user(user)
                flash("Logged in successfully!", "success")
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password!", "error")
        else:
            flash("Account doesn't exist!", "error")

    return render_template('login.html', form=form)


@auth.route('/Logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for('views.login'))

