from pymongo import MongoClient
import urllib

cluster = MongoClient("mongodb://localhost:27017/")
db=cluster["linkedin"]
collection=db['person']
collection2=db["for_test"]


def save_to_db(datas):
    for data in datas:
        collection2.insert_one({"tr_name" : data["persian_firstname"] + " " + data["persian_lastname"], "linkedin_url":data["linkedin_url"]})


def read_from_db():
    person_name = []

    for person in collection.find({},{"first_middle_name":1, "last_name":1, "linkedin_url":1}):
        person_name.append(person)
    
    return person_name




# print(read_from_db())

# save_to_db(datas)
