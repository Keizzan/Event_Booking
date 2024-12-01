# imports
import psycopg
from admin import DB_config as DB

class Event_database:
    def __init__(self):
        try:
            self.conn = psycopg.connect("dbname=%s user=%s password=%s host=%s port=%s"
            % (DB.event_name, DB.user, DB.password, DB.host, DB.port))
        except Exception as e:
            print(f'Failed to connect do db: {e}')
        self.cur = self.conn.cursor()
    
    def execute_function(self, sql):
        self.cur.execute(sql)
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()
        
class PastEvent_database:
    def __init__(self):
        try:
            self.conn = psycopg.connect("dbname=%s user=%s password=%s host=%s port=%s"
            % (DB.past_name, DB.user, DB.password, DB.host, DB.port))
        except Exception as e:
            print(f'Failed to connect do db: {e}')
        self.cur = self.conn.cursor()
    
    def execute_function(self, sql):
        self.cur.execute(sql)
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()

