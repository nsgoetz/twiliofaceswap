from flask import Flask, request, redirect, session
from twilio.rest import TwilioRestClient
import twilio.twiml
import random

#todo - fix lol
SECRET_KEY = 'a secret key'
# Try adding your own number to this list!
callers = {
    "+12143150822": "Noah Goetz"
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

    nummedia = request.values.get('NumMedia')
    if nummedia == None:
        nummedia = ""   
    media_type = request.values.get('MediaContentType')
    if media_type == None:
        media_type = ""
    media_url = request.values.get('MediaUrl')
    if media_url == None:
        media_url = ""

    # try:
    counter = session.get('counter', 0)

    # increment the counter
    counter += 1

    # Save the new counter value in the session
    session['counter'] = counter

    from_number = request.values.get('From')
    if from_number == None:
        from_number = "Test"
    if from_number not in callers:
        callers[from_number] = from_number
    name = callers[from_number]
    
    print "counter = ", counter
    
    receiver = request.values.get('To')
    receiver = "Unknown_Reciever" if receiver == None else receiver

    message = "".join([name, " has messaged ", receiver, " ", str(counter), " times.", "nummedia =", str(nummedia), "Media = ", str(media_type), "url =", str(media_url)])
    resp = twilio.twiml.Response()
    with resp.message(message) as m:
        m.media("https://demo.twilio.com/owl.png")
    return str(resp)
# else:
    #     resp = twilio.twiml.Response()
    #     resp.sms("You must send an image!")
    #     return str(resp)

    # except Exception as inst:
    #     print(type(inst))    # the exception instance
    #     print(inst.args)     # arguments stored in .args
    #     print(inst) 
    #     return(inst)

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
