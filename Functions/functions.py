import sqlite3
import getpass
import sys

def userSignUp():
    global userName
    conn, c = connectDB()
    
    userName = raw_input("\n\nEnter the desired Username: ")
    userName = userName.lower()
    
    rows = c.execute("SELECT * FROM myData;")
    
    for row in rows:
        if row[0] == userName:
            print "This userName has already been chosen; please try some other username"
            closeDB(conn)
            return
        
   
    password = getpass.getpass(prompt = "Enter the App Password: ")
    confirmPassword = getpass.getpass(prompt = "Confirm the App Password: ")
    if password != confirmPassword:
        print "The values of the fields in Password and Confirm password do not match. Please try again"
        closeDB(conn)
        return
    
    values = [(userName), (password)]
    c.execute("INSERT INTO myData (userNameC, passwordC) VALUES (?,?)", values)
    closeDB(conn)
    
    print "You've successfully signed up for the App. Please login to continue"
    userLogIn()
    return

def userLogIn():
        print "\n\n                          Login Screen\n"
        global userName
        global password
        userName = raw_input("Enter the App Username: ")
        password = getpass.getpass(prompt = "Enter the App Password: ")
        
        conn, c = connectDB()
        
        rows = c.execute("SELECT * FROM myData;")
    
        for row in rows:
            if row[0] == userName:
                if row[4] == password:
                    print "You've Successfully Logged In"
                    closeDB(conn)
                    authenticatedUser()
                else:
                    print "One or more information is incorrect. Please try logging in again."
                    closeDB(conn)
                    return
            else:
                print "One or more information is incorrect. Please try logging in again."
                closeDB(conn)
                return
                
def authenticatedUser():
    print "\n\n                           Home Screen\n"
    action = raw_input("Enter 1: Add data to your database OR 2: Retrieve data from your database OR 3: Update Data OR 4: Log Out :- ")
    
    if action == "1":
        addData()
   
    elif action == "2":
        getData()
    
    elif action == "2":
        updateData()
    
    
    elif action == "4":
        print "\n        You have successfully LOGGED OUT of your account"
        sys.exit(0)
        
    else:
        print "\n           Please enter a relevant action number."
        authenticated_user()
        
    return
    
def addData():
    firstName = raw_input("Enter your First Name:")
    lastName = raw_input("Enter your Last Name:")
    filePath = raw_input("Enter your Absolute File Path:")
    print filePath
    
    #theData = open(filePath,'rb').read()
    theData = 2
    
    conn, c = connectDB()
    
    #values = [ firstName, lastName, theData, userName]
    
    # c.execute("UPDATE INTO myData (firstNameC, lastNameC, fileC) VALUES (?,?,?) WHERE userNameC = ?", values)
    print "Before"
    print firstName
    print lastName
    print theData
    
    c.execute('''UPDATE myData SET firstNameC = ?, lastNameC = ?, fileC = ? WHERE userNameC = ?''', (firstName, lastName, theData, "aarav"))
    closeDB(conn)
    print "After"
    print "\n         The above entry has been ADDED TO YOUR DATABASE.\n"
    task = raw_input("\nEnter 1: Update Entry OR 2: Home Screen OR (Any Other key): Log Out :- ")
    if task == "1":
        updateData()
    elif task == "2":
        authenticatedUser()
    else:
        print "\n        You have successfully LOGGED OUT of your account"
        sys.exit(0)
        
def updateData():
    firstName = raw_input("Enter new - First Name:")
    lastName = raw_input("Enter new - Last Name:")
    filePath = raw_input("Enter new - Absolute File Path:")
    theData = open('filePath','rb').read()
    
    conn, c = connectDB()
    c.execute("UPDATE myData SET firstNameC = ?, lastNameC = ?, fileC = ? WHERE userNameC = userName", firstName, lastName, theData)
    closeDB(conn)
    
    print "\n         The above entry has been UPDATED IN THE DATABASE.\n"
    task = raw_input("\nEnter 1: Update Entry OR 2: Home Screen OR (Any Other key): Log Out :- ")
    if task == "1":
        updateData()
    elif task == "2":
        authenticatedUser()
    else:
        print "\n        You have successfully LOGGED OUT of your account"
        sys.exit(0)
    
def getData():
    conn, c = connectDB()
    value = [(userName)]
    row = c.execute("SELECT * FROM myData WHERE userNameC = (?)", value)
    row = c.fetchone()
    
    print row[0]
    print row[1]
    print row[2]
    print row[3]
    print row[4]
    
    closeDB(conn)
    task = raw_input("\nEnter 1: Update Entry OR 2: Home Screen OR (Any Other key): Log Out :- ")
    if task == "1":
        updateData()
    elif task == "2":
        authenticatedUser()
    else:
        print "\n        You have successfully LOGGED OUT of your account"
        sys.exit(0)
    
    
    
    
    
def connectDB():
    conn = sqlite3.connect('data.db')
    conn.text_factory = str
    c = conn.cursor()
    return conn, c
    
    
def closeDB(conn):
    conn.commit()
    conn.close()