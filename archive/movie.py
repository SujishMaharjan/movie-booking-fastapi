from enum import StrEnum
from database.database import *

class MovieStatus(StrEnum):
    available = "Available"
    unavailable = "Unavailable"
    fully_reserved ="Fully Reserved"

class Movie:

    def __init__(self,movie_id:int,movie_name:str,movie_description:str,movie_status:MovieStatus,total_seats:int = 200,booked_seats:int = 0,available_seats:int = 200):
        self._movie_id = movie_id
        self._movie_name = movie_name
        self._movie_description = movie_description
        self._movie_status = movie_status
        self._total_seats = total_seats
        self._booked_seats = booked_seats
        self._available_seats = total_seats - booked_seats

    def add_movie(self,DATABASE,db_type):
        # loading the existing data
        json_data = Database.read_json(DATABASE,db_type)

        #getting the data to modify in existing data
        movie_dict = self.__dict__
        
        #removing the leading _ in key
        cleaned_dict = {key.lstrip('_'): value for key, value in movie_dict.items()}

        json_data[self._movie_name] = cleaned_dict
        if Database.write_json(DATABASE,db_type,json_data):
            return self._movie_id
        else:
            return False
        
    @property
    def movie_id(self):
        return self._movie_id
    
    @property
    def available_seats(self):
        return self._available_seats
    
    @property
    def booked_seats(self):
        return self._booked_seats
    

    
    def update_booked_seats(self,DATABASE,db_type,no_of_seats=0,no_of_seats_unreserve=0):
        if no_of_seats != 0:
            self._booked_seats += no_of_seats
            self._available_seats -=no_of_seats
            if self._available_seats == 0:
                self._movie_status = "Fully Reserved"
        else:
            self._booked_seats -= no_of_seats_unreserve
            self._available_seats += no_of_seats_unreserve
            if self._available_seats != 0:
                self._movie_status = "Available"

        self.add_movie(DATABASE,db_type)
        return True
        



    