from flask import Blueprint, render_template, request, flash, redirect, make_response
import pandas as pd
import os
import uuid
from .auth import encode_auth_token, decode_auth_token

main = Blueprint('main', __name__)

def readFile():
    file = 'app/data/userInfoData.csv'
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return None

@main.route('/home')
def home():
    token = request.cookies.get('token')
    if token:
        user = decode_auth_token(token)
        if user and not user.startswith("Token"):
            file = 'app/data/data.csv'
            df = pd.read_csv(file)
            page = int(request.args.get('page', 1))
            per_page = 20
            total = len(df)
            total_pages = (total + per_page - 1) // per_page

            start = (page - 1) * per_page
            end = start + per_page
            users = df.iloc[start:end].to_dict(orient='records')
            
            return render_template('home.html', username=user,page=page, total_pages=total_pages, total=total,users=users)
        
        else:
            return redirect('/login') 
    else:
        return redirect('login')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        fileData = readFile()

        if fileData is not None:
            user = fileData[(fileData['username'] == username) & (fileData['password'] == password)]
            if not user.empty:
                token = encode_auth_token(username)
                response = make_response(redirect('/home'))
                response.set_cookie('token', token)
                flash('Login successful!', 'success')
                return response
            else:
                flash('Invalid username or password.', 'danger')
        else:
            flash('User data not found.', 'danger')
    return render_template('index.html')

@main.route('/signup', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        user_id = str(uuid.uuid4())

        data = {"user_id": user_id, 'username': username, 'password': password, 'email': email}
        file = 'app/data/userInfoData.csv'
        df = pd.DataFrame(data, index=[0])
        os.makedirs(os.path.dirname(file), exist_ok=True)

        if not os.path.exists(file):
            df.to_csv(file, mode='w', header=True, index=False)
        else:
            df.to_csv(file, mode='a', header=False, index=False)

        flash('Account created successfully! Please log in.', 'success')
        return redirect('/login')
    return render_template('signUp.html')

@main.route('/logout')
def logout():
    response = make_response(redirect('/login'))  
    response.set_cookie('token', '', expires=0) 
    flash('You have been logged out.', 'info')
    return response
