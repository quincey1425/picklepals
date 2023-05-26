import pymysql.cursors

class MySQLConnection:
    #Represents a connection to a MySQL database.
    def __init__(self, db):
        #Constructs a MySQLConnection object with the given database name.
        self.connection = pymysql.connect(
            host='localhost',
            user='root', 
            password='Vagkilla2', 
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query_db(self, query, data=None):
        #Executes the given SQL query with the optional data and returns the results.
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running query:", query)
                cursor.execute(query, data)
                if query.lower().startswith("select"):

                    result = cursor.fetchall()
                    return result
                elif query.lower().startswith("insert"):
                    self.connection.commit()
                    return cursor.lastrowid
                else:
                    self.connection.commit()
            except Exception as e:
                print("Query failed:", e)
                raise e

    def __del__(self):
        #Closes the database connection when the object is deleted.
        self.connection.close()

def connectToMySQL(db):
    #Creates and returns a MySQLConnection object with the given database name.
    return MySQLConnection(db)