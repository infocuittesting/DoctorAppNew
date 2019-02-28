from sqlwrapper import gensql,dbget,dbput
import json
import datetime
from flask import Flask,request,jsonify

def Insert_Doctor_Login(request):
  try:
        d=request.json
        print(d)
        datetime1=datetime.datetime.now()
        print(datetime1)
        d['date_time'] = datetime1
        
        doctorid = json.loads(dbget("select count(*) as doctor_id from new.doctorinbusiness where doctor_id ='"+d['doctor_id']+"'"))
        print( doctorid)
        businessid = json.loads(dbget("select count(*) as business_id from new.doctorinbusiness where business_id ='"+str(d['business_id'])+"'"))
        print(businessid)
        if doctorid[0]['doctor_id']==1 and businessid[0]['business_id']!=1:
           print("hai")
           
           dbput("update new.doctorinbusiness set login_status='" + str(d['login_status']) + "' \
                   where doctor_id='" +d['doctor_id']+"' and business_id='"+str(d['business_id'])+"'")

           gensql('insert','new.doctor_login',d)
           return(json.dumps({"Message":"Record Updated  Successfully","Message_Code":"RUS","Service_Status":"Success"},indent=4))
        else:
           return(json.dumps({"Message":"Invalid_Data","Message_Code":"ID","Service_Status":"UnSuccess"},indent=4)
        
   except:
        return(json.dumps({"Message":"Record Inserted UnSuccessfull","Message_Code":"RIUS","Service_Status":"Failure"},indent=4))
def Select_Doctor_Login(request):
    try:
        d=request.json
        print('mohan',d)
        d1=json.loads(gensql('select','new.doctor_login','*',d))
        return(json.dumps({"Message":"Record Selected Successfully","Message_Code":"RSS","Service_Status":"Success","output":d1},indent=4))
    except:
        return(json.dumps({"Message":"Record Selected UnSuccessfull","Message_Code":"RSUS","Service_Status":"Failure"},indent=4))
    

def Update_Doctor_Login(request):
      try:
          d=request.json
          print(d)
          e= { k : v for k,v in d.items() if k in ('doctor_login_id')}
          a= { k : v for k,v in d.items() if k not in ('doctor_login_id')}
    
          gensql('update','new.FeedBack',a,e)
          #res = dbget("")
          return(json.dumps({"Message":"Record Updated Successfully","Message_Code":"RUS","Service_Status":"Success"},indent=4))
      except:
          return(json.dumps({"Message":"Recored Updated UnSuccessfully","Message_Code":"RUUS","Service":"UnSuccess"},indent=4))
    





