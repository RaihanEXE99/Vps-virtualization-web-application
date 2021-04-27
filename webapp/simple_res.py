from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for

simple_res = Blueprint('simple_res',__name__)

@simple_res.route('/success/<succ_body>')
def response_succ_view(succ_body):
   return render_template('response/response_success.html',succ_body=succ_body)

@simple_res.route('/basic/<err_body>')
def response_basic_view(err_body):
   return render_template('response/response_basic.html',err_body=err_body)

