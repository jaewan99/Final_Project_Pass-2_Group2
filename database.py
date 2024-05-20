import pymongo
from flask import session


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
courses_db = myclient["courses_management"]
users_management_db = myclient["users_management"]



def get_course(code):
    course_coll = courses_db["courses"]
    course = course_coll.find_one({"code":code}, {"_id":0})
    return course

def get_courses():
    courses_list = []
    courses_coll = courses_db["courses"]
    for p in courses_coll.find({},{"_id":0}):
        courses_list.append(p)
    return courses_list


def get_subcourse(subcode):
    subcourse_coll = courses_db["subcourses"]
    subcourse = subcourse_coll.find_one({"subcode": subcode}, {"_id":0})
    return subcourse

def get_subcourses(code):
    subcourses_list = []
    subcourses_coll = courses_db["subcourses"]
    for p in subcourses_coll.find({"code":code},{"_id":0}):
        subcourses_list.append(p)
    return subcourses_list

def get_subcourse_topics(subcode):
    subcourse_topics_head = []
    subcourse_topics_list = []
    subcourse_topics_coll = courses_db["subcourse_topic"]
    for p in subcourse_topics_coll.find({"subcode":subcode},{"_id":0}):
        if p['subcode'] == p['subtopiccode']:
            subcourse_topics_head.append(p)
        else:
            subcourse_topics_list.append(p)
    return subcourse_topics_list, subcourse_topics_head

def get_subcourse_topic(subtopiccode):
    subcourse_coll = courses_db["subcourse_topic"]
    subcourse_topic = subcourse_coll.find_one({"subtopiccode": subtopiccode}, {"_id":0})
    return subcourse_topic

def get_user(username):
    users_coll = users_management_db['users']
    user=users_coll.find_one({"username":username})
    return user

def get_user_password(username):
    users_coll = users_management_db['users']
    user= users_coll.find_one({"username":username})
    return user["password"]

def change_user_password(pwd):
    users_coll = users_management_db['users']
    users_coll.update_one({"username":session["user"]["username"]}, {"$set": {"password": pwd}})

def create_user(username, password, first_name, last_name):
    users_coll = users_management_db['users']
    user = {"username":username, "password":password, "first_name":first_name, "last_name":last_name}
    users_coll.insert_one(user)

def get_user_comments(username):
    comments_list = []
    comments_coll = users_management_db["user_comment"]
    for p in comments_coll.find({"username":username},{"_id":0}):
        comments_list.append(p)
    return comments_list

def get_user_comments_with_subtopiccode(username, subtopiccode):
    comments_list = []
    comments_coll = users_management_db["user_comment"]
    for p in comments_coll.find({"username":username,"subtopiccode":int(subtopiccode)},{"_id":0}):
        comments_list.append(p)
    return comments_list


#  check
def add_user_comment(username, comment, subtopiccode):
    comments_coll = users_management_db["user_comment"]
    user_comment = {"username":username, "comment":comment, "subtopiccode": int(subtopiccode)}
    comments_coll.insert_one(user_comment)


