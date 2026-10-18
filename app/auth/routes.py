from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from urllib.parse import urlsplit

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Jika user sudah login, arahkan kembali ke dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        # Membuat instance User baru
        user = User(username=form.username.data, email=form.email.data)
        # Menggunakan metode hashing yang kita buat di models.py
        user.set_password(form.password.data)
        
        # Menyimpan ke database
        db.session.add(user)
        db.session.commit()
        
        flash('Selamat! Akun Anda berhasil dibuat. Silakan login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        # Mencari user berdasarkan email
        user = User.query.filter_by(email=form.email.data).first()
        
        # Mengecek apakah user ada DAN password cocok dengan hash di database
        if user is None or not user.check_password(form.password.data):
            flash('Email atau password salah. Silakan coba lagi.', 'error')
            return redirect(url_for('auth.login'))
            
        # Mengeksekusi sesi login via Flask-Login
        login_user(user, remember=form.remember_me.data)
        
        # Proteksi Open Redirect (Keamanan tambahan)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
            
        return redirect(next_page)
        
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))