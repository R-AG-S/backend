ACTIVE_CARPOOL_TABLE = 'Active-Sessions'

INACTIVE_SESSIONS_TABLE = 'Session-History'

def init_inactive_table():
    return {
                'session_count': 0,
                'history': [],
                'last_session': "",
                "distance_travelled_split": [],
                "cost_split": []
            }