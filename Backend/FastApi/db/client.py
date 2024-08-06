from pymongo import MongoClient

#Conexion a base de datos local
#db_client = MongoClient().local

#Conexion a MongoDB Atlas

db_client = MongoClient("mongodb+srv://ranaraniada2:11111111rs@rodrigo-company.fp386l0.mongodb.net/?retryWrites=true&w=majority&appName=Rodrigo-Company").test