# myapp/utils.py

class CustClass:
    
    def __init__(self, user):
        self.user = user
        self.is_staff=user.is_staff
        self.is_authenticated=user.is_authenticated and not user.is_staff and user.is_active
    
    
