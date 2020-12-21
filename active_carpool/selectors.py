from .services import get_active_room_if_room_valid, get_history_if_room_valid
from .serializers import active_session_parser


def get_active_session_data(room_id, user_id):
    
    active_room_ref = get_active_room_if_room_valid(room_id, user_id, must_exist=True)
    session_data = active_room_ref.get().to_dict()

    parsed_data = active_session_parser(session_data)

    return {"SESSION_DETAILS": parsed_data}


def get_history_data(room_id, user_id):
    
    history_ref = get_history_if_room_valid(room_id, user_id, must_exist=True)
    session_data = history_ref.get().to_dict()
    session_data['sessions'] = []
    for session in session_data['history']:
        session_data['sessions'].append(active_session_parser(session))

    session_data['sessions'] = sorted(session_data['sessions'], key = lambda i: (i['end_time']), reverse=True)

    session_data.pop('history', None)
    
    return {"SESSION_DETAILS": session_data}

