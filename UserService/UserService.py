"""Class to get the user path for Excel file"""

import json
from pathlib import Path

# Function to read the user file
def readUserJSON ():

    base_dir = Path(__file__).resolve().parent
    json_path = base_dir / "User_files.json"

    with open(json_path, "r") as json_file:
        data = json.load(json_file)

    return data

def userGetter(fileType):

    if fileType == "master_file":
        return readUserJSON()["master_file"]
    elif fileType == "acquisti":
        return readUserJSON()["master_file_acquisti"]
    else:
        raise Exception ("ERROR! File type not found!")
