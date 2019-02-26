import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def gupshup(request):
    Hotel_Name = 'QualityInn'
    Hotel_Address = 'Chennai'
    Hotel_Mobile_Number = '99999999999'
    Hotel_email = 'qualityinn@gmail.com'
    name = request.args['name']
    phone= request.args['mobile']
    code= request.args['code']
    arrival = request.args['arrival']
    depature = request.args['depature']
    rooms= request.args['rooms']
    pickupdrop=request.args['pickupdrop']
    email = request.args['email']
    message = request.args['message']
    child = request.args['child']
    adult = request.args['adult']
    Booking_details = 'BOOKING DETAILS'
    
    no_of_nights= request.args['no_of_nights']
    room_type = request.args['roomtype']
     
    sender = 'infocuit.testing@gmail.com'
    receiver = email
    print(sender,type(sender),receiver,type(receiver))
     
    #data = message.split("|")
    #print(data)
    subject = request.args['subject']
    msg = MIMEMultipart()
    msg['from'] = sender
    msg['to'] = receiver
    msg['subject'] = subject
    # Create the body of the message (a plain-text and an HTML version)
    html = """\
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        </head>
        <body>
        <dl>
        <dt>
        <pre>
        <font size="4" color="black">"""+Hotel_Name+""",</font>
        <font size="4" color="black">"""+Hotel_Address+""",</font>
        <font size="4" color="black">"""+Hotel_Mobile_Number+""",</font>
        <font size="4" color="black">"""+Hotel_email+""",</font>
        
        <font size="4" color="black">Dear """+name+""",</font>
        <font size="4" color="black">      We are delighted that you have selected our """+Hotel_Name+""" On behalf of the entire team at the
      """+Hotel_Name+""",extend you a very welcome and trust stay with us will be both enjoyable and comfortable
      """+Hotel_Name+""" offers a selection of business services and facilities.which are detailed in the booklet,
      placed on the writing table in your room.Should you require any assistance or have any specific
      requirements,please do not hesitate to contact me extension(999).</font>
        </pre>
 
        <p><font size="2" color="black">"""+Booking_details+"""</font></p>
        <p><font size="2" color="blue">Hi,"""+name+"""</font></p>
        <p><font size="2" color="black">"""+message+"""</font></p>
        <p><font size="2" color="black">country code:"""+code+"""</font></p>
        <p><font size="2" color="black">mobile Number:"""+phone+"""</font></p>
        <p><font size="2" color="black">Arrival Date:"""+arrival+"""</font></p>
        <p><font size="2" color="black">Depature Date:"""+depature+"""</font></p>
        <p><font size="2" color="black">Adult:"""+adult+"""</font></p>
        <p><font size="2" color="black">Child:"""+child+"""</font></p>
        <p><font size="2" color="black">Room Type:"""+room_type+"""</font></p>
        <p><font size="2" color="black">number of Nights: """+no_of_nights+"""</font></p>
        <p><font size="2" color="black">Rooms:"""+rooms+"""</font></p>
        <p><font size="2" color="black">pickupdrop:"""+pickupdrop+"""</font></p>
        
       
        <font size="4" color="black">With best regards / Yours sincerely,</font>
        <font size="4" color="black">Hotel Manager</font>

        </dl>
        </body>
        </html>
        """

     
     
    #msg.attach(MIMEText(msg['subject'],'plain'))
    msg.attach(MIMEText(html,'html'))
     
    gmailuser = 'infocuit.testing@gmail.com'
    password = 'infocuit@123'
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(gmailuser,password)
    text = msg.as_string()
    server.sendmail(sender,receiver,text)
    print ("the message has been sent successfully")
    server.quit()
    return(json.dumps({'Return': 'Message Send Successfully',"Return_Code":"MSS","Status": "Success","Status_Code": "200"}, sort_keys=True, indent=4))

