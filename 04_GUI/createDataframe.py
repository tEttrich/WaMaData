import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pymongo import MongoClient

# CONNECT TO CLIENT AND CREATE COLLECTION
print("Connecting to MongoDB")
client = MongoClient("mongodb+srv://test:test@cluster1337.kv1ih.mongodb.net/IoTProjectData?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.ProjectData
col = db.Data
print("Connected to Client:", db)

def createDF():
    cursor = col.find()
    print ("total docs in collection:", col.count_documents( {} ))

    print("Creating Dataframe from MongoDB Collection")
    df = pd.DataFrame(list(cursor))
    print("Dataframe created!")
    return df
