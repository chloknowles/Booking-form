from guizero import App, Window, PushButton, Text, TextBox, ButtonGroup, info, ListBox
import sqlite3  
from sqlite3 import Error
import os
import os.path
global stored_userid
#
#
# set up database
#
# Define the DDL SQL
# Create a user table and a booking table 
sql = """
CREATE TABLE "Users" (
	"UserID"	INTEGER NOT NULL,
	"First_name"	TEXT,
	"Last_name"	TEXT,
	"Phone_number"	TEXT,
	"Email_address"	TEXT,
	"User_password"	TEXT,
	PRIMARY KEY("UserID" AUTOINCREMENT)
);
CREATE TABLE "Bookings" (
	"BookingID"	INTEGER NOT NULL,
	"UserID"	INTEGER,
	"Numberof_guests"	INTEGER,
	"Dateof_visit"	TEXT,
	"Timeof_visit"	INTEGER,
	"User_requests"	TEXT,
	PRIMARY KEY("BookingID" AUTOINCREMENT),
	CONSTRAINT "UserID_FK" FOREIGN KEY("UserID") REFERENCES "Users"("UserID")
);
Insert into Users (First_name, Last_name, Phone_number, Email_address, User_password) values ('Chloe', 'Knowles', '07895743036', 'chloe', 'college1');
Insert into Bookings (UserID, Numberof_guests, Dateof_visit, Timeof_visit, User_requests) values (1, 4, '10/10/2021', 1900, 'Vegan');


"""
#
#   Procedures to open the forms
#
def login_windowL():
    windowL.show()

def create_windowB():
    windowB.show()
    

def create_windowC():
    windowC.show()
    

def mybooking_window():
    windowN.show()
   


###########################
### Run a query to SELECT ###
def query_database(database, query):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    return rows


### Creates an account ###
def sql_createacc(entities): #CREATE ACCOUNT
      conn = sqlite3.connect('bookings.db')
      cursorObj = conn.cursor()
      create_query = "INSERT INTO Users (First_name, Last_name, Phone_number, Email_address, User_password) VALUES (?,?,?,?,?)"
      cursorObj.execute(create_query, entities)
      conn.commit()
#
#
### Creates a booking ###
def sql_createbooking(entitiesB): #CREATE BOOKING
      conn = sqlite3.connect('bookings.db')
      cursorObj = conn.cursor()
      create_query = "INSERT INTO Bookings (UserID, Numberof_guests, Dateof_visit, Timeof_visit, User_requests) VALUES (?,?,?,?,?)"
      cursorObj.execute(create_query, entitiesB)
      conn.commit()
      #
      # 
      #
      



def login_process(): ### Login form validation and checks email and password ###
    global stored_userid ## variable needed in all forms ##
    if email_boxL.value == "":
        info("Error", "You must enter a valid email")
    elif password_boxL.value == "":
        info("Error", "You must enter a password")

    else:
        email = email_boxL.value
        password = password_boxL.value
        ### set up SQL to find email on the database ###
        sqlselect = "SELECT * FROM Users WHERE Email_address = '"+ email+"'"
        rows = query_database(database_file, sqlselect)
        if len(rows) == 0: ### This checks that the user was found ###
            info("Error","Error")
        else:
            ### Stored UserID is stored as rows[0,0]
            stored_userid = (rows[0][0])  # We need this as a foreign key for the booking table
            storedemail = (rows[0][4])
            storedpassword = (rows[0][5])
            if email == storedemail and password == storedpassword:
                info("Log in","Success")
                buttonenquire.enable()
                makebooking.enable()
            else:
                info("Error","Incorrect")



def signup_process(): ### Process for creating an account ###
    global stored_userid ## global variable used again
    Fname = input_box1.value
    Lname = input_box2.value
    Pnumber = input_box3.value
    EmailA = input_box4.value
    Pword = input_box5.value
    if Fname == "" or Lname == "" : 
         info("ERROR","All details must be entered")
    elif len(Pword) < 5:
           info("ERROR","Pasword must be atleast 5 characters long")
    elif len(Pnumber) != 11:
        info("ERROR", "Please enter a valid phone number.")
    elif '@' not in EmailA:
        info("ERROR, please enter a valid email.")
    else:
        # insert user as all credential correct
        entities = (Fname, Lname, Pnumber, EmailA, Pword)
        sql_createacc(entities)
        info("INSERT USER","Account Created")
        buttonforbooking.enable()
         ### set up SQL to find new user on the database ###
        sqlselect = "SELECT * FROM Users WHERE Email_address = '"+ EmailA +"'"
        rows = query_database(database_file, sqlselect)
        if len(rows) == 0: ### This checks that the user was found ###
            info("Error","New user not found")
        else:
            ### Stored UserID is stored as rows[0,0]
            stored_userid = (rows[0][0])  # We need this as a foreign key for the booking table
            storedemail = (rows[0][4])
       



def openbooking_process(): ### Process for opening your bookings ###
    global stored_userid
    info("My Bookings","Directing you to your Bookings..",)
    ###
    ## Look at your bookings
    sqlselect = "SELECT * FROM Bookings WHERE UserID = "+ str(stored_userid)+ ""
    rows = query_database(database_file, sqlselect)
    numrows = len(rows)
    if len(rows) == 0: ### This checks that the user was found ###
        info("Error","No bookings found")
    else:
        for row in range(numrows):
           numG = (rows[row][2])
           dateb = (rows[row][3])
           timeb = (rows[row][4])
           detail = ("       "+ str(numG) + "              " + dateb + "         " + str(timeb) )
           listbox_booking.insert(row,detail)
        
    windowN.show()


def booking_createprocess():
    global stored_userid #This has been stored from the database
    info("Booking","Booking Confirmed")
    windowB.show()
    if inputguestbox.value == "" : 
         info("ERROR","Booking details must be entered")
    
    else:
        
        # insert booking correct
        Numberof_guests = inputguestbox.value
        Dateof_vist = inputdatebox.value
        Timeof_visit = inputtimebox.value
        UserID= stored_userid
        User_requests = "Vegan"
        entitiesB = (UserID, Numberof_guests, Dateof_vist, Timeof_visit, User_requests)
        sql_createbooking(entitiesB)
        #info("INSERT NOTE","Note added")
    



### MAIN PROGRAM ###
#####################

database_file = 'bookings.db'
# Delete the database
if os.path.exists(database_file):
  os.remove(database_file)

# Connect to the database
conn = sqlite3.connect(database_file)
# Get a cursor pointing to the database
cursor = conn.cursor()
# Create the tables
cursor.executescript(sql)
# Commit to save everything
conn.commit()
# Close the connection to the database


### TITLE PAGE ###
app = App(title="Login or Sign up")

windowL = Window(app, title="Login")
windowL.hide()

windowC = Window(app, title="Create account")
windowC.hide()

windowB = Window(app, title="Make a Booking")
windowB.hide()

windowN = Window(app, title= "My Bookings")
windowN.hide()

login_button = PushButton(app, text="Login", command=login_windowL)
app.bg = "pink"
login_button.bg = "light grey"

#createbooking_button = PushButton(app, text="Make a Booking", command=createbooking_windowB)
signup_button = PushButton(app, text = "Sign up", command = create_windowC)
signup_button.bg = "light grey"


### LOGIN PAGE ###
titleL = Text(windowL, text ="Login")
titleL.text_size = 20
windowL.bg = "pink"
textLU = Text(windowL, text="Enter Email:")
textLU.text_color = "black"
email_boxL = TextBox(windowL)
email_boxL.bg = "white"
textLP = Text(windowL, text="Enter Password:")
textLP.text_color = "black"
password_boxL = TextBox(windowL, hide_text=True)
password_boxL.bg = "white"
buttonL = PushButton(windowL, text = "Log in", command = login_process)
buttonenquire = PushButton(windowL, text = "My Bookings", command = openbooking_process)
buttonenquire.disable()
makebooking = PushButton(windowL, text = "Make a Booking", command = create_windowB)
makebooking.disable()


### CREATE ACCOUNT PAGE ###
titleC = Text(windowC, text ="Create account")
titleC.text_size = 20 
windowC.bg = "pink"
textName = Text(windowC, text = "First name:")
input_box1 = TextBox(windowC)
input_box1.bg = "white"
textSurname = Text(windowC, text = "Last name:")
input_box2 = TextBox(windowC)
input_box2.bg = "white"
textPhone = Text(windowC, text = "Phone number: ")
input_box3 = TextBox(windowC)
input_box3.bg = "white"
textUsername = Text(windowC, text = "Email:")
input_box4 = TextBox(windowC)
input_box4.bg = "white"
textPassword = Text(windowC, text = "Password:")
input_box5 = TextBox(windowC, hide_text=True)
input_box5.bg = "white"
buttonC = PushButton(windowC, text = "Sign up", command = signup_process)
buttonforbooking = PushButton(windowC, text = "Make a booking", command = create_windowB)
buttonforbooking.disable()



### MAKE A BOOKING PAGE ###
titlebooking = Text(windowB, text = "Make a booking")
titlebooking.text_size = 20
guests = Text(windowB, text = "Number of Guests: ")
inputguestbox = TextBox(windowB, multiline = True)
inputguestbox.bg = "white"
date = Text(windowB, text = "Date: ")
inputdatebox = TextBox(windowB)
inputdatebox.bg = "white"
time = Text(windowB, text = "Time")
inputtimebox = TextBox(windowB)
inputtimebox.bg = "white"
submit = PushButton(windowB, text = "Submit", command = booking_createprocess)



### VIEW BOOKINGS PAGE ###
titlebooking = Text(windowN, text = "My Bookings")
titlebooking.text_size = 20
guestbox = Text(windowN, text = "Number of guests   Date of visit         Time of visit   User requests")


listbox_booking = ListBox(windowN, items=[""],height = 60, width = 400, scrollbar = True)
listbox_booking.text_size = 13
app.display()