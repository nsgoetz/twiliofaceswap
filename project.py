from flask import Flask
from twilio.rest import TwilioRestClient

#todo - fix lol
SECRET_KEY = 'a secret key'
# Try adding your own number to this list!
callers = {
    "+2143150822": "Noah Goetz"
}

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # counter = session.get('counter', 0)

    # # increment the counter
    # counter += 1

    # # Save the new counter value in the session
    # session['counter'] = counter

    # from_number = request.values.get('From')
    # if from_number in callers:
    #     name = callers[from_number]
    # else:
    #     name = "Monkey"

    # message = "".join([name, " has messaged ", request.values.get('To'), " ", 
    #     str(counter), " times."])
    # resp = twilio.twiml.Response()
    # resp.sms(message)

    # return str(resp)

    return 'Hello, World!'


@app.route('/receive_text', methods=['GET', 'POST'])
def receive_text():
    counter = session.get('counter', 0)

    # increment the counter
    counter += 1

    # Save the new counter value in the session
    session['counter'] = counter

    from_number = request.values.get('From')
    if from_number in callers:
        name = callers[from_number]
    else:
        name = "Monkey"

    message = "".join([name, " has messaged ", request.values.get('To'), " ", 
        str(counter), " times."])
    resp = twilio.twiml.Response()
    resp.sms(message)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)

#need local media server 

#need sessions 

#need unwrap 

# Find these values at https://twilio.com/user/account
# account_sid = "ACXXXXXXXXXXXXXXXXX"
# auth_token = "YYYYYYYYYYYYYYYYYY"
# client = TwilioRestClient(account_sid, auth_token)

# message = client.messages.create(to="+12316851234", from_="+15555555555",
#                                      body="Hello there!",
#                                      media_url=['https://demo.twilio.com/owl.png', 'https://demo.twilio.com/logo.png'])
