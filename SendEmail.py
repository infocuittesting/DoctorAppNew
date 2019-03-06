import json
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask,request,jsonify
from sqlwrapper import gensql,dbget,dbput
def callfn(request):
    d = request.json
    sender = 'infocuit.testing@gmail.com'
    res =json.loads(dbget(" select new.user_profile.email from new.appointment join new.user_profile on new.appointment.mobile=new.user_profile.mobile \
                            # where appointment_id='"+str(d['appointment_id'])+"'"))
    
    
    print('lenth',len(res))

    if len(res)==0:
         return(json.dumps({'Message':'Email Not Available','Message_code':'ENA','Status':'Failure'},indent=4))
    else:
        #print(res[0]['email'],type(res[0]['email']))
    
        mail = []
        if len(res[0]['email']) != None:
            mail = [x['email'] for x in res]
            print("hiii",mail)
            len_mail = len(mail)
            message_no = request.json['message']
            print(message_no)
            val1 = message_no['name']
            val2 = message_no['message']
            val3 = message_no['token_no']
            val4 = message_no['token_status']
            val5 = message_no['wait_time']
            val6 = message_no['bus_hour']
            val7 = message_no['break_time']
            val8 = message_no['address']
            val9 = message_no['hospital']
            subject = request.json['subject']
            msg = MIMEMultipart()
            msg['from'] = sender
            x=0
            while len_mail != x:
                msg['to'] = mail[x]
                msg['subject'] = subject
                html = """\
                <html>
                <head></head>
                <body>
                  <dl>
                  <dt>
                   <p><font size="2" color="black">"""+str(val1)+"""</font></p>
                    <p><font size="4" color="blue">"""+str(val2)+"""</font></p>
                    <dd>
                    <p><font size="2" color="black">"""+str(val3)+"""</font></p>
                    <p><font size="2" color="black">"""+str(val4)+"""</font></p>
                    <p><font size="2" color="black">"""+str(val5)+"""</font></p>
                    <p><font size="2" color="black">"""+str(val6)+"""</font></p>
                    <p><i><font size="2" color="blue">"""+str(val7)+"""</font></i></p>
                    <p><font size="4" color="blue">"""+str(val8)+"""</font></p>
                    </dd>
                    </dl>
                 </body>
                 </html>
                 """
                msg.attach(MIMEText(html,'html'))
                gmailuser = 'infocuit.testing@gmail.com'
                password = 'infocuit@123'
                server = smtplib.SMTP('smtp.gmail.com',587)
                server.starttls()
                server.login(gmailuser,password)
                text = msg.as_string()
                server.sendmail(sender,mail[x],text)
                x+=1
                server.quit()
                
            print ("the message has been sent successfully") 
            return(json.dumps({'Message': 'Mail Send Successfully','Message_code':'MSS','Status':'sucess'},indent=4))   
             
        else:
            return(json.dumps({'Message':'Email Not Available','Message_code':'ENA','Status':'Failure'},indent=4))

