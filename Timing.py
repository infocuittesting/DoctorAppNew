from sqlwrapper import gensql,dbget,dbput
import json
import datetime
from flask import Flask,request,jsonify


def Insert_Timing(request):
     try:
          timing=request.json
          doc_timing = { k : v for k,v in timing.items() if k in ('doctor_id','business_id')}
          days = timing['days']
          for day in days:
               i={}
               i['doctor_id'] = doc_timing['doctor_id']
               i['business_id'] = doc_timing['business_id']
               i['day'] = day['day']
               i['start_timing'] = day['start_timing']
               i['end_timing'] = day['end_timing']
               gensql('insert','new.timing',i)
          return(json.dumps({"Message":"Record Inserted Successfully","MessageCode":"RIS","Service Status":"Success"},indent=4))
          
     except:
          return(json.dumps({"Message":"Record Inserted UnSuccessfully","MessageCode":"RIUS","Service":"UnSuccess"},indent=4))  
               
          
    
     
     


def Select_Timing(request):
    try:
        d = request.json
        output=json.loads(gensql('select','new.timing','*',d))
        return(json.dumps({"Message":"Record Selected Successfully","MessageCode":"RSS","Service Status":"Success","output":output},indent=4))
    except:
          return(json.dumps({"Message":"Recored Selected UnSuccessfully","MessageCode":"RSUS","Service":"UnSuccess"},indent=4))


def Update_Timing(request):
     try:
          timing=request.json
          doc_timing = { k : v for k,v in timing.items() if k in ('doctor_id','business_id')}
          days = timing['days']
          for day in days:
               i={}
               doc_timing['day'] = day['day']
               i['start_timing'] = day['start_timing']
               i['end_timing'] = day['end_timing']
               gensql('update','new.timing',i,doc_timing)
             
          return(json.dumps({"Message":"Record Updated Successfully","MessageCode":"RUS","Service Status":"Success"},indent=4))
     except:
          return(json.dumps({"Message":"Recored Updated UnSuccessfully","MessageCode":"RUUS","Service":"UnSuccess"},indent=4))


def Delete_Timing(request):
    try:
        d=request.json['timing_id']
        dbput("delete from new.timing where timing_id='"+d+"'")
        return(json.dumps({"Message":"Record Deleted Successfully","MessageCode":"RDS","Service Status":"Success"},indent=4))
    except:
         return(json.dumps({"Message":"Record Deleted UnSuccessfully","MessageCode":"RDUS","Service Status":"UnSuccess"},indent=4)) 
