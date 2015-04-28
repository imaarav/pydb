import sqlite3


def userSignUp():
    global userName
    connectDB()
    
    userName = raw_input("\n\nEnter the desired Username: ")
    userName = userName.lower()
    
    rows = c.execute("SELECT * FROM myData;")
    
    for row in rows:
        if row[0] == userName:
            print "This userName has already been chosen; please try some other username"
            closeDB()
            return
        
   
    password = getpass.getpass(prompt = "Enter the App Password: ")
    confirmPassword = getpass.getpass(prompt = "Confirm the App Password: ")
    if password != confirmPassword:
        print "The values of the fields in Password and Confirm password do not match. Please try again"
        closeDB()
        return
    
    c.execute("INSERT INTO myData (userNameC, passwordC) VALUES ('userName','password')")
    closeDB()
    
    print "You've successfully signed up for the App. Please login to continue"
    userLogIn()
    return

def userLogIn():
        print "\n\n                          Login Screen\n"
        global userName
        global password
        userName = raw_input("Enter the App Username: ")
        password = getpass.getpass(prompt = "Enter the App Password: ")
        
        connectDB()
        
        rows = c.execute("SELECT * FROM myData;")
    
        for row in rows:
            if row[0] == userName:
                if row[4] == password:
                    print "You've Successfully Logged In"
                    closeDB()
                    authenticatedUser()
                else:
                    print "One or more information is incorrect. Please try logging in again."
                    closeDB()
                    return
            else:
                print "One or more information is incorrect. Please try logging in again."
                closeDB()
                return
                
def authenticatedUser():
    print "\n\n                           Home Screen\n"
    action = raw_input("Enter 1: Add data to your database OR 2: Retrieve data from your database OR 3: Log Out :- ")
    
    if action == "1":
        addData()
   
    elif action == "2":
        getData()
    
    elif action == "3":
        print "\n        You have successfully LOGGED OUT of your account"
        sys.exit(0)
        
    else:
        print "\n           Please enter a relevant action number."
        authenticated_user()
        
    return
    
def addData():
    firstName = raw_input("Enter your First Name:")
    lastName = raw_input("Enter your Last Name:")
    #R for blob
    
    
def connectDB():
    global conn = sqlite3.connect('data.db')
    global c = conn.cursor()
    
    
def closeDB():
    conn.commit()
    conn.close()