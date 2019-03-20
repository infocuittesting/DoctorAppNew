import urllib.request
import time
import json
import psycopg2
from flask import Flask, request, jsonify

def gupshupsms(request):
         print("hiiiii")
         
         if request.method=='POST':
                
                 mobile = request.json['mobile']
                 message = request.json['message']
                 code =  request.json['code']
                 print(mobile, message, code)
         if request.method=='GET':
                mobile = request.args['mobile']
                message = request.args['message']
                code =  request.args['code']
                print(mobile, message, code)
                
         url = "https://control.msg91.com/api/sendhttp.php?authkey=195833ANU0xiap5a708d1f&mobiles="+mobile+"&message="+message+"&sender=Infoit&route=4&country="+code+""
         req = urllib.request.Request(url)
         with urllib.request.urlopen(req) as response:
            the_page = response.read()
            the_page = the_page[1:]
            print(the_page)
            the_page = str(the_page)
         return(json.dumps({"Message":"SMS Sent Sucessfully","Message_Code":"SSS","Key":the_page},indent =3))
