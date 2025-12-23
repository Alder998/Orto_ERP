"""Class used as a simple ETL to manipulate data from Excel"""

import pandas as pd
from UserService import UserService as user

class ExcelDataService:

    def __init__(self):
        pass

    def getExcelData(self):
        data = pd.read_excel(user.userGetter(fileType="master_file"))
        return data

    def updateExcelData (self, data):

        # Process the data from dict to dataFrame row
        data = pd.DataFrame([data])
        # Remove Emoji
        data["Attività"] = data["Attività"].str.replace(" ⛏️", "").str.replace(" 💩", "").str.replace(" 👻", "").str.replace(" 💦", "").str.replace(" 🧪", "").str.replace(" 🔰","").str.replace(" 🚜", "").str.replace(" 🍎", "").str.replace(" 🫘", "").str.replace(" 🌱", "")

        # load the data
        existing_data = pd.read_excel(user.userGetter(fileType="master_file"))
        # add the id
        if len(existing_data["id_activity"]) == 0:
            data["id_activity"] = 0
        else:
            data["id_activity"] = existing_data["id_activity"].max() + 1

        # append the data to the existing table, save it
        new_data = pd.concat([existing_data, data], axis=0)

        # sort by date
        #new_data = new_data.sort_values(by="Data", ascending=False)

        # Save to the existing dir
        new_data.to_excel(user.userGetter(fileType="master_file"), index=False)
        # Save a copy for backup
        new_data.to_excel(user.userGetter(fileType="master_file").replace(".xlsx", "") + "_backup.xlsx", index=False)

        return new_data

    def deleteExcelRow (self, id_activity):

        # load the data
        existing_data = pd.read_excel(user.userGetter(fileType="master_file"))
        # delete wrt the id_activity
        existing_data = existing_data.set_index("id_activity")
        new_data = existing_data.drop(index=id_activity)
        # reset index
        new_data = new_data.reset_index(drop=False)

        # Save the new Excel File
        new_data.to_excel(user.userGetter(fileType="master_file"), index=False)

        return new_data