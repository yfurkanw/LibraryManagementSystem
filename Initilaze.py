import sqlite3 as sql
def initialize():
    db = sql.connect("libraryDb.sqlite")

    cur = db.cursor()

    cur.execute(""" CREATE TABLE IF NOT EXISTS Members(
                    MemberID Integer Primary Key AUTOINCREMENT,
                    FirstName Text,
                    LastName Text,
                    Type Text,
                    Mail Text,
                    Password Text,
                    TookedBooks Integer)
                    """)
    cur.execute(""" CREATE TABLE IF NOT EXISTS Categories(
                    CategoryID Integer Primary KEy AUTOINCREMENT,
                    Name Text )""")

    cur.execute(""" CREATE TABLE IF NOT EXISTS Books(
                    BookID Integer Primary Key AUTOINCREMENT,
                    Name Text,
                    Author Text,
                    ISBN Integer,
                    Address Text,
                    PublicationDate Text,
                    Status Text,
                    Category_ID Integer,
                    Foreign Key(Category_ID) References Categories(CategoryID))
                    """)

    cur.execute(""" CREATE TABLE IF NOT EXISTS TookBooks(
                    TookBookID Integer Primary Key AUTOINCREMENT,
                    MemberID Integer ,
                    BookID Integer,
                    TookDate Text,
                    Foreign Key(MemberID) references Members(MemberID),
                    Foreign Key(BookID) references Books(BookID))""")

    cur.execute(""" CREATE TABLE IF NOT EXISTS ReceivedBooks(
                    ReceivedBookID Integer Primary Key AUTOINCREMENT,
                    MemberID Integer,
                    BookID Integer ,
                    ReceivedDate Text,
                    Foreign Key(MemberID) references Members(MemberID),
                    Foreign Key(BookID) references Books(BookID))""")

    cur.execute(""" CREATE TABLE IF NOT EXISTS ReturnedBooks(
                    ReturnedBookID Integer Primary Key AUTOINCREMENT,
                    MemberID Integer,
                    BookID Integer,
                    ReturnedDate Text,
                    Foreign Key(MemberID) references Members(MemberID),
                    Foreign Key(BookID) references Books(BookID))""")

    cur.execute(""" Create Trigger IF NOT EXISTS tookedBookTrigger
                    After Insert
                    On TookBooks
                    BEGIN
                        Update Books Set Status = 'Occupied' where BookID = NEW.BookID;
                        
                    END
                    """)
    cur.execute(""" Create Trigger IF NOT EXISTS reservedBookTrigger
                        After Insert
                        On ReceivedBooks
                        BEGIN
                            Update Books Set Status = 'Reserved' where BookID = NEW.BookID;
                        END
                        """)
    cur.execute(""" Create Trigger IF NOT EXISTS returnedBookTrigger
                            After Insert
                            On ReturnedBooks
                            BEGIN
                                Update Books Set Status = 'Free' where BookID = NEW.BookID;
                            END
                            """)

    cur.execute(""" Create Trigger IF NOT EXISTS tookedBookPlus1Trigger
                        After Insert
                        On TookBooks
                        BEGIN
                            Update Members Set TookedBooks = TookedBooks+1 where MemberID = NEW.MemberID;
                        END
                        """)
    cur.execute(""" Create Trigger IF NOT EXISTS returnedBookMinus1Trigger
                        After Insert
                        On ReturnedBooks
                        BEGIN
                            Update Members Set TookedBooks = TookedBooks-1 where MemberID = NEW.MemberID;
                        END
                        """)

"""
    ??lk 6 cur.execute fonksiyon ??a????r??m??yla tablolar??m??z?? ve aralar??ndaki ili??kileri kurduk.
    5 Adet Trigger olu??turduk. 
    tookedBookTrigger --> Yeni bir kiralama i??lemi yap??ld??ktan sonra kitap stat??s??n?? 'Occupied' yap??yor.
    reservedBookTrigger --> Yeni bir kiralama i??lemi yap??ld??ktan sonra kitap stat??s??n?? 'Reserved' yap??yor.
    returnedBookTrigger --> Yeni bir kiralama i??lemi yap??ld??ktan sonra kitap stat??s??n?? 'Free' yap??yor.
    tookedBookPlus1Trigger --> Yeni bir kiralama i??lemi yap??ld??ktan sonra ba??lant??l?? oldu??u ??yenin TookedBooks h??cresini 1 artt??yor.
    returnedBookMinus1Trigger --> Yeni bir kiralama i??lemi d??n?????? yap??ld??ktan sonra ba??lant??l?? oldu??u ??yenin TookedBooks h??cresini 1 azalt??yor.

    
"""

initialize()
