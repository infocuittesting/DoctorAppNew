import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def gupshup(request):
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
     amount= request.args['dateamount']
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
     <html>
      <head></head>
      <body>
        <dl>
        <dt>
        <p><font size="2" color="blue">hi,"""+name+"""</font></p>
        <p><font size="2" color="black">"""+message+"""</font></p>
  
        <p><font size="2" color="black">mobile Number:"""+ phone+"""</font></p>
        <p><font size="2" color="black">Arrival Date:"""+ arrival+"""</font></p>
        <p><font size="2" color="black">Depature Date:"""+ depature+"""</font></p>
        <p><font size="2" color="black">Room Type:"""+ room_type+"""</font></p>
        <p><font size="4" color="black">no_of_nights: """+no_of_nights+"""</font></p>
        <p><font size="2" color="black">Country code:"""+code+"""</font></p>
        <p><font size="2" color="black">Amount:"""+amount+"""</font></p>
        <p><font size="2" color="black">adult:"""+ adult+"""</font></p>
        <p><font size="2" color="black">child:"""+child+"""</font></p>
        <p><font size="4" color="black">rooms:"""+rooms+"""</font></p>
        <p><font size="2" color="black">pickupdrop:"""+ pickupdrop+"""</font></p>
      
        
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
