class profile:
    name = 0
    surname = 0
    reg_date = 0
    date_last_request = 0
    user_city = 0

    def __init__(self, name, surname,user_city,reg_date,date_last_request):
        self.name = name
        self.surname = surname
        self.reg_date = reg_date
        self.date_last_request = date_last_request
        self.user_city = user_city

    def get_name_and_surname(self,name,surname):
        self.name = name
        self.surname = surname


    def get_user_city(self,user_city):
        self.user_city = user_city