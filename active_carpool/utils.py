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


def topic_notification(room_id, payload):
    topic = room_id
    # See documentation on defining a message payload.
    message = messaging.Message(
        data=payload,
        topic=topic,
    )
    # Send a message to the devices subscribed to the provided topic.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    return response

def topic_subscribe(reg_token, topic):
    # These registration tokens come from the client FCM SDKs.
    registration_tokens = reg_token

    # Subscribe the devices corresponding to the registration tokens to the
    # topic.
    response = messaging.subscribe_to_topic(registration_tokens, topic)
    # See the TopicManagementResponse reference documentation
    # for the contents of response.
    print(response.success_count, 'tokens were subscribed successfully')


def fcm_single_notification(registration_token: str, payload: str):

    message = messaging.Message(
        data=payload,
        token=registration_token,
    )
    response = messaging.send(message)
    return response

#######################

# Public functions


def start_drive_notif(room_id, driver_uid="Driver"):
    
    message = {driver_uid: "An active carpool session has been started by "+ driver_uid}

    carpool_ref = db.collection('User-Details')
    query = carpool_ref.where(u'rooms', u'array_contains', room_id)
    docs = query.get()
    token_list = []

    topic = topic_notification(room_id, {driver_uid: "An active carpool session has been started by "+ driver_uid, 'time': '2:45'})

    for doc in docs:
        user_details = doc.to_dict()
        print("->", user_details['displayname'])
        if 'device_notif_token' in user_details:
            token_list.append(user_details['device_notif_token'])
        # TODO: Remove Driver from this.

    if token_list:
        
        resp = fcm_bulk_notification(token_list, message)
        print(resp.success_count)
        return {"SUCCESS": "Devices Reached: " + str(resp.success_count), "MESSAGE": message, "TOPIC": topic}
    else:
        print("Token List is Empty for Room " + str(room_id))
        return {"ERROR": "Token List is Empty for Room " + str(room_id)}


    


    

    

    