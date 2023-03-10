import sqlite3 as sql
from bookState import BookState


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = sql.connect(db_file)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def execute(self, sql, params=None):
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)
        self.connection.commit()

    def fetchAll(self, sql, params=None):
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)
        return self.cursor.fetchall()
    
    def fetchOne(self, sql, params=None):
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)
        return self.cursor.fetchone()

class DatabaseHandler(object):
    def __new__(cls):
        if not hasattr(cls,"instance"):
            cls.instance = super(DatabaseHandler,cls).__new__(cls)

        return cls.instance
    
    def init(self,db_file):
        self.m_Database = Database(db_file)
        
    def check_user_name(self,userName):
        #Check if userName exist in database
        response = self.m_Database.fetchOne(f"SELECT count(1) from Members where UserName == \"{userName}\";")
        if(response[0] == 1):
            return True
        else:
            return False
        pass

    def     check_auth(self,userName,password):
        response = self.m_Database.fetchOne(f"SELECT * from Members where UserName == \"{userName}\" and Password == \"{password}\";")
        #print(response)
        if response is not None:
            result = {
                "userName" : response[1]+ " " + response[2],
                "userId" : response[0],
                "phoneNumber" : response[4],
                "occupiedOrReservedBooks" : response[6],
                "role" : response[3]
            }
            return result
        else:
            return None

    def check_user_Id(self, userId):
        response = self.m_Database.fetchOne(f"SELECT * from Members where MemberID == \"{userId}\";")
        if response is not None:
            result = {
                "result" : True,
                "data" : {
                    "userName" : response[1]+ " " + response[2],
                    "userId" : response[0],
                    "phoneNumber" : response[4],
                    "occupiedOrReservedBooks" : response[6],
                    "role" : response[3]
                }
                
            }
            return result
        else:
            result = {
                "result" : False
            }
            return result

    def check_book(self,bookId):
        response =self.m_Database.fetchOne(f"SELECT * from Books where BookID == \"{bookId}\";")
        print(response)
        if response is not None:
            result = {
                "result" : True,
                "data" : {
                    "physicalAddress" : {
                        response[4].split('-')[0],
                        response[4].split('-')[1]
                        },
                    "title" : response[1],
                    "author" : response[2],
                    "publicationDate" : response[5],
                    "bookState" : response[6],
                    "occupiedOrReservedBy" : response[8],
                    "UUID" : response[0]
                }
                
            }
            print(result)
            return result
        else:
            result = {
                "result" : False
            }
            return result

    def update_book(self,book):
        state = "Free"
        print(book.m_UniqueId)
        if(book.m_State == BookState.OCCUPIED):
            state = "Occupied"
        elif(book.m_State == BookState.RESERVED):
            state = "Reserved"
        
        if book.m_OccupiedOrReservedBy is None:
            self.m_Database.execute(f"UPDATE Books Set Status = \"{state}\" , occupiedOrReservedBy = \"{None}\"  where BookID = \"{book.m_UniqueId}\";")
        else:
            self.m_Database.execute(f"UPDATE Books Set Status = \"{state}\" , occupiedOrReservedBy = \"{book.m_OccupiedOrReservedBy.m_UserId}\"  where BookID = \"{book.m_UniqueId}\";")
        pass
    
    def update_reader(self, reader):
        self.m_Database.execute(f"UPDATE Members Set TookedBooks = \"{reader.m_NumberOfBooksOccupied}\" where MemberID = \"{reader.m_UserId}\";")
        pass

    def search_book(self,criteria, keyword):
        response =self.m_Database.fetchOne(f"SELECT * from Books where \"{criteria}\" == \"{keyword}\";")
        #print(response)
        if response is not None:
            result = {
                "result" : True,
                "data" : {
                    "physicalAddress" : {
                        response[4].split('-')[0],
                        response[4].split('-')[1]
                        },
                    "title" : response[1],
                    "author" : response[2],
                    "publicationDate" : response[5],
                    "bookState" : response[6],
                    "occupiedOrReservedBy" : response[8],
                    "UUID" : response[0]
                }
                
            }
            print("Title: ",result["data"]["title"])
            print("Author: ",result["data"]["author"])
            print("Publication Date: ",result["data"]["publicationDate"])
            print("State: ",result["data"]["bookState"])
            print("Book Unique ID: ", result["data"]["UUID"])
            return result
        else:
            print("No record exist!")
