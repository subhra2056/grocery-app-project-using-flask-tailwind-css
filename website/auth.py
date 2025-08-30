from . import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
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

        if password == confirm_password:
            #creates new customer
            new_customer = customer()
            new_customer.email = email
            new_customer.fulname = fullname
            new_customer.password = confirm_password

            try:
                #inserts new customer data into the database
                db.session.add(new_customer)
                db.session.commit()
                flash('New account created successfully!')
                return redirect('/Login')
            
            except Exception as e:
                print(e)
                flash('Email already exists! try using another email address')

            form.email.data = ''
            form.fullname.data = ''
            form.password.data = ''
            form.confirm_password.data = ''
            
    return render_template('signup.html', form = form)


@auth.route('/Login', methods=['GET', 'POST'])
def login():
    form = login_form()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        #check that customer exists in database or not
        customer = customer.query.filter_by(email = email).first()

        if customer: 
            if customer.verify_password(password = password):
                login_user(customer)
                redirect('/')
            else:
                flash('Incorrect account data')
        else:
            flash("Account doesn't exist")

    return render_template('login.html', form = form)


@auth.route('/Logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect ('/')
