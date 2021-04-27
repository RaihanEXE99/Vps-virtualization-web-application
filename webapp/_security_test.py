from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for
from flask_login import login_user,login_required,logout_user,current_user
from .utility.custom_decorators import EmailAuthRequired,PhoneAuthRequired

security_test = Blueprint('security_test',__name__)

@security_test.route('/isEmailVerified')
@login_required
@EmailAuthRequired
def isEmailVerified():
   return redirect(url_for('views.response_basic_view'),err_body="Your Email is verified")

@security_test.route('/isEmailVerified')
@login_required
@PhoneAuthRequired()
def isPhoneVerified():
   return redirect(url_for('views.response_basic_view'),err_body="Your Phone no is verified")