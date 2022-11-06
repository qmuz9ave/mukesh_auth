import sqlite3
from typing import List
from commons.db_exceptions import MultipleValueReturn, TableCreationError
from commons.userModel import UserModel
from commons.variables import variables



class SqliteClient():
    def __init__(self, db_path=None, conn=None) -> None:
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = variables.SQLITE_PATH

    def __call__(self):
        # TODO: connection error handle
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        self.conn = conn
        return self


    @staticmethod
    def check_if_table_exists(cursor):
        query = "select * FROM sqlite_master WHERE name = 'user_data' and type = 'table'"
        selector = cursor.execute(query)
        status = selector.fetchone()
        return status

    def create_table(self):
        cursor = self.conn.cursor()
        table_exists = self.check_if_table_exists(cursor=cursor)  # no need of this: IF NOT EXISTS handles it
        if not table_exists:
            try:
                # IF NOT EXISTS: creates table if doesnot exist
                # else table creation will ignored
                query = "CREATE TABLE IF NOT EXISTS user_data(\
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
                    name CHAR(100),\
                    mobile_number CHAR(100),\
                    password CHAVARR(100),\
                    dob CHAR(100) NULL,\
                    created_at CHAR(100) NULL,\
                    updated_at CHAR(100) NULL\
                        )"
                query_status = cursor.execute(query)
            except Exception as e:
                raise TableCreationError(e)

        else:
            query_status = None
        return query_status

    def close_connection(self):
        self.conn.close()


sqlite = SqliteClient()


class UserData(object):

    def __init__(
        self, 
        table_name = 'user_data',
        db = sqlite(), #connection established db
        cursor = None,
        ) -> None:

        self.table_name = table_name
        self.db = db
        self.cursor = cursor
        self.instance = None

    def objects(self):
        self.cursor = self.db.conn.cursor()
        return self

    @staticmethod
    def decode_row_object(obj):
        data = None
        if isinstance(obj, sqlite3.Row):
            data = {}
            keys = obj.keys()
            for key in keys:
                data[key] = obj[key]
        elif isinstance(obj, list):
            data = []
            for raw_data in obj:
                keys = raw_data.keys()
                data_dict = {}
                for key in keys:
                    data_dict[key] = raw_data[key]
                data.append(data_dict)
        return data

    def get(self,**kwargs):
        query = f"SELECT * FROM {self.table_name} WHERE "
        counter = 1
        for key,value in kwargs.items():
            if counter == 1:
                query += f"{key}= '{value}' "
            else:
                query += f"AND {key}= '{value}' "
            counter += 1

        selector = self.cursor.execute(query)
        result = selector.fetchall()

        if not result:
            return self

        # self.cursor.close()
        if len(result) > 1:
            raise MultipleValueReturn()
        data = self.decode_row_object(result[0])

        # set instance
        self.instance = data
        return self
    
    def filter(self, **kwargs):
        query = f"SELECT * FROM {self.table_name} WHERE "
        counter = 1
        for key,value in kwargs.items():
            if counter == 1:
                query += f"{key}= '{value}' "
            else:
                query += f"AND {key}= '{value}' "
            counter += 1

        selector = self.cursor.execute(query)
        result = selector.fetchall()
        self.cursor.close()
        data = self.decode_row_object(result)
        # set id as none
        self.id = None
        return data

    @staticmethod
    def get_key_value(kwargs):
        keys = ""
        values = ""
        counter = 1
        for key, value in kwargs.items():
            if counter == 1:
                keys += f'{key}'
                values += f"'{value}'"
            else:
                keys += f',{key}'
                values += f",'{value}'"
            counter +=1
        return keys,values

    def create(self,**kwargs):
        UserModel(**kwargs)
        query = f"INSERT INTO {self.table_name} "
        keys,values = self.get_key_value(kwargs)
        query += f"({keys}) VALUES ({values})"
        selector = self.cursor.execute(query)
        id = selector.lastrowid
        self.db.conn.commit()
        data = self.get(id=id)
        # set instance
        self.instance = data
        return self

    def update(self,**kwargs):
        query = f"UPDATE {self.table_name} SET "

        counter = 1
        for key, value in kwargs.items():
            if counter == 1:
                query += f"{key}= '{value}'"
            else:
                query += f",{key}= '{value}'"
            counter += 1

        # get instance
        instance_id = self.instance.get('id')
        query += f" WHERE id = {instance_id}"

        selector = self.cursor.execute(query)
        self.db.conn.commit()

        # set instance
        data = self.get(id=instance_id)
        self.instance = data.instance
        return self

