from PayUp.firebase import messaging

#####################

from PayUp.firebase import db
from carpool.models import Carpool_Table

def fcm_bulk_notification(registration_tokens: list, payload):

    message = messaging.MulticastMessage(
        data=payload,
        tokens=registration_tokens,
    )
    response = messaging.send_multicast(message)
    return response


def fcm_single_notification(registration_token: str, payload: str):

    message = messaging.Message(
        data=payload,
        token=registration_token,
    )
    response = messaging.send(message)
    return response

#######################


def start_drive_notif(room_id, driver_uid="Driver"):
    
    message = {driver_uid: "An active carpool session has been started by "+ driver_uid}

    carpool_ref = db.collection('User-Details')
    query = carpool_ref.where(u'rooms', u'array_contains', room_id)
    docs = query.get()
    token_list = []

    for doc in docs:
        user_details = doc.to_dict()
        if 'device_notif_token' in user_details:
            token_list.append(user_details['device_notif_token'])
        # TODO: Remove Driver from this.

    if token_list:
        
        resp = fcm_bulk_notification(token_list, message)
        print(resp.success_count)
    else:
        print("Token List is Empty for Room " + room_id)


    

    

    