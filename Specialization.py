from flask import Flask,request,jsonify
from sqlwrapper import gensql,dbget,dbput
import json
import re
def insertspecialization(request):
    try:
        d=request.json
        e = request.json['specialization_name']
        regex = re.compile('[a-zA-Z]')
        specialization_name = json.loads(dbget("select count(*) as specialization_name from new.specialization where specialization_name ='"+e+"'"))
        if specialization_name[0]['specialization_name'] == 1:
            return(json.dumps({"Message":"Already Exists","Message_Code":"AE","Service_Status":"Failure"},indent=4))
        
        if regex.match(e):
            gensql('insert','new.specialization',d)
            return(json.dumps({"Message":"Record Inserted Successfully","Message_Code":"RIS","Service_Status":"Success"},indent=4))
        else:
            return(json.dumps({"Message":"Invalid Input","Message_Code":"II","Service_Status":"Failure"},indent=4))
    except:
       return(json.dumps({"Message":"Record Inserted UnSuccessfull","Message_Code":"RIUS","Service_Status":"Failure"},indent=4))

def selectspecialization(request):
    try:
        d1 = json.loads(gensql('select','new.specialization','*'))
        return(json.dumps({"Message":"Record Selected Successfully","Message_Code":"RSS","Service_Status":"Success","output":d1},indent=4))
    except:
        return(json.dumps({"Message":"Record Selected UnSuccessfull","Message_Code":"RSUS","Service_Status":"Failure"},indent=4))
    
def updatespecialization(request):
      try:
          d=request.json
          e= { k : v for k,v in d.items() if k in ('specialization_id')}
          a= { k : v for k,v in d.items() if k not in ('specialization_id')}
          specialization = json.loads(dbget("select count(*) as specialization_id from new.specialization where specialization_id ='"+str(d['specialization_id'])+"'"))
          if specialization[0]['specialization_id'] == 1:
              gensql('update','new.specialization',a,e)
              return(json.dumps({"Message":"Record Updated Successfully","Message_Code":"RUS","Service_Status":"Success"},indent=4))
          else:
             return(json.dumps({"Message":"Invalid specialization_id ","Message_Code":"ICI","Service_Status":"Failure"},indent=4))
      except:
          return(json.dumps({"Message":"Recored Updated UnSuccessfully","Message_Code":"RUUS","Service":"Failure"},indent=4))
def deletespecialization(request):
    try:
        d=request.json['specialization_id']
        dbput("delete from new.specialization where specialization_id='"+d+"'")
        return(json.dumps({"Message":"Record Deleted Successfully","Message_Code":"RDS","Service_Status":"Success"},indent=4))
    except:
         return(json.dumps({"Message":"Record Deleted UnSuccessful","Message_Code":"RDUS","Service_Status":"Failure"},indent=4))
