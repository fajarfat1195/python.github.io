from numpy import result_type
from src.action.sqlite_local import select, update, post
from src.normalization import setDateTime
from src.services.zoho import getRecordsByEmail
import json

def checkData(param):
    '''
    jekaterina.amatniece@gmail.com
    Email:equals:
    Phone:equals:
    Mobile:equals:
    '''
    print("Checking "+param+" In Zoho")
    ds = getRecordsByEmail({'criteria': '(('+param+') and (Brand:equals:Karma Resorts) and (Lead_Source:equals:Past Guests))'})
    if ds.status_code == 200:
        das = json.loads(ds.text)['data'][0]
        print("Checking "+param+" In Zoho", " Result : FOUND")
        das['status_code'] = 200
    else:
        print("Checking "+param+" In Zoho", " Result : NOT FOUND")
        das = {'status_code': ds.status_code}

    return das

def LeadLocations(old = [], add = ''):
    if add not in old:
        old.append(add)

    return old

def pushZoho(data: dict, id):
    from src.services.zoho import insert_records, put_records
    
    if data['Email']:
        ds = checkData('Email:equals:'+data['Email'])
        if ds['status_code'] == 204:
            print('Add New Data')
            data.update({'Lead_Locations' : [data['Lead_Locations']]})
            return insert_records(data)
            # add NEW
        else:
            print('Update Existing Data')
            loc = ds['Lead_Locations']
            if data['Lead_Locations'] not in loc:
                loc.append(data['Lead_Locations'])
            putZohomap = {
                "id" : ds['id'],
                "BookRef" : data['BookRef'],
                "Arrival_Date" : data['Arrival_Date'],
                "Departure_Date" : data['Departure_Date'],
                "Lead_Locations": loc,
            }
            result_put = put_records(putZohomap)
            if result_put['data'][0]['code'] == 'SUCCESS':
                return {'data' : [{"code": "UPDATED", 'id': ds['id']}]}
            return {'data' : [{"code": "ERROR_UPDATED", 'id': ds['id']}]}

            """ # Update 'data_guesline' process_status = WAITING & IDzoho = ds['id']
            # update('data_guestline', 'process_status="WAITING",IDzoho="'+str(ds['id'])+'"', 'id='+str(id))
            print('WAITING UPDATE : ', ds['id'])

            # loc = checkInZohoMobile['Lead_Locations']
            # if data['Lead_Locations'] not in loc:
            #     loc.append(data['Lead_Locations'])
            # Skipp Add
            return {'data' : [{"code": "WAITING", 'id': ds['id']}]} """
    else:
        ds = checkData('Phone:equals:'+data['Phone'])
        if ds['status_code'] == 204:
            print('Add New Data - Phone Only')
            data.update({'Lead_Locations' : [data['Lead_Locations']]})
            return insert_records(data)
        else:
            print('Update Existing Data - Phone Only')
            loc = ds['Lead_Locations']
            if data['Lead_Locations'] not in loc:
                loc.append(data['Lead_Locations'])
            putZohomap = {
                "id" : ds['id'],
                "BookRef" : data['BookRef'],
                "Arrival_Date" : data['Arrival_Date'],
                "Departure_Date" : data['Departure_Date'],
                "Lead_Locations": loc,
            }
            result_put = put_records(putZohomap)
            if result_put['data'][0]['code'] == 'SUCCESS':
                return {'data' : [{"code": "UPDATED", 'id': ds['id']}]}
            return {'data' : [{"code": "ERROR_UPDATED", 'id': ds['id']}]}


def runner(data: dict, id):
    pr = pushZoho(data, id)
    if pr['data'][0]['code'] == 'SUCCESS':
        IDzoho = pr['data'][0]['details']['id']
        update('data_guestline', 'process_date="'+setDateTime()+'",process_status="SUCCESS",IDzoho="'+str(IDzoho)+'"', 'id='+str(id))
    elif pr['data'][0]['code'] == 'INVALID_DATA':
        print(pr['data'])
        update('data_guestline', 'process_date="'+setDateTime()+'",process_status="ERROR",process_note="INVALID_DATA"', 'id='+str(id))
    elif pr['data'][0]['code'] == 'ERROR_UPDATED':
        print(pr['data'])
        update('data_guestline', 'process_date="'+setDateTime()+'",process_status="ERROR",process_note="ERROR_UPDATED"', 'id='+str(id))
    elif pr['data'][0]['code'] == 'UPDATED':
        IDzoho = pr['data'][0]['id']
        update('data_guestline', 'process_date="'+setDateTime()+'",process_status="UPDATED",process_note="FOUND",IDzoho="'+str(IDzoho)+'"', 'id='+str(id))
def boolConv(x):
    if x == 0:
        return False
    else:
        return True

def loop():
    from src.services.zoho import getAuthRefresh

    data = select('data_guestline','*','Odyssey_Members = False AND meta_id >= 190 AND process_status="Pendding" AND (Email !="" OR Phone != "" OR Mobile !="") LIMIT 100')
    if len(data) != 0:
        for rw in data:
            print(rw['id'])
            zohomap = {
                "BookRef" : rw['BookRef'],
                "PrimaryGuestProfileRef" : rw['PrimaryGuestProfileRef'],
                "Destination" : rw['Lead_Locations'],
                "Language" : rw['Language'],
                "Brand": rw['Brand'],
                "Lead_Sub_Brand": rw['Lead_Sub_Brand'],
                "Lead_Source": rw['Lead_Source'],
                "Lead_Source_Description": rw['Lead_Source_Description'],
                "Lead_Locations": rw['Lead_Locations'],
                "Guest_Type": rw['Guest_Type'],
                "Booking_Status" : rw['Booking_Status'],
                "Arrival_Date" : rw['Arrival_Date'],
                "Departure_Date" : rw['Departure_Date'],
                "Street" : rw['Street'],
                "Street2" : rw['Street2'],
                "City": rw['City'],
                "State": rw['State'],
                "Country": rw['Country'],
                "Nationality": rw['Nationality'],
                "Zip_Code": rw['Zip_Code'],
                "Phone": rw['Phone'],
                "Mobile": rw['Mobile'],
                "Email": rw['Email'],
                "Salutation" : rw['Salutation'],
                "First_Name": rw['First_Name'],
                "Last_Name": rw['Last_Name'],
                "Gender": rw['Gender'],
                "Media_Source_Code": rw['Media_Source_Code'],
                "Market_Segment": rw['Market_Segment'],
                "Adult": str(rw['Adult']),
                "Children": str(rw['Children']),
                "Contact_type" : [rw['Contact_type']],
                "Email_Opt_In": boolConv(rw['Email_Opt_In']),
                "Email_Opt_Out": boolConv(rw['Email_Opt_Out']),
                "Do_Not_Mail": boolConv(rw['Email_Opt_Out']),
                "Email_status" : [rw['Email_status']]
            }
            # print(zohomap)
            runner(zohomap, rw['id'])
        loop()
    else:
        print("DONE")
        
    print("DONE")

# HELL START
loop()

# ds = checkData("Email:equals:cassandra@tgfineart.com")
# print(ds)