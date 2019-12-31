from flask import Flask, render_template, request, url_for, session, flash, redirect, render_template_string
from models import *
from werkzeug.security import check_password_hash, generate_password_hash
import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(**kwargs)
    return wrapped_view

def login_user(username, password):
    error = None 
    
    # Validate user inputs
    if len(username) < 1:
        error = "Username is required"
    elif len(password) < 1:
        error = "Password is required"

    if error is not None:
        return render_template("auth/login.html", error=error)

    # Get user account        
    user = User.query.filter_by(username=username).all()        
    if not user:
        error = "Incorrect login details"
    else:            
        for u in user:
            user_pwd = u.password
            user_id = u.id
        if not check_password_hash(user_pwd, password):
            error = "Incorrect login details"
    
    if error is None:
        user_role = UserRoles.query.filter_by(user_id=user_id).first()        
        role = Role.query.get(user_role.role_id)

        session.clear()
        session['user_id'] = user_id
        session['username'] = username
        session['role'] = role.name

        if role.name == "member" or role.name == "admin":
            flash("Logged in successfully!", "success")
            return redirect(url_for('index'))
        else:
            flash("Welcome back, Admin!", "success")
            return redirect(url_for('admin'))
            
    if 'user_id' in session:
        return redirect(url_for('index'))       
            
    return render_template("auth/login.html", error=error)

def create_account(username, password, role):
    error = None    
        
    if len(username) < 1 or len(password) < 1:
        error = "All fields are required"
        
    elif len(password) < 6:
        error = "Password: Minimum of 6 characters required"
    
    # Check if user already exist
    if User.query.filter_by(username=username).count() > 0:
        error = f"Sorry, '{username}' already exist"         
                
    # Register new user
    if error is None:
        raw_pwd = password
        password = generate_password_hash(password)
        user = User(username=username, password=password)
        user_role = Role.query.filter_by(name=role).first()
        role = Role.query.get(user_role.id)
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()

        return render_template_string(""" 
                    <h5>Account created successfully!</h5>
                    <p>Username: {{ username }}</p>
                    <p>Password: {{ raw_pwd }}</p>
                    <br/><hr>
                    <a href="{{ url_for('index') }}">Go back to homepage</a>
                """, username=username, raw_pwd=raw_pwd)
        # return f"Account created successfully! The username is {username} and password is {raw_pass}" 
    
    return render_template("admin/admin.html", error=error)