from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone = True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class Receipt(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nama_menu = db.Column(db.String(1000))
    tipe_menu = db.Column(db.String)
    nama_pembeli = db.Column(db.String(1000))
    harga = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    total_harga = db.Column(db.Integer)
    
    def __init__(self, nama_menu, tipe_menu, nama_pembeli, harga, quantity, total_harga):
        self.nama_menu = nama_menu
        self.tipe_menu = tipe_menu
        self.nama_pembeli = nama_pembeli
        self.harga = harga
        self.quantity = quantity
        self.total_harga = total_harga


