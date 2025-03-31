import json,os
from database.database import Database
from archive.contextmanager import ContextManager
from archive.person import *
from archive.movie import Movie
import uuid
from functions import *
from archive.reserve import Reservation


DATABASE = {
    "DB_FOLDER" : "Database",
    "DB_FILES" : {
        "db_users": "user.json",
        "db_movies":"movie.json",
        "db_reserves":"reserve.json",
        "db_relations":"relation.json"
    }
}



INPUT_STRING = """
ENTER 1 TO CREATE DATABASE:
ENTER 2 TO CREATE USERS:
ENTER 3 TO ADD MOVIES:
ENTER 4 TO RESERVE MOVIES:
ENTER 5 TO UNRESERVE MOVIES:

PRESS 0 TO EXIT:

"""


if __name__ == "__main__":

    while True:
        choice = int(input(INPUT_STRING))
        match choice:
            case 1:
                Database.create_database(DATABASE)

            case 2:
                try:
                    choice = int(input("Enter 1 to add admin and 2 add Member:"))
                except Exception as e:
                    print(e)
                    continue
                if choice not in (1,2):
                    print("Invalid choice")
                    continue
                
                #getting user_data from users.json database
                user_data_json = Database.read_json(DATABASE,"db_users")

                #sending user_data_json to check if there is such username while input and
                # generating new user_id
                user_details = Functions.input_user_data(user_data_json)
                user_details["user_id"] =str(uuid.uuid1())

                #creating instance using **kwargs so that order of dictionary keys won't matter
                p = Admin(**user_details) if choice == 1 else Member(**user_details) if choice == 2 else print("Invalid choice")
                token = p.add_person(DATABASE,"db_users")
                if not token:
                    print("Failed to add person")
                else:
                    p.add_relation(DATABASE,"db_relations",token,p.permission)
                    print(f"Successfully added username {user_details['username']}") 
                 


            case 3:

                print(f"Please login you admin credentials to add movies")
                input_dict = Functions.input_data_from_custom_fields(["username","password"])
                username,password = input_dict.values()
                user_details,token = Functions.login(DATABASE,"db_users",username,password)

                relation_data = Database.read_json(DATABASE,"db_relations")
                movie_data = Database.read_json(DATABASE,'db_movies')

                if token in relation_data and relation_data[token]["permission"] == "admin":
                    a = Person(**user_details)
                    movie_details = Functions.input_data_from_custom_fields(["movie_name","movie_description"])
                    movie_details["movie_status"] = "Available"
                    movie_details["added_by_admin_id"] = a.user_id
                    movie_details["movie_id"] = str(uuid.uuid4())

                    m = Movie(**movie_details)
                    # movie_token =  m.add_movie(filepath_mov)
                    if not m.add_movie(DATABASE,"db_movies"):
                        print(f"Error occured while adding movies")
                    else:
                        print(f"{movie_details['movie_name']} is added successfully in database")
                else:
                    print("Invalid token")




            case 4:
                #Anyone can view available movies at first
                Functions.view_movies(DATABASE,'db_movies')

                choice =int(input("Press 1 to reserve Movies:"))
                if choice == 1:
                    pass
                else:
                    print("Invalid choice")
                    break

                

                print("Enter your member credentials to reserve the movies:")
                input_details_dict = Functions.input_data_from_custom_fields(["username","password"])
                username,password = input_details_dict.values()
                user_details,token = Functions.login(DATABASE,'db_users',username,password)

                #loading all necessary data from database for reserving movies
                relation_data = Database.read_json(DATABASE,'db_relations')
                movie_data = Database.read_json(DATABASE,'db_movies')
                reserve_data = Database.read_json(DATABASE,'db_reserves')

                #checking if there is such token which is associated with member_data_type
                print(token)
                if token in relation_data and relation_data[token]["permission"] == "member":
                    p = Person(**user_details)
                    reserve_details = {}
                    reserve_details["reserve_id"] = str(uuid.uuid4())
                    reserve_details["user_id"] = p.user_id
                    reserve_details["username"] = p.username
                    movie_name = input("Enter movie_name you want to reserve:")
                    reserve_details["movie_name"] = movie_name
                    if movie_name  in movie_data and movie_data[movie_name]["movie_status"] == "Available":

                        #creating movie instance so that updating movie_seats of that movie, reserve then only adding reserve movies
                        movie_details = movie_data[movie_name]
                        m = Movie(**movie_details)

                        while True:
                            no_of_seats = int(input("Enter the no_of_seats you want to reserve:"))
                            if no_of_seats <= m.available_seats:
                                break
                            else:
                                print(f"Please enter valid seat, {m.available_seats} available")

                        if m.update_booked_seats(DATABASE,"db_movies",no_of_seats,0):
                            result = Functions.check_same_user_id_with_same_movie_id(reserve_data,p.user_id,m.movie_id)
                            print(result)
                            if result:
                                r = Reservation(**result)
                                r.booked_seats = r.booked_seats + no_of_seats
                            else:
                                r = Reservation(**reserve_details,movie_id=m.movie_id,booked_seats=no_of_seats)
                            r.reserve_seats(DATABASE,"db_reserves")

                        else:
                            print("Failed to update booked_seats")
                    
                        

                        
                        

                        #  if p.username in reserve_data and 
                        
                    # [movie_data[key]=movie for key,movie in movie_data.items() if movie['status']=="Available"]:
                    else:
                        print("error:Invalid Movie Entered")
                else:
                    print("Invalid Token")
            



            case 5:
                #Anyone can view available movies at first
                # Functions.view_movies(DATABASE,'db_movies') 

                choice =int(input("Press 2 to Unreserve Movies:"))
                if choice == 2:
                    pass
                else:
                    print("Invalid choice")
                    break

                

                print("Enter your member credentials to Unreserve the movies:")
                input_details_dict = Functions.input_data_from_custom_fields(["username","password"])
                username,password = input_details_dict.values()
                user_details,token = Functions.login(DATABASE,'db_users',username,password)

                #loading all necessary data from database for reserving movies
                relation_data = Database.read_json(DATABASE,'db_relations')
                movie_data = Database.read_json(DATABASE,'db_movies')
                reserve_data = Database.read_json(DATABASE,'db_reserves')
                #checking if there is such token which is associated with member_data_type
                print(token)
                if token in relation_data and relation_data[token]["permission"] == "member":
                    p = Person(**user_details)
                    # reserve_details = {}
                    # reserve_details["reserve_id"] = str(uuid.uuid4())
                    # reserve_details["user_id"] = p.user_id
                    # reserve_details["username"] = p.username
                    movie_name = input("Enter movie_name you want to unreserve:")
                    if movie_name in movie_data:
                        movie_details = movie_data[movie_name]
                        m = Movie(**movie_details)
                        reserve_details = Functions.check_same_user_id_with_same_movie_id(reserve_data,p.user_id,m.movie_id)
                        r = Reservation(**reserve_details)

                        while True:
                            no_of_seats = int(input("Enter the no_of_seats you want to unreserve:"))
                            if no_of_seats <= r.booked_seats:
                                break
                            else:
                                print(f"Please enter valid seat, booked seats {r.booked_seats} ")

                        if r.unreserve_seats(DATABASE,"db_reserves",no_of_seats):
                            m.update_booked_seats(DATABASE,"db_movies",0,no_of_seats)
                            print("Successfully unreserved movies")
                                

                        else:
                            print("Failed to unreserved movies")        
                    else:
                        print("error:Invalid Movie Entered")
                else:
                    print("Invalid Token")
            

            case 0:
                exit()

            case _:
                print("Invalid Choice")

            



    

