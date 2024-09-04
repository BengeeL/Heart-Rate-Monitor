# GROUP 1

# Benjamin 
# Paige
# Harpreet
# Gwen 

class User:
    def __init__(self, name, username):
        self.name = name
        self.username = username

    def get_user(self):
        data = {'name': self.name, 'username': self.username}
        return data
