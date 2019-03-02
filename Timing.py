from sqlwrapper import gensql,dbget,dbput
import json
import datetime
from flask import Flask,request,jsonify


def Insert_Timing(request):
     try:
          timing=request.json
          doc_timing = { k : v for k,v in timing.items() if k in ('doctor_id','business_id')}
          if doc_timing['doctor_id'] != 0:
               doctor = json.loads(dbget("select count(*) as doc_id from new.doctor_profile where doctor_profile_id ='"+doc_timing['doctor_id']+"'"))
               business = json.loads(dbget("select count(*) as bus_id from new.business_profile where business_id ='"+str(doc_timing['business_id'])+"'"))
               if doctor[0]['doc_id'] == 1 and business[0]['bus_id'] == 1:
                    days = timing['days']
                    for day in days:
                         i={}
                         i['doctor_id'] = doc_timing['doctor_id']
                         i['business_id'] = doc_timing['business_id']
                         i['day'] = day['day']
                         i['start_timing'] = day['start_timing']
                         i['end_timing'] = day['end_timing']
                         i['session'] = day['session']
                         gensql('insert','new.timing',i)
                    return(json.dumps({"Message":"Record Inserted Successfully","Message_Code":"RIS","Service_Status":"Success"},indent=4))
               else:
                    return(json.dumps({'Message': 'Invalid Data', 'Message_Code': 'ID', 'Status': 'Failure'},indent=4)) 
          else:
               days = timing['days']
               for day in days:
                    i={}
                    i['doctor_id'] = doc_timing['doctor_id']
                    i['business_id'] = doc_timing['business_id']
                    i['day'] = day['day']
                    i['start_timing'] = day['start_timing']
                    i['end_timing'] = day['end_timing']
                    i['session'] = day['session']
                    gensql('insert','new.timing',i)
               return(json.dumps({"Message":"Record Inserted Successfully","Message_Code":"RIS","Service_Status":"Success"},indent=4))
     except:
          return(json.dumps({"Message":"Record Inserted UnSuccessfully","MessageCode":"RIUS","Service":"UnSuccess"},indent=4))  
def Select_Timing(request):
    try:
        d = request.json
        if d['doctor_id'] != 0:
             doctor = json.loads(dbget("select count(*) as doc_id from new.doctor_profile where doctor_profile_id ='"+d['doctor_id']+"'"))
             print(doctor)
             business = json.loads(dbget("select count(*) as bus_id from new.business_profile where business_id ='"+str(d['business_id'])+"'"))
             
             if doctor[0]['doc_id'] == 1 and business[0]['bus_id'] == 1:
                  output=json.loads(gensql('select','new.timing','*',d))
                  return(json.dumps({"Message":"Record Selected Successfully","Message_Code":"RSS","Service_Status":"Success","output":output},indent=4))
             else:
                 return(json.dumps({'Message': 'Invalid Data', 'MessageCode': 'ID', 'Status': 'Failure'},indent=4)) 
        else:
            output=json.loads(gensql('select','new.timing','*',d))
            return(json.dumps({"Message":"Record Selected Successfully","Message_Code":"RSS","Service_Status":"Success","output":output},indent=4)) 
    except:
          return(json.dumps({"Message":"Recored Selected UnSuccessfully","Message_Code":"RSUS","Service":"UnSuccess"},indent=4))

def Update_Timing(request):
     try:
          timing=request.json
          doc_timing = { k : v for k,v in timing.items() if k in ('doctor_id','business_id')}
          if doc_timing['doctor_id'] != 0:
               doctor = json.loads(dbget("select count(*) as doc_id from new.doctor_profile where doctor_profile_id ='"+doc_timing['doctor_id']+"'"))
               business = json.loads(dbget("select count(*) as bus_id from new.business_profile where business_id ='"+str(doc_timing['business_id'])+"'"))
               days = timing['days']
               if doctor[0]['doc_id'] == 1 and business[0]['bus_id'] == 1:
                    for day in days:
                         i={}
                         doc_timing['day'] = day['day']
                         i['start_timing'] = day['start_timing']
                         i['end_timing'] = day['end_timing']
                         doc_timing['session'] = day['session']
                         gensql('update','new.timing',i,doc_timing)
                    return(json.dumps({"Message":"Record Updated Successfully","Message_Code":"RUS","Service_Status":"Success"},indent=4))
               else:
                    return(json.dumps({'Message': 'Invalid Data', 'Message_Code': 'ID', 'Status': 'Failure'},indent=4))
          else:
               days = timing['days']
               for day in days:
                         i={}
                         doc_timing['day'] = day['day']
                         i['start_timing'] = day['start_timing']
                         i['end_timing'] = day['end_timing']
                         doc_timing['session'] = day['session']
                         gensql('update','new.timing',i,doc_timing)
               return(json.dumps({"Message":"Record Updated Successfully","Message_Code":"RUS","Service_Status":"Success"},indent=4))
     except:
          return(json.dumps({"Message":"Recored Updated UnSuccessfully","Message_Code":"RUUS","Service":"UnSuccess"},indent=4))
def Delete_Timing(request):
    try:
        d=request.json['timing_id']
        dbput("delete from new.timing where timing_id='"+d+"'")
        return(json.dumps({"Message":"Record Deleted Successfully","Message_Code":"RDS","Service_Status":"Success"},indent=4))
    except:
         return(json.dumps({"Message":"Record Deleted UnSuccessfully","Message_Code":"RDUS","Service_Status":"UnSuccess"},indent=4)) 
