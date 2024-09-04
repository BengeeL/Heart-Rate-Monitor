# GROUP 1

# Benjamin 
# Paige
# Harpreet
# Gwen 

from time import asctime
from json import dumps
from group_1_User import User

class Utils:
    def __init__(self):
        self.start_id = 0

    def get_json_data(self, heart_rate: int, user: User):
        self.start_id += 1
        data = {
            'packet_id': self.start_id, 
            'timestamp': asctime(), 
            'heart_rate': heart_rate, 
            'user': user.get_user()
            }
        return dumps(data, indent=2)
