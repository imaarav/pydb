import sqlite3
import getpass
import sys
import os

def user_sign_up():
    global username
    conn, c = connect_DB()
    
    username = raw_input("\n\nEnter the desired Username: ")
    username = username.lower()
    
    rows = c.execute("SELECT * FROM myData;")
    
    for row in rows:
        if row[0] == username:
            print "This username has already been chosen; please try some other username"
            conn.commit()
            conn.close()
            return
        
   
    password = getpass.getpass(prompt = "Enter the App Password: ")
    confirm_password = getpass.getpass(prompt = "Confirm the App Password: ")
    if password != confirm_password:
        print "The values of the fields in Password and Confirm password do not match. Please try again"
        conn.commit()
        conn.close()
        return
    
    values = [(username), (password)]
    c.execute("INSERT INTO myData (usernameC, passwordC) VALUES (?,?)", values)
    conn.commit()
    conn.close()
    
    print "You've successfully signed up for the App. Please login to continue"
    user_log_in()
    return

def user_log_in():
        print "\n\n                          Login Screen\n"
        global username
        global password
        username = raw_input("Enter the App Username: ")
        password = getpass.getpass(prompt = "Enter the App Password: ")
        
        conn, c = connect_DB()
        
        rows = c.execute("SELECT * FROM myData;")
    
        for row in rows:
            if row[0] == username:
                if row[4] == password:
                    print "You've Successfully Logged In"
                    conn.commit()
                    conn.close()
                    authenticated_user()
                else:
                    print "One or more information is incorrect. Please try logging in again."
                    conn.commit()
                    conn.close()
                    return
            
        print "One or more information is incorrect. Please try logging in again."
        conn.commit()
        conn.close()
        return
                
def authenticated_user():
    print "\n\n                           Home Screen\n"
    action = raw_input("Enter 1: Add data to your database OR 2: Retrieve data from your database OR 3: Update Data OR 4: Log Out :- ")
    
    if action == "1":
        add_data()
   
    elif action == "2":
        get_data()
    
    elif action == "2":
        update_data()
    
    
    elif action == "4":
        print "\n        You have successfully LOGGED OUT of your account"
        sys.exit(0)
        
    else:
        print "\n           Please enter a relevant action number."
        authenticated_user()
        
    return
    
def add_data():
    first_name = raw_input("Enter your First Name:")
    last_name = raw_input("Enter your Last Name:")
    upld_file = raw_input("Enter your File Path:")
    
    # the_data = open(upld_file,'rb').read()
    # the_data = 2
    with open(upld_file,"rb") as input_file:
        ablob = input_file.read()
    
    conn, c = connect_DB()
    
    c.execute('''UPDATE myData SET firstNameC = ?, lastNameC = ?, fileC = ? WHERE usernameC = ?''', (first_name, last_name, sqlite3.Binary(ablob), username))
    conn.commit()
    conn.close()

    print "\n         The above entry has been ADDED TO YOUR DATABASE.\n"
    task = raw_input("\nEnter 1: Update Entry OR 2: Home Screen OR (Any Other key): Log Out :- ")
    if task == "1":
        update_data()
    elif task == "2":
        authenticated_user()
    else:
        print "\n        You have successfully LOGGED OUT of your account"
        sys.exit(0)
        
def update_data():
    first_name = raw_input("Enter new - First Name:")
    last_name = raw_input("Enter new - Last Name:")
    file_path = raw_input("Enter new - Absolute File Path:")
    the_data = open('file_path','rb').read()
    
    conn, c = connect_DB()
    c.execute("UPDATE myData SET first_nameC = ?, last_nameC = ?, fileC = ? WHERE usernameC = username", first_name, last_name, the_data)
    conn.commit()
    conn.close()
    
    print "\n         The above entry has been UPDATED IN THE DATABASE.\n"
    task = raw_input("\nEnter 1: Update Entry OR 2: Home Screen OR (Any Other key): Log Out :- ")
    if task == "1":
        update_data()
    elif task == "2":
        authenticated_user()
    else:
        print "\n        You have successfully LOGGED OUT of your account"
        sys.exit(0)
    
def get_data():
    conn, c = connect_DB()
    value = [(username)]
    row = c.execute("SELECT * FROM myData WHERE usernameC = (?)", value)
    row = c.fetchone()
    
    print row[0]
    print row[1]
    print row[2]
    print row[4]
    
    dnld_path = "C:\Users\khushboo\Desktop\python db\default download"
    dnld_file = os.path.join(dnld_path, row[0])
    
    # output_file = open(dnld_file,'wb')
    # output_file.write(row[3])
    
    with open (dnld_file, "wb") as output_file:
        output_file.write(row[3])
    
    print "Your file has been saved to the -- Default Download -- folder"
    
    conn.commit()
    conn.close()
    task = raw_input("\nEnter 1: Update Entry OR 2: Home Screen OR (Any Other key): Log Out :- ")
    if task == "1":
        update_data()
    elif task == "2":
        authenticated_user()
    else:
        print "\n        You have successfully LOGGED OUT of your account"
        sys.exit(0)
    
    
    
    
    
def connect_DB():
    conn = sqlite3.connect('data.db')
    #conn.text_factory = str
    c = conn.cursor()
    return conn, c