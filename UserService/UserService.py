"""Class to get the user path for Excel file"""

import json

# Function to read the user file
def readUserJSON ():

    with open("D:\\PythonProjects-Storage\\Orto_ERP\\UserService\\User_files.json", "r") as json_file:
        data = json.load(json_file)

    return data

def userGetter(fileType):

    if fileType == "master_file":
        return readUserJSON()["master_file"]
    else:
        raise Exception ("ERROR! File type not found!")
