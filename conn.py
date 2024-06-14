import pyodbc
import pandas as pd
from dotenv import load_dotenv
from pypika import Query, Table
import queue
from concurrent import futures
import os
import datetime

load_dotenv()

class GenericConn:
    _instance = None
    _workers = 8
    _multi_row_insert_limit = 5000
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(GenericConn, cls).__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def get_connection(self):
        if not self._connection:
            _conn_params = {
                'server': os.getenv('HOST'),
                'database': os.getenv('DATABASE'),
                'user': os.getenv('USER'),
                'password': os.getenv('PASS'),
                'driver': '{SQL Server}',
            }
            self._connection = pyodbc.connect(**_conn_params)
        return self._connection

    def _execute(self, query, flg=True):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.fast_executemany = True
            cursor.execute(query)
            
            if flg:
                result = cursor.fetchall()
                cols = [i[0] for i in cursor.description]
                df = pd.DataFrame.from_records(result,columns=cols)
                return df
            else:
                connection.commit()
                
        except Exception as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
                    
    def _multi_row_insert(self, batch, table_name, table_schema):
        row_expressions = []

        for _ in range(batch.qsize()):
            row_data = tuple(batch.get())
            row_expressions.append(row_data)
        
        table = Table(table_name,schema=table_schema)
        insert_into = Query.into(table).insert(*row_expressions)
        print(insert_into)
        return self._execute(str(insert_into),flg=False)
    
    def _process_row(self, row, batch, table_name, table_schema):
        batch.put(row)

        if batch.full():
            self._multi_row_insert(batch, table_name, table_schema)

        return batch
    
    def _bulk_insert(self, df, table_name, table_schema):
        batch = queue.Queue(self._multi_row_insert_limit)
        result = None

        with futures.ThreadPoolExecutor(max_workers=self._workers) as executor:
            todo = []

            for index, row in df.iterrows():
                future = executor.submit(
                    self._process_row, row, batch, table_name, table_schema
                )
                todo.append(future)

            for future in futures.as_completed(todo):
                result = future.result()

        if result is not None and not result.empty():
            return self._multi_row_insert(result, table_name, table_schema)

    def import_data_concurrent(self, df, table_name, table_schema):
        self._bulk_insert(df, table_name, table_schema)
    
    def execute(self, query):
        self._execute(query,flg=False)
    
    def get_query(self, query):
        return self._execute(query)

    