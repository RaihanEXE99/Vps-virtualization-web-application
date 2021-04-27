from twilio.rest import Client

account_sid = 'AC37381e36c41d8f081f74958449d5f06b'
auth_token = 'c069353b2399e2cacf00c9dff584a60e'
    
client = Client(account_sid, auth_token)

# def getOTP():
#     return random.randrange(100000,999999)

def getOTPApi(number,otp):
    body = "Your Otp is " + str(otp)
    message = client.messages.create(
        body=body,
        from_='+19729542472',
        to='+8801670557340'
    )
    if message.sid:
        print(message.sid)