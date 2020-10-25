from .util import get_conn
import sqlite3, json

class TableOps:
    def __init__(self, db_name=None):
        self.db_name = db_name

    def execute(self, sqllite_query):
        conn = None
        result = None
        try:
            conn = get_conn(self.db_name)
            result = conn.execute(sqllite_query)
            conn.commit()
        except sqlite3.Error as e:
            print("Error: %s" % e)
        finally:
            if conn:
                conn.close()
        return result

    def drop(self, table_name):
        query = "DROP TABLE %s" % table_name
        result = self.execute(sqllite_query=query)
        if result:
            print("table removed......... ")

    def insert(self, table_name, data):
        try:
            data_dict = json.loads(data)
        except (ValueError, json.JSONDecodeError) as e:
            print("Error: %s" %e)
            raise ValueError

        if data_dict:
            columns = ", ".join(data_dict.keys())
            values = []
            for val in data_dict.values():
                if type(val) == str:
                    val = '"' + val + '"'
                else:
                    val = str(val)
                values.append(val)
            sql_query = """
            insert into {table_name}
            ({columns}) 
            values ({values}) ;
            """.format(table_name=table_name, columns=columns, values=', '.join(values))
            result = self.execute(sqllite_query=sql_query)
            if result:
                print("data inserted successfully.......")
        else:
            print("Data format is not acceptable: %s" %data_dict)

    def update(self, update_query):
        result = self.execute(sqllite_query=update_query)
        if result:
            print("%s data updated successfully.............")

    def truncate(self, table_name):
        query = "DELETE FROM %s ;" %table_name
        result = self.execute(sqllite_query=query)
        if result:
            print("%s table truncated successfully..........." % table_name)

    def create(self, select_query):
        result = self.execute(sqllite_query=select_query)
        if result:
            print("Table created successfully.....................\n")
