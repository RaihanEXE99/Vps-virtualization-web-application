from .import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(40),unique=True)
    phone = db.Column(db.String(15),unique=True)
    password = db.Column(db.String(150))
    # Verification
    isEmailVerified = db.Column(db.Boolean)
    isPhoneVerified = db.Column(db.Boolean)
    # If company
    is_company = db.Column(db.Boolean)
    company_name = db.Column(db.String(15))
    vat_number = db.Column(db.String(15))
    # TwoFactor
    isOtpOn = db.Column(db.Boolean)
    two_factor_code = db.relationship('Two_factor_code')

class Two_factor_code(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    otp = db.Column(db.String(6))
    exp = db.Column(db.String(20))

class PhoneConfirmCode(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    otp = db.Column(db.String(6))
    exp = db.Column(db.String(20))

class EmailConfirmCode(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    otp = db.Column(db.String(6))
    exp = db.Column(db.String(20))
    