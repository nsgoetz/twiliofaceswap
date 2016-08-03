from flask import Flask, request, redirect, session, send_file
from twilio.rest import TwilioRestClient
import twilio.twiml
import random
import urllib2
import string
import faceswap 

#todo - fix lol
SECRET_KEY = 'a secret key'
# Try adding your own number to this list!
callers = {
    "+12143150822": "Noah Goetz"
}

app = Flask(__name__)
app.config.from_object(__name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = "/Users/ngoetz/Projects/FaceSwap/"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

base_url = "http://bd0f309a.ngrok.io/"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def id_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

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

def save_image(media_url):
    if media_url != "":
        #todo error handling here
        #suffix = string.split(media_url, ".")[-1]
        suffix = ".jpeg"
        imgname = "image/" + id_generator() + suffix
        file = open(UPLOAD_FOLDER+imgname, 'w+')
        req = urllib2.Request(media_url, headers={'User-Agent' : "Magic Browser"}) 
        response = urllib2.urlopen(req)
        content = response.read()
        file.write(content)
        resp_media= base_url+imgname
        return imgname
    return ""

@app.route('/receive_text', methods=['GET', 'POST'])
def receive_text():
    print "request.values = ", str(request.values)

    nummedia = request.values.get('NumMedia', default=0)
    media_type = request.values.get('MediaContentType0', default="")
    media_url = request.values.get('MediaUrl0', default="")

    # try:
    counter = session.get('counter', 0)
    image1_name = session.get('image1_path', "")
    if image1_name == "":
        counter = 0

    # increment the counter
    if nummedia == '1':
        next_counter = counter + 1
        next_counter %= 2
        session['counter'] = next_counter
        
        if counter == 0:
            session['image1_path'] = save_image(media_url)
            message = "Now send the second photo"
            resp = twilio.twiml.Response()
            resp.message(message) 
            return str(resp)   
        else:
            image2_name = save_image(media_url)
            from_number = request.values.get('From')
            if from_number == None:
                from_number = "Test"
            if from_number not in callers:
                callers[from_number] = from_number
            name = callers[from_number]
            
            print "counter = ", counter
            
            receiver = request.values.get('To')
            receiver = "Unknown_Reciever" if receiver == None else receiver

            # resp_media = "https://demo.twilio.com/owl.png"
            output_name = "image/" + id_generator() + ".jpeg"
            message = ""
            #message = "".join([name, " has messaged ", receiver, " ", str(counter), " times.", "nummedia =", str(nummedia), "Media = ", str(media_type), "url =", str(media_url)])
            try:
                faceswap.swap( image1_name,  image2_name,  output_name)
                resp_media = base_url + output_name
            except Exception, e:
                print "execteption"
                print e
                message = "too many faces"
                resp_media = "https://demo.twilio.com/owl.png"
            resp = twilio.twiml.Response()
            with resp.message(message) as m:
                m.media(resp_media)
            return str(resp)
    else:
        message = "You must send a photo"
        resp = twilio.twiml.Response()
        resp.message(message) 
        return str(reps)   

# else:
    #     resp = twilio.twiml.Response()
    #     resp.sms("You must send an image!")
    #     return str(resp)

    # except Exception as inst:
    #     print(type(inst))    # the exception instance
    #     print(inst.args)     # arguments stored in .args
    #     print(inst) 
    #     return(inst)

@app.route('/image/<filename>', methods=['GET'])
def get_image(filename):
    suffix = string.split(filename, ".")[-1]
    print "print suffix = ", suffix
    if suffix == "jpeg":
        return send_file("image/" + filename, mimetype='image/jpeg')
    elif suffix == "png":
        return send_file("image/" + filename, mimetype='image/png')
    else:
        print suffix

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
