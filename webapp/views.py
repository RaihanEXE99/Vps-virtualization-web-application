from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for
from flask_login import login_user,login_required,logout_user,current_user
from .models import Two_factor_code
from . import db
from . import mail,MAIL_USERNAME
import json
from flask_mail import Message

views = Blueprint('views',__name__)

@views.route('/',methods=['GET'])
@login_required
def home():
   return render_template("home.html",user = current_user)



@views.route('/phone_verification')
@login_required
def verification_center():
   return render_template('auth/phone_verification.html')

@views.route('/two_factor_toggle',methods=['POST','GET'])
@login_required
def two_factor_toggle():
   val = current_user.isOtpOn
   if request.method == "POST":
      toggle = request.form.get('toggle')
      if toggle == 'True':
         current_user.isOtpOn = False
         db.session.commit()
      elif toggle == 'False' :
         current_user.isOtpOn = True
         db.session.commit()
      print(str(current_user.isOtpOn)*100)
      return redirect(url_for('views.two_factor_toggle',val=val))
   else:
      return render_template('auth/two_factor_toggle.html',val=val)

@views.route('/mail-me')
def sendmail():
   msg = Message('Yo Bro', sender = MAIL_USERNAME, recipients = ['zushitt@gmail.com'])
   msg.body = "You can do that Too"
   mail.send(msg)
   return "Sent"