
from connector import DBConnect

connection = DBConnect()
engine = connection.engine

class CRUD:
    def __init__(self):
        self.db = DBConnect()
        
    def create_table(self, table_name, schema):
        query = f"""CREATE TABLE IF NOT EXISTS {table_name} ({schema})"""
        
        self.db.execute_query(query)
        
    def drop_table(self, table_name):
        query = f"""DROP TABLE IF EXISTS {table_name}"""
        
        self.db.execute_query(query)
        
    def insert(self, table_name, columns, values):
        query = f"""INSERT INTO {table_name} ({columns}) VALUES ({values})"""
        
        self.db.execute_query(query)
        
    def select(self, table_name, columns, condition=None):
        query = f"""SELECT {columns} FROM {table_name}"""
        
        if condition:
            query += f""" WHERE {condition}"""
            
        self.db.execute_query(query)
        
    def update(self, table_name, columns, condition=None):
        query = f"""UPDATE {table_name} SET {columns}"""
        
        if condition:
            query += f""" WHERE {condition}"""
            
        self.db.execute_query(query)
        
    def delete(self, table_name, condition=None):
        query = f"""DELETE FROM {table_name}"""
        
        if condition:
            query += f""" WHERE {condition}"""
            
        self.db.execute_query(query)
        
    def close(self):
        self.db.close()
