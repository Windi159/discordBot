import json
from os.path import isfile
def readJson(user_name):
    if isfile(f".\\userInfo\\{user_name}.json"):
        with open(f".\\userInfo\\{user_name}.json", "r", encoding="utf-8") as file:
            user_info_file = json.load(file)

            return user_info_file

    else:
        return None

def writeJson(user_name, user_info):
    with open(f".\\userInfo\\{user_name}.json", "w", encoding="utf-8") as make_file:
        json.dump(user_info, make_file, indent=4)
