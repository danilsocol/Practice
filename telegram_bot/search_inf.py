class search_inf:

    city = ""
    sphere = ""
    type_range = 0
    range = [None,None]
    step = 0

    def __init__(self, city, sphere,type_range,range,step):
        self.city = city
        self.sphere = sphere
        self.type_range = type_range
        self.range = range
        self.step = step

    def get_user_city(self,city):
        self.city = city

    def get_sphere(self,sphere):
        self.sphere = sphere

    def get_type_range(self, type_range):
        self.type_range = type_range

    def get_range(self,range):
        self.range = range

    def get_step(self,step):
        self.step += step

    def get_step_null(self):
        self.step = 0