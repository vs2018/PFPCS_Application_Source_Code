# [1] PyMongo API is an interface to MongoDB, a NoSQL database, URL: https://api.mongodb.com/python/current/
# [2] Pandas library used for creating a DataFrame, URL: https://pandas.pydata.org/pandas-docs/stable/
# [3] GridFS allows the ability to store large documents in MongoDB, URL: https://api.mongodb.com/python/current/api/gridfs/index.html
# [4] Adapted from: https://realpython.com/introduction-to-mongodb-and-python/
# [5] Source: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
# [6] Source: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html
# [7] Adapted from: https://api.mongodb.com/python/current/examples/gridfs.html
# [8] Source: Author: therahulkumar, Date: Dec 22 '16 at 8:31, URL: https://stackoverflow.com/questions/41278798/python-bytessome-string-utf-8-and-strsome-string-utf-8
# [9] Source: Author: Kiran Kumar Kotari, Date: Jan 20 '16 at 15:56, URL: https://stackoverflow.com/questions/15197673/using-pythons-eval-vs-ast-literal-eval
# [10] Source: Author: fedorqui, Date: Jun 19 '15 at 22:26, URL: https://stackoverflow.com/questions/30948151/how-to-drop-a-collection-in-mongodb


from pymongo import MongoClient  # [1]
import pandas as pd  # [2]
import gridfs  # [3]
import ast
from utility import Utility


class DatabaseConnector:
    def __init__(self):  # [4]
        self.client = MongoClient()
        self.db = self.client["fuelprice"]
        self.db2 = self.client["master"]

    def collection(self, name):  # [4]
        return self.db[name]


class DatabaseModel:
    def __init__(self):
        self.connection = DatabaseConnector()
        self.db_id = None

    def save_master(self):
        df = pd.read_csv("master_data_file_updated.csv")  # [5]
        df = df.to_dict("records")  # [6]
        df = str(df)
        fs = gridfs.GridFS(self.connection.db2)  # [7]
        id = fs.put(df, encoding="utf-8")  # [7]
        self.save(id, "stations_data", "stations_data_id")

    def get_master(self):
        id = self.read("stations_data", "stations_data_id")
        fs = gridfs.GridFS(self.connection.db2)  # [7]
        a = fs.get(id).read()  # [7]
        s = str(a, "utf-8")  # [8]
        result = ast.literal_eval(s)  # [9]
        return Utility.to_dataframe(result)

    def save(self, data, name, id):  # [4]
        collection = self.connection.collection(name)
        data = {"id": id, "data": data}
        collection.insert_one(data, bypass_document_validation=True)

    def read(self, name, id):  # [4]
        collection = self.connection.collection(name)
        collection = collection.find_one({"id": id})
        return collection["data"]

    def drop(self, name):  # [4]
        collection = self.connection.collection(name)
        self.connection.db.collection.drop()  # [10]
