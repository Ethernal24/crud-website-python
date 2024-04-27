from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Receipt
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login berhasil', category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Password salah", category="error")
        else:
            flash("Email tidak ada", category="error")

    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()
        if user:
            flash("email sudah ada", category="error")
        elif len(email)<4:
            flash('Email harus lebih dari 4 character', category="error")
        elif len(first_name)<2:
            flash("nama harus lebih dari 2 karakter", category="error")    
        elif password1 != password2:
            flash('pasword tidak sama', category="error")
        elif len(password1)<7:
            flash('pasword harus setidaknya 7 karakter', category="error")
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            # login_user(user, remember=True)
            flash('Akun berhasil dibuat', category="success")
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user = current_user)


@auth.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        nama_menu = request.form['namaMenu']
        type_menu = request.form['typeMenu']
        # radio_menu = Receipt.query.first()
        # radio_menu.option = type_menu
        nama_pembeli = request.form['namaPembeli']
        harga = request.form['harga']
        quantity = request.form['quantity']
        total_harga = request.form['totalHarga']
        
        my_data = Receipt(nama_menu = nama_menu, tipe_menu = type_menu, nama_pembeli = nama_pembeli, harga = harga, quantity = quantity, total_harga = total_harga)
        db.session.add(my_data)
        db.session.commit()
        flash("Receipt Berhasil ditambah")
        return redirect (url_for('views.home'))


@auth.route('/update', methods = ['GET','POST'])
def update():
    if request.method == 'POST':
        nota = Receipt.query.get(request.form.get('id'))
        nota.nama_menu = request.form['namaMenu']
        nota.tipe_menu = request.form['typeMenu']
        nota.nama_pembeli = request.form['namaPembeli']
        nota.harga = request.form['harga']
        nota.quantity = request.form['quantity']
        nota.total_harga = request.form['totalHarga']
        db.session.commit()
        flash('Receipt berhasil di perbarui')
        return redirect (url_for('views.home'))
    

@auth.route('/delete/<id>/', methods = ['GET','POST'])
def delete(id):
    nota = Receipt.query.get(id)
    db.session.delete(nota)
    db.session.commit()
    flash('Receipt berhasil di hapus')
    return redirect (url_for('views.home'))