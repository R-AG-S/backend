from .services import get_active_room_if_room_valid
from .serializers import active_session_parser
def get_active_session_data(room_id, user_id):
    
    active_room_ref = get_active_room_if_room_valid(room_id, user_id, must_exist=True)
    session_data = active_room_ref.get().to_dict()

    parsed_data = active_session_parser(session_data)

    return {"SESSION_DETAILS": parsed_data}