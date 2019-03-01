import json
from flask import Flask,request,jsonify
import datetime
from sqlwrapper import gensql,dbget,dbput

def insert_businessprofile(request):
    try:
        business = request.json
        gensql('insert','new.business_profile',business)
        bus_id = json.loads(gensql('select','new.business_profile','business_id',business))
        business_id =bus_id[0]['business_id']
        return(json.dumps({"Message":"Record Inserted Successfully",
                                   "Message_Code":"RIS","Service":"Success",'business_id':business_id},indent=4))
    except:
        return(json.dumps({"Message":"Record Inserted Unsuccessful","Message_Code":"RIUS","Service_Status":"Success"},indent=4))  

def insert_Doctorsprofile(request):
    try:
        doctors = request.json['doctors']
        business = request.json['business_id']
        password = request.json['password']
        login_status = request.json['login_status']
        wait_time = request.json['average_waiting_time']
        doc_record = {k : v for k,v in doctors.items() if k not in ('Specialization','services')}
        speclaization = doctors['Specialization']
        service = doctors['services']
        if len(speclaization) == 0 and len(service) == 0:
            return(json.dumps({"Message":"Specialization and Service are Empty","Message_Code":"SSE","Service_Status":"Failure"},indent=4))
        doc_id = json.loads(dbget("select max(doctor_id) as doc_id from new.doctor_profile"))
        doctor_id = int(doc_id[0]['doc_id'])+1
        doc_record['doctor_profile_id'] = doctors['doctor_name'][:4]+str(doctor_id)
        gensql('insert','new.doctor_profile',doc_record)
        for sep in speclaization:
            i = {}
            i['doctor_id'] = doctors['doctor_name'][:4]+str(doctor_id)
            i['specialization_id'] = sep
            gensql('insert','new.doctor_specialization',i)
        for ser in service:
            i = {}
            i['doctor_id'] = doctors['doctor_name'][:4]+str(doctor_id)
            i['service_id'] = ser
            gensql('insert','new.doctor_services',i)
        business = request.json['business_id']  
        doctor_id = doctors['doctor_name'][:4]+str(doctor_id)    
        docandbus = {'business_id':business,'doctor_id':doctor_id,'password':password,'login_status':login_status,'average_waiting_time':wait_time}
        gensql('insert','new.doctorinbusiness',docandbus)
        return(json.dumps({"Message":"Record Inserted Successfully",
                       "Message_Code":"RIS","Service":"Success","doctor_id":doctor_id},indent=4))
    except:
        return(json.dumps({"Message":"Record Inserted Unsuccessful","Message_Code":"RIUS","Service_Status":"Failure"},indent=4))  

def update_Businessprofile(request):
    try:
        d = request.json
        businessid = json.loads(dbget("select count(*) as business_id from new.business_profile where business_id ='"+str(d['business_id'])+"'"))
        if businessid[0]['business_id'] ==1:
            b={k : v for k,v in d.items() if k in ('business_id')}
            c={ k : v for k,v in d.items() if k  not in('business_id')}
            gensql('Update','new.business_profile',b,c)
            return(json.dumps({"Message":"Recored Updated Successfully","Message_Code":"RUS","Service_Status":"Success"},indent=4))
        else:
            return(json.dumps({'Message': 'Invalid Data', 'Message_Code': 'ID', 'Status': 'Failure'},indent=4))
    except:
        return(json.dumps({"Message":"Record Updated Unsuccessful","Message_Code":"RUUS","Service_Status":"Success"},indent=4))  

def update_doctorprofile(request):
    try:
        doctors = request.json
        w_time={}
        w_time['average_waiting_time']=doctors['average_waiting_time']
        
        speclaization = doctors['Specialization']
        service = doctors['services']
        day = doctors['days']
        doctor_id=doctors['doctor_id']
        doc_record = {k : v for k,v in doctors.items() if k not in ('Specialization','services','days','business_id','average_waiting_time','doctor_id')}
        print(doc_record )
        doctor = {k : v for k,v in doctors.items() if k  in ('doctor_profile_id')}
        print('mohan',doctor)
        doctorid = json.loads(dbget("select count(*) as doctor_id from new.doctor_profile where doctor_profile_id  ='"+(doctors['doctor_profile_id'])+"'"))
        print(doctorid)
        #businessid = json.loads(dbget("select count(*) as business_id from new.business_profile where business_id ='"+str(doctors['business_id'])+"'"))
        #if doctorid[0]['doctor_id'] == 1 and businessid[0]['business_id'] == 1 and  len(speclaization) != 0 and len(service) != 0:
        if 1==1:
            doc = doctor.get('doctor_profile_id')
            print(doc)
            #doc_record['doctor_profile_id'] = doctors['doctor_name'][:4]+str(doctor.get('doctor_profile_id'))
            print(doc_record)
            gensql('update','new.doctor_profile',doc_record,doctor)
            doc_profile_id = doc_record['doctor_profile_id']
            print(doc_profile_id)
            d = {'doctor_id':doc_profile_id}
           
            dbput("delete from new.doctor_specialization where doctor_id='"+str(doc_profile_id)+"'")
            for sep in speclaization:
                i = {}
                i['specialization_id'] = sep
                i['doctor_id'] = doc_profile_id
                gensql('insert','new.doctor_specialization',i)
            dbput("delete from new.doctor_services where doctor_id='"+str(doc_profile_id)+"'")    
            for ser in service:
                i = {}
                i['doctor_id'] = doc_profile_id
                i['service_id'] = ser
                print('qwertyu',i)
                gensql('insert','new.doctor_services',i)
           
            #businessid = json.loads(dbget("select count(*) as bus_id from new.timing where business_id='"+(doctors['business_id'])+"'"))
            dbput("delete from new.timing where doctor_id='"+doc_profile_id+"' and business_id='"+doctors['business_id']+"' ")
            for tim in day:
                print(day)
                tim['doctor_id'] = doc_profile_id
                tim['business_id'] = doctors['business_id']
                gensql('insert','new.timing',tim)
    
                #print(wait_time)
            avg={}
            print(avg)
            print(doctor_id)
            avg['doctor_id'] = doctor_id
            print(avg)
            avg['business_id'] = doctors['business_id']
            print('avg', avg)
            #print(average_waiting_time, type(average_waiting_time))
            gensql('update','new.doctorinbusiness', w_time ,avg)

            
            return(json.dumps({"Message":"Recored Updated Successfully","Message_Code":"RUS","Service_Status":"Success"},indent=4))
        else:
            return(json.dumps({'Message': 'Invalid Data', 'Message_Code': 'ID', 'Status': 'Failure'},indent=4))
    except:
       return(json.dumps({"Message":"Record Updated Unsuccessful","Message_Code":"RUUS","Service_Status":"Success"},indent=4))  

    
def update_businessanddoctors(request):
    try:
        d = request.json
        docinbusid = json.loads(dbget("select count(*) as docbus_id from new.doctorinbusiness where docinbus_id ='"+d['docinbus_id']+"'"))
        if docinbusid[0]['docbus_id'] == 1:
            b={k : v for k,v in d.items() if k in ('docinbus_id')}
            c={ k : v for k,v in d.items() if k  not in('docinbus_id')}
            gensql('Update','new.doctorinbusiness',b,c)
            return(json.dumps({"Message":"Recored Updated Successfully","Message_Code":"RUS","Service":"Success"},indent=4))
        else:
            return(json.dumps({'Message': 'Invalid Data', 'Message_Code': 'ID', 'Status': 'Failure'},indent=4))
    except:
        return(json.dumps({"Message":"Record Updated Unsuccessful","Message_Code":"RUUS","Service_Status":"Success"},indent=4))
def updatedocspecialization(request):
    try:
        d=request.json
        a= { k : v for k,v in d.items() if k not in ('specialization_id')}
        e={ k : v for k,v in d.items() if k in ('specialization_id')}
        gensql('update','new.doctor_specialization',a,e)
        return(json.dumps({"Message":"Record Updated Successfully","Message_Code":"RUS","Service_Status":"Success"},indent=4))
    except:
        return(json.dumps({"Message":"Record Updated Unsuccessful","Message_Code":"RUUS","Service_Status":"Success"},indent=4))               
            
def updatedocservices(request):
    try:
        d=request.json
        a= { k : v for k,v in d.items() if k not in ('service_id')}
        e={ k : v for k,v in d.items() if k in ('service_id')}
        gensql('update','new.doctor_services',a,e)
        return(json.dumps({"Message":"Record Updated Successfully","Message_Code":"RUS","Service_Status":"Success"},indent=4))
    except:
        return(json.dumps({"Message":"Record Updated Unsuccessful","Message_Code":"RUUS","Service_Status":"Success"},indent=4))
def selectdoctorprofile(request):
    d = request.json
        
    doctor = json.loads(dbget("select count(*) as doc_id from new.doctor_profile where doctor_profile_id ='"+d['doctor_id']+"'"))
    print(doctor)
    business = json.loads(dbget("select count(*) as bus_id from new.business_profile where business_id ='"+str(d['business_id'])+"'"))
             
    if doctor[0]['doc_id'] == 1 and business[0]['bus_id'] == 1:
        output=json.loads(dbget("select new.doctor_profile.*,new.doctorinbusiness.average_waiting_time \
                                 from new.doctor_profile join new.doctorinbusiness on new.doctor_profile.\
                                 doctor_profile_id=new.doctorinbusiness.doctor_id\
                                where doctor_profile_id='"+str(d['doctor_id'])+"'" ))
        output[0]['timing'] = json.loads(dbget("select new.timing.start_timing,new.timing.end_timing,new.timing.day,new.timing.session  \
                                                from new.timing where doctor_id='"+d['doctor_id']+"'"))
                                  
        
        output[0]['specialization']=json.loads(dbget("select new.doctor_specialization.specialization_id,new.specialization.\
                                                     specialization_name from new.doctor_specialization join new.specialization on \
                                                     doctor_specialization.specialization_id=new.specialization.specialization_id where doctor_id='"+d['doctor_id']+"'"))

        output[0]['services']=json.loads(dbget("select new.doctor_services.service_id,new.services.\
                                                     service_name from new.doctor_services join new.services on \
                                                     doctor_services.service_id=new.services.service_id where doctor_id='"+d['doctor_id']+"'"))
        return(json.dumps({"Message":"Record Selected Successfully","Message_Code":"RSS","Service_Status":"Success","output":output},indent=4))
    
