from flask import Blueprint,render_template,request,flash,redirect,url_for,jsonify
from .models import User,Two_factor_code,EmailConfirmCode,PhoneConfirmCode
from werkzeug.security import  generate_password_hash,check_password_hash
from .import db
from flask_login import login_user,login_required,logout_user,current_user

from .security import __sign_up_validation,__generate_otp,__emailConfirmCode
from .utility.custom_decorators import EmailAuthRequired
import base64,datetime

from flask_mail import Message
from . import mail,MAIL_USERNAME

auth = Blueprint('auth',__name__)

@auth.route('/login')
def login():
   if current_user.is_authenticated:
      return redirect(url_for('views.home'))
   return render_template("auth/login.html",user=current_user)

@auth.route('/login',methods=['POST'])
def login_post():
   email = request.form.get('email')
   password = request.form.get('password')
   user = User.query.filter_by(email=email).first()
   if user:
      if check_password_hash(user.password,password):
         if user.isOtpOn == True:
            isOk,user_id,otp,exp = __generate_otp(user)
            if isOk:
               create_new_otp = Two_factor_code(user_id=user_id,otp=otp,exp=exp)
               db.session.add(create_new_otp)
               db.session.commit()
               p1,p2 = base64.b64encode(email.encode('ascii')).decode("ascii"),base64.b64encode(password.encode('ascii')).decode("ascii")
               return render_template('auth/otp.html',p1=p1,p2=p2)
            else:
               return redirect(url_for('simple_res.response_basic_view',err_body="Something wrong happend"))
         else:
            login_user(user,remember=True)
            return redirect(url_for('views.home'))
      else:
         flash('Invalid password',category='error')
         return redirect(url_for('auth.login'))
   else:
      flash("Email doesn't exist",category='error')
      return redirect(url_for('auth.login'))


@auth.route('/otp',methods=['POST'])
def otp_post():
   otp = request.form.get('otp')
   p1 = request.form.get('p1')
   p2 = request.form.get('p2')
   p1 = base64.b64decode(p1.encode('ascii')).decode("ascii")
   p2 = base64.b64decode(p2.encode('ascii')).decode("ascii")
   user = User.query.filter_by(email=p1).first()
   if user:
      if check_password_hash(user.password,p2):
         otp_code = Two_factor_code.query.filter_by(user_id=user.id).first()
         if (otp_code.otp == otp) and (str(datetime.datetime.now()) < otp_code.exp):
            login_user(user,remember=True)
            return redirect(url_for('views.home'))
         else:
            return redirect(url_for('simple_res.response_basic_view',err_body="Expired or Invalid Token , Go to Login and try again"))
      else:
         return redirect(url_for('simple_res.response_basic_view',err_body="Wrong credentials"))
   else:
      return redirect(url_for('simple_res.response_basic_view',err_body="Email does not exist"))

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
   if request.method == "POST":
      name = request.form.get('name')
      email = request.form.get('email')
      password1 = request.form.get('password1')
      password2 = request.form.get('password2')
      phone = request.form.get('phone')
      is_company = request.form.get('is_company')

      if is_company:
         is_company = True
         company_name = request.form.get('company_name')
         vat_number = request.form.get('vat_number')
      else:
         is_company = False
         company_name,vat_number = "",""

      isInvalid =  __sign_up_validation(name,email,password1,password2,phone)
      if isInvalid:
         flash(isInvalid,category="error")
      else:
         new_user = User(
            name=name,
            email=email,
            phone=phone,
            password=generate_password_hash(password1, method='sha256'),
            is_company=is_company,
            company_name=company_name,
            vat_number=vat_number,
            isOtpOn=False,
            isEmailVerified = False,
            isPhoneVerified = False
            )
         db.session.add(new_user)
         db.session.commit()
         flash("Account Created",category="success")
         return redirect(url_for('auth.login'))
   return render_template("/auth/sign_up.html",user=current_user)


@auth.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('auth.login'))

@auth.route('/verification_center')
@login_required
def verification_center_view():
   return render_template('auth/verification_center.html')

@auth.route('/phone_verification')
@login_required
def phone_verification_view():
   if current_user.isPhoneVerified:
      return redirect(url_for('simple_res.response_succ_view'),succ_body="Already Verified")
   return render_template('auth/phone_verification.html')

@auth.route('/email_verification',methods=['POST','GET'])
@login_required
def email_verification_view():
   if current_user.isEmailVerified:
      return redirect(url_for('simple_res.response_succ_view',succ_body="Already Verified"))
   elif request.method == "POST":
      otp = request.form.get('otp')
      otp_code = EmailConfirmCode.query.filter_by(user_id=current_user.id).first()
      if (otp_code.otp == otp) and (str(datetime.datetime.now()) < otp_code.exp):
         current_user.isEmailVerified = True
         db.session.commit()
         return redirect(url_for("auth.verification_center_view"))
      else:
         return redirect(url_for('simple_res.response_basic_view',err_body="Invalid Code"))
   return render_template('auth/email_verification.html')

@auth.route('/generate-otp-email',methods=['POST'])
@login_required
def generate_otp_email():
   if request.method == "POST":
      print("STARTED\n"*5)
      isOk,otp,exp,user_id= __emailConfirmCode(current_user)
      if isOk:
         msg = Message('Email Verification Code', sender = MAIL_USERNAME, recipients = [current_user.email])
         msg.body = "Your Verification code is {}".format(otp)
         mail.send(msg)

         create_new_otp = EmailConfirmCode(user_id=user_id,otp=otp,exp=exp)
         db.session.add(create_new_otp)
         db.session.commit()
         return jsonify({"res":"Email Confirmation Code generated successfully"})
      else:
         return jsonify({"res":"Something Wrong"})


# @auth.route('forgot-password',methods=['POST','GET'])
# def forgot_password():
#    if request.method == 'POST':
#       email = request.form.get('email')
#       if email:
#          flash('Mail sent successfully',category='success')
#          return render_template('auth/forgot_password.html')
#    else:
#       return render_template('auth/forgot_password.html')