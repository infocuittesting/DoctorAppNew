from sqlwrapper import gensql, dbget, dbput
import json
import datetime
from datetime import timedelta
from flask import Flask, request, jsonify
def weeklyreport(request):
    try:
        d = request.json
        list1 = []
        currentdate = datetime.datetime.now().date() 
        fromdate=currentdate-timedelta(days=currentdate.weekday()) 
        todate= fromdate+timedelta(days=7)
        while fromdate!=todate:
            b_count = json.loads(dbget("select count(token_status) filter (where token_status='Booked') as b_count,\
                count(token_status) filter (where token_status='Cancel') as c_count,\
                count(token_status) filter (where token_status='Checkout') as co_count\
                from new.appointment where doctor_id='" + str(d['doctor_id']) + "' and business_id = '" + str(d['business_id']) + "'\
                and new.appointment.business_date = '" + str(fromdate) + "'"))
            booked_count = b_count[0]['b_count']
            canceled_count = b_count[0]['c_count']
            cheout_count = b_count[0]['co_count']
            dic = {"period":str(fromdate),"booked_count": booked_count, "canceled_count": canceled_count, "Checked_out": cheout_count}
            list1.append(dic)
            fromdate=fromdate+timedelta(days=1)
        return (json.dumps({"Message": "Token number Counted  Sucessfully","Message_Code": "TNS", "Service_Status": "Success","ReturnValue":list1},indent=4))
    except:
        return (json.dumps({"Message": "Token number  Counted UnSuccessful", "Message_Code": "TNUS", "Service_Status": "Failure"},indent=4))
def locationreport(request):
    try:
        d = request.json
        count = json.loads(dbget("select distinct city,count(city) as city_count from new.appointment join new.user_profile on new.appointment.mobile=new.user_profile.mobile\
                                     where doctor_id='"+d['doctor_id']+"' and business_id = '" + str(d['business_id'])+"' group by city"))
        return (json.dumps({"Message": "City Counted  Sucessfully","Message_Code": "CCS", "Service_Status": "Success","ReturnValue":count},indent=4))
    except:
        return (json.dumps({"Message": "City  Counted UnSuccessful", "Message_Code": "CCUS", "Service_Status": "Failure"},indent=4))
def weekdayreport(request):
    try:
        d = request.json
        list1 = []
        currentdate = datetime.datetime.now().date() 
        fromdate=currentdate-timedelta(days=currentdate.weekday()) 
        todate= fromdate+timedelta(days=7)
        while fromdate!=todate:
            b_count = json.loads(dbget("select count(token_status) filter (where token_status='Booked') as b_count,\
                count(token_status) filter (where token_status='Cancel') as c_count,\
                count(token_status) filter (where token_status='Checkout') as co_count\
                from new.appointment where doctor_id='" + str(d['doctor_id']) + "' and business_id = '" + str(d['business_id']) + "'\
                and new.appointment.business_date = '" + str(fromdate) + "'"))
            booked_count = b_count[0]['b_count']
            canceled_count = b_count[0]['c_count']
            cheout_count = b_count[0]['co_count']
            dic = {"period":str(fromdate.strftime("%a")),"booked_count": booked_count, "canceled_count": canceled_count, "Checked_out": cheout_count}
            list1.append(dic)
            fromdate=fromdate+timedelta(days=1)
        return (json.dumps({"Message": "Token number Counted  Sucessfully","Message_Code": "TCS", "Service_Status": "Success","ReturnValue":list1},indent=4))
    except:
        return (json.dumps({"Message": "Token number  Counted UnSuccessful", "Message_Code": "TCUS", "Service_Status": "Failure"},indent=4))
def token_report(request):
    try:
        d = request.json
        token_count = json.loads(dbget("select token_status,count(*) from new.appointment where doctor_id='" + str(d['doctor_id']) + "'\
        and business_id = '" + str(d['business_id']) + "'\
        and business_date = '" + str(d['business_date']) + "' group by token_status"))  
        return (json.dumps({"Message": "Token_status Counted  Sucessfully", "Message_Code": "TCS", "Service_Status": "Success"
                                , "token_status": token_count},indent=4))

    except:
        return (json.dumps({"Message": "Token_status Counted UnSuccessful", "Message_Code": "TCUS", "Service_Status": "Failure"},indent=4))
def illness_report(request):
    try:
        d = request.json
        illness_status = json.loads(dbget("select reason,count(*) from new.appointment where doctor_id='" + str(d['doctor_id']) + "'\
        and business_id = '" + str(d['business_id']) + "' group by reason"))
       
        return (json.dumps({"Message": "Illness Counted  Sucessfully", "Message_Code": "ICS", "Service_Status": "Success"
                                , "illness_count": illness_status},
                            indent=4))
    except:
        return (json.dumps({"Message": "Illness Counted UnSuccessful", "Message_Code": "ICUS", "Service_Status": "Failure"},indent=4))
def channel_report(request):
    try:
        d = request.json
        channel_status = json.loads(dbget("select channel,count(*) from new.appointment where doctor_id='" + str(d['doctor_id']) + "'\
        and business_id = '" + str(d['business_id']) + "' group by channel"))
       
        return (json.dumps({"Message": "illness Counted  Sucessfully", "Message_Code": "CCS", "Service_Status": "Success"
                                , "illness_count": channel_status},
                            indent=4))
    except:
        return (json.dumps({"Message": "channel Counted UnSuccessful", "Message_Code": "CCUS", "Service_Status": "Failure"},indent=4))
def latlong_report(request):
    try:
        d = request.json
        count = json.loads(dbget("select distinct new.user_profile.area,new.user_profile.location_lat,new.user_profile.location_long from new.appointment\
                                 join new.user_profile on new.appointment.mobile=new.user_profile.mobile\
                                     where doctor_id='"+d['doctor_id']+"' and business_id = '" + str(d['business_id'])+"'"))
        return (json.dumps({"Message": "Latlong Selected  Sucessfully","Message_Code": "LSS", "Service_Status": "Success","ReturnValue":count},indent=4))
    except:
        return (json.dumps({"Message": "latlong  Selected UnSuccessful", "Message_Code": "LSUS", "Service_Status": "Failure"},indent=4))
        
