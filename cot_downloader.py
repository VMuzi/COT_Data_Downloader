from ast import If
import csv
from importlib.resources import path
from os import read
import string
import cotdetail
import json
import dbconnect
from os.path import exists
import os
from datetime import datetime
import shutil
from pathlib import Path

sqlStatment = """INSERT INTO DOMData.dbo.COTData(InstrumentName,CotDate,NonCommercial_Long,NonCommercial_Short,OpenInterest)
                 VALUES(?,?,?,?,?)"""

def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def GetCOTDataList(filepath,extension):
    cot_data_list = []
    path = Path(filepath)  # current directory
    file_with_extension = next(path.glob(f"*{extension}"))

    if file_with_extension:
         with open(file_with_extension) as txt_file:
            csv_reader = csv.reader(txt_file,delimiter=',')
            for row in csv_reader:
                if csv_reader.line_num != 1:
                    if row:
                        instrName = row[0]
                        cotDate = row[2]
                        openInterest = row[7].strip()
                        nonCommLong = row[8].strip()
                        nonCommShort = row[9].strip()

                        newCotDetail = cotdetail.COTDetail(instrName,
                         cotDate,
                         openInterest,
                         nonCommLong,
                         nonCommShort)       
                        cot_data_list.append(newCotDetail)
            return cot_data_list


def SaveCOTData():
    currentdire = os.path.split(__file__)
    current_config = read_json(currentdire[0] + "\\" + "config.json")

    current_data = GetCOTDataList(current_config['filepath'],current_config['extension'])
    currentConnection_Objects = dbconnect.connectToDb(current_config['server'], current_config['database'], current_config['username'], current_config['password'])
    currentCursor = currentConnection_Objects[0]
    cnxn = currentConnection_Objects[1]

    if current_data:
        for current_cot_detail in current_data:
            values = (current_cot_detail.instrumentname,
            current_cot_detail.importdate,
            current_cot_detail.noncomm_long,
            current_cot_detail.noncomm_short,
            current_cot_detail.openinterest)
            dbconnect.execute_Create_SQL(sqlStatment,values,currentCursor)
    currentCursor.close()
    cnxn.commit()
    BackupFile(current_config['filepath'],current_config['extension'],current_config['backuppath'])


def BackupFile(filepath,extension,backuppath):
    if exists(filepath):
        path = Path(filepath)  # current directory
        file_with_extension = next(path.glob(f"*{extension}"))
        newfileName = file_with_extension.name + "-" + str(datetime.now().date()) + '.bak'
        os.rename(filepath+"\\"+file_with_extension.name,filepath+"\\"+newfileName)
        shutil.move(filepath+"\\"+newfileName,backuppath+"\\"+newfileName)



try:
    SaveCOTData()        
except Exception as error:
    print("Error while saving COT data: " + json.dumps(str(error)))