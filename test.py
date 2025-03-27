# import json
# import os
# from database import *

# DB_FILES ={
#     "db_users": "user.json",
#     "db_movies":"movies.json",
#     "db_reserve":"reserve.json"
# }
# DB_FOLDER ="database"


# # def create_database(DB_FOLDER,DB_FILES):
    
# #     #creating the folder if it doesn't exist
# #     os.makedirs(DB_FOLDER, exist_ok=True)
# #     for key, filename in DB_FILES.items():
# #         filepath = os.path.join(DB_FOLDER,filename)
# #         try:
# #             with open(filepath,"x") as file:
# #                 json.dump({},file) # starting with an empty dictionary
# #             print(f"Created database: {filepath}")

# #         except FileExistsError as e:
# #             print(f"file already existed {filepath}")


# # def load_json(filepath,mode)


# # filepath = os.path.join(DB_FOLDER,DB_FILES['db_users'])
# # # filepath = "//{DB_FOLDER}//{DB_FILES['db_users]}"
# # user_data_json = Database.read_json(filepath)
# # # for key,sub_dict in user_data_json.items():
# # #     print(sub_dict["user_id"])

# # # #for debugging
# # # user_details = {'user_id': 3, 'username': 'sujish123', 'name': 'sujish', 'password': 'sujish456', 'person_token': '54da9a6a-63c1-4b0f-ab80-3292dc58c38esujish123'}
                

# # def generate_next_id(user_data_json):
# #     if len(user_data_json) == 0:
# #         return 0
# #     return max(sub_dict["user_id"] for _,sub_dict in user_data_json.items()) + 1

# # print(generate_next_id(user_data_json))



# # user_data_json ={
# #     "user1234567": {
# #         "user_id": 1,
# #         "username": "user1234567",
# #         "name": "Sujish Maharjan",
# #         "hashed_password": "#pass123",
# #         "person_token": "person1",
# #         "permission": "member"
# #     },
# #     "user": {
# #         "user_id": 2,
# #         "username": "user",
# #         "name": "Sujish Maharjan",
# #         "hashed_password": "#pass123",
# #         "person_token": "person1",
# #         "permission": "admin"
# #     },
# #     "user456": {
# #         "user_id": 3,
# #         "username": "user",
# #         "name": "Sujish Maharjan",
# #         "hashed_password": "#pass123",
# #         "person_token": "person1",
# #         "permission": "admin"
# #     }
# # }

# # user_admin_list = {key : sub_dict for key,sub_dict in user_data_json.items() if sub_dict['permission'] == "admin"}
# # print(user_admin_list)


# # relation_data ={
# #     "41b705b4-523d-4b08-b77a-c4f8d6137162s": {
# #         "relation_id": 0,
# #         "person_token": "41b705b4-523d-4b08-b77a-c4f8d6137162s",
# #         "permission": "admin"
# #     },
# #     "2de1abc9-4752-4741-9075-a74fa1d2bef1m": {
# #         "relation_id": 1,
# #         "person_token": "2de1abc9-4752-4741-9075-a74fa1d2bef1m",
# #         "permission": "member"
# #     }
# # }
# # person_token = "41b705b4-523d-4b08-b77a-c4f8d6137162s"
# # if person_token in relation_data and relation_data[person_token]["permission"] == "admin":
# #     print("true")
# # else:
# #     print("falses")

# user_data_json = {
#     "s": {
#         "user_id": 0,
#         "name": "s",
#         "username": "s",
#         "password": "s",
#         "person_token": "41b705b4-523d-4b08-b77a-c4f8d6137162s",
#         "permission": "admin"
#     },
#     "m": {
#         "user_id": 1,
#         "name": "m",
#         "username": "m",
#         "password": "m",
#         "person_token": "2de1abc9-4752-4741-9075-a74fa1d2bef1m",
#         "permission": "member"
#     }
# }

# username ='s'
# user_data_details =user_data_json[username]
# print(user_data_details)
# # username ='s'
# # password = "s"

# # if username in user_data_json and password == user_data_json[username]["password"]:
# #     user_details = user_data_json[username]
# #     print("token",user_details,user_details["person_token"])
    
# # else :
# #     print(f"Invalid username or password ")



token={
    "admin":[],
    "member":[]
}


permission= "admin"
generated_token = "tokenstr"
token[permission].append(generated_token)
print(token)

    