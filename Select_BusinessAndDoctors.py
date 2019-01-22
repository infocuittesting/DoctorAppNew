from sqlwrapper import gensql,dbget,dbput
import json
from datetime import datetime
import time
from flask import Flask,request,jsonify

def Select_BusinessandDoctors(request):
  try:
    st_time = time.time()
    d = request.json
    # Get all business profile from db dpends on county and city
    business = json.loads(dbget("SELECT * FROM new.business_profile where country='"+d['country']+"'"
                                " and city='"+d['city']+"' "))
    #print(business)
    specialist_type = list(set(bus['specialist'] for bus in business))
    print(specialist_type)
    specialist = []
    doc_only_specialist = {}
    #This loop segregate business based on specialist
    for bus in business:
      #print(bus)
      typeofspecialist = bus['specialist']
      index_no = specialist_type.index(typeofspecialist)
      try:
         bus['cli_img'] = ""
         bus.update({"cli_subimages1":"","cli_subimages2":"","cli_subimages3":""})
         bus['cli_feedback'] = json.loads(dbget("select count(*) from new.feedback where "
                                                "business_id='"+str(bus['business_id'])+"'"))[0]['count']
         bus['cli_doc_count'] = json.loads(dbget("select count(*) from new.doctorinbusiness where "
                                                 "business_id='"+str(bus['business_id'])+"'"))[0]['count']
         specialist[index_no].append(bus)
      except:
          bus['cli_img'] = ""
          bus.update({"cli_subimages1": "", "cli_subimages2": "", "cli_subimages3": ""})
          bus['cli_feedback'] = json.loads(dbget("select count(*) from new.feedback where "
                                                 "business_id='"+str(bus['business_id'])+"'"))[0]['count']
          bus['cli_doc_count'] = json.loads(dbget("select count(*) from new.doctorinbusiness "
                                                  "where business_id='"+str(bus['business_id'])+ "'"))[0]['count']
          specialist.append([bus])

    #print("sp",specialist)
    # Main  loop
    for i in specialist:
        for a in i:
          b_id = a['business_id']
          #print("id",b_id)
          new_dict = {k:v for k,v in a.items()
                       if k in ('business_name', 'area','address','location_lat','location_long')}
          # Get the timing based on business
          timing = json.loads(dbget("select day,start_timing,end_timing from new.timing "
                                                        "where business_id='"+str(a['business_id'])+"'"
                                                        "and doctor_id='0' "))
          #print("timing",timing)
          # Loop for format timing of business profile
          for t in timing:
              timing[timing.index(t)] = {'day':t['day'],
                                         'time':""+datetime.strptime(t['start_timing'], "%H:%M").strftime("%I:%M %p")+"-"
                                                ""+datetime.strptime(t['start_timing'], "%H:%M").strftime("%I:%M %p")+""}
          new_dict['clinic_images'] = [{"img":""},{"img":""},{"img":""}]
          new_dict['clinic_timings'] = timing
          doctorinbusiness = json.loads(dbget("select * from new.doctor_profile where "
                                              "doctor_profile_id in (select doctor_id from "
                                              "new.doctorinbusiness where business_id='"+str(b_id)+"')"))

          # Doctor details inside the business details
          for docinbus in doctorinbusiness:
              docinbus['doctor_details'] = [docinbus.copy()]
              doc_timing = json.loads(dbget("select day,start_timing,end_timing from new.timing "
                                        "where business_id='"+str(a['business_id'])+"'"
                                        "and doctor_id='"+docinbus['doctor_profile_id']+"' "))
              #print("doc timing", doc_timing)
              # Loop for format timing of doctor profile
              for t in doc_timing:
                  #print("t",t,type(t))
                  doc_timing[doc_timing.index(t)] = {'day': t['day'],
                                                 'time': ""+datetime.strptime(t['start_timing'], "%H:%M").strftime("%I:%M %p")+"-"
                                                         ""+datetime.strptime(t['start_timing'],"%H:%M").strftime("%I:%M %p")+""}
                  #print("doc_timing", doc_timing,type(doc_timing))
              docinbus['doctor_details'][0]['doctorstimings'] = doc_timing
              docinbus['doctor_details'][0]['doctor_clinic'] = json.loads(dbget("select * from new.business_profile where "
                                                                                " business_id in (SELECT business_id FROM new.doctorinbusiness "
                                                                                " where doctor_id='"+docinbus['doctor_profile_id']+"')"))
              docinbus['doctor_details'][0]['doctor_feedback'] = json.loads(dbget("select * from new.feedback where business_id"
                                                                                "='"+str(a['business_id'])+"'"
                                                                                " and doctor_id='"+docinbus['doctor_profile_id']+"'"))
              docinbus['doctor_details'][0]['doctor_clinic_img'] = [{"img":""},{"img":""},{"img":""}]
              docinbus['doctor_details'][0]['doctor_specialization'] = json.loads(dbget("SELECT new.specialization.* "
                                                                                        " FROM new.doctor_profile join new.doctor_specialization on"
                                                                                        " doctor_profile.doctor_profile_id = doctor_specialization.doctor_id"
                                                                                        " join new.specialization on doctor_specialization.specialization_id = "
                                                                                        " specialization.specialization_id"
                                                                                        " where doctor_profile.doctor_profile_id='"+str(a['business_id'])+"'"))

              docinbus['doctor_details'][0]['doctor_services'] = json.loads(dbget("SELECT new.services.* "
                                                                                  " FROM new.doctor_profile join new.doctor_services on"
                                                                                  " doctor_profile.doctor_profile_id = doctor_services.doctor_id"
                                                                                  " join new.services on doctor_services.service_id = services.service_id"
                                                                                  " where doctor_profile.doctor_profile_id='"+str(a['business_id'])+"'"))
          new_dict['clinic_doctor_list'] = doctorinbusiness

          for doc in doctorinbusiness:
              #if doc['specialist'] not in doc_only_specialist:
              #    doc_only.append(doc)
              try:
                 print("try")
                 print(doc_only_specialist[''+doc['specialist']+''])
                 doc_only_specialist[''+doc['specialist']+''].append(doc)
              except:
                  print("except")
                  doc_only_specialist[''+doc['specialist']+''] = [doc]

          # Get service data for business profile
          bus_service = json.loads(dbget("select new.services.* from new.doctor_services"  
                                                         " join new.services"
                                                         " on doctor_services.service_id = services.service_id where" 
                                                         " new.doctor_services.doctor_id" 
                                                         " in (select doctor_id from new.doctorinbusiness" 
                                                         " where business_id='"+str(b_id)+"') "))
          service = []
          service_set = set()
          # Loop for format service datas for business  profile
          for b_ser in bus_service:
              if b_ser['service_name'] not in service_set:
                  service.append({"service":b_ser['service_name']})
                  service_set.add(b_ser['service_name'])

          new_dict['clinic_services'] = service
          new_dict['clinic_open'] = "Open Today"
          a["clinic_details"] = [new_dict]

        print("doc_only_specialist",doc_only_specialist)
        if i[0]['specialist'] in doc_only_specialist:
            doc_list = doc_only_specialist["" + i[0]['specialist'] + ""]
        else:
            doc_list = []
        specialist[specialist.index(i)] = {"name":i[0]['specialist'],"icon":"","Listofdoctors":[{"clinics":i,
                                           "Doctors":doc_list}]}
        print("sm_sp",specialist)
    ed_time=time.time()
    full_time = ed_time - st_time
    print("spcialist", specialist)
    print("Time Taken",full_time)
    return (json.dumps(
        {"Message": "Records Selected Sucessfully", "Message_Code": "RSS",
         "Service_Status": "Success","specialist":specialist}, indent=4))
  except:
      return (json.dumps(
          {"Message": "Records Un Selected Sucessfully", "Message_Code": "RUS",
           "Service_Status": "Success", "specialist": specialist}, indent=4))
