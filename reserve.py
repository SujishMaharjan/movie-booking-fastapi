from database import *

class Reservation:

    def __init__(self,reserve_id,user_id,username,movie_id,movie_name,booked_seats):
        self._reserve_id = reserve_id
        self._user_id = user_id
        self._username = username
        self._movie_id = movie_id
        self._movie_name = movie_name
        self._booked_seats = booked_seats

    def return_data_after_reserve(self):
        return {'reserve_id':self._reserve_id,'username':self._username,} 

    def reserve_seats(self,DATABASE,db_type):
        json_data = Database.read_json(DATABASE,db_type)

        #getting the data to modify in existing data
        reserve_dict = self.__dict__
        
        #removing the leading _ in key
        cleaned_dict = {key.lstrip('_'): value for key, value in reserve_dict.items()}

        json_data[self._reserve_id] = cleaned_dict
        if Database.write_json(DATABASE,db_type,json_data):
            return self._reserve_id
        else:
            return None
        
    def unreserve_seats(self,DATABASE,db_type,no_of_seats):
        json_data = Database.read_json(DATABASE,db_type)
        self._booked_seats -= no_of_seats
        if self._booked_seats == 0:
            json_data.pop(self._reserve_id)
        else:
            #getting the data to modify in existing data
            reserve_dict = self.__dict__
            
            #removing the leading _ in key
            cleaned_dict = {key.lstrip('_'): value for key, value in reserve_dict.items()}
            json_data[self._reserve_id] = cleaned_dict
        if Database.write_json(DATABASE,db_type,json_data):
            return self._reserve_id
        else:
            return False


    @property
    def booked_seats(self):
        return self._booked_seats
    
    @booked_seats.setter
    def booked_seats(self,booked_seats):
        self._booked_seats = booked_seats


    


