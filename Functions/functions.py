import sqlite3
import getpass
import sys
import os
import Crypto.Hash as Hash
import base64

from Row import DB_record

def hashed(data_value, salt_value):
    hasher = Hash.SHA256.new()
    hasher.update(salt_value + ":" + data_value)
    data_value = base64.b64encode(hasher.digest())
    return data_value

def user_sign_up():
    global username
    global password
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
    
    new_row = DB_record.record(username, "First Name not saved", "Last Name not saved", "No File uploaded yet", password)
    new_row.encrypt(password)
    values = [(new_row.username), (new_row.first_name), (new_row.last_name), (new_row.file), (new_row.password), (new_row.IV), (new_row.salt)]
    c.execute("INSERT INTO myData (usernameC, first_nameC, last_nameC, fileC, passwordC, IVC, saltC) VALUES (?,?,?,?,?,?,?)", values)
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
        
        DB_rows = c.execute("SELECT * FROM myData;")
    
        for DB_row in DB_rows:
            if DB_row[0] == username:
                global this_row
                this_row = DB_record.record(DB_row[0], DB_row[1], DB_row[2], DB_row[3], DB_row[4], DB_row[5], DB_row[6])
                this_row.decrypt(password)
                if this_row.password == hashed(password, this_row.salt):
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
    
    this_row.first_name = first_name
    this_row.last_name = last_name
    this_row.file = ablob
    
    this_row.encrypt(password)
    
    conn, c = connect_DB()
    
    c.execute('''UPDATE myData SET first_nameC = ?, last_nameC = ?, fileC = ? WHERE usernameC = ?''', (this_row.first_name, this_row.last_name, sqlite3.Binary(this_row.file), this_row.username))
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
    upld_path = raw_input("Enter new - Absolute File Path:")
    #the_data = open('file_path','rb').read()
    
    with open(upld_file,"rb") as input_file:
        ablob = input_file.read()
    
    this_row.first_name = first_name
    this_row.last_name = last_name
    this_row.file = ablob
    
    this_row.encrypt(password)
    
    conn, c = connect_DB()
    c.execute('''UPDATE myData SET first_nameC = ?, last_nameC = ?, fileC = ? WHERE usernameC = ?''', (this_row.first_name, this_row.last_name, sqlite3.Binary(this_row.file), this_row.username))
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
    current_row = c.execute("SELECT * FROM myData WHERE usernameC = (?)", value)
    current_row = c.fetchone()
    current_row = DB_record.record(current_row[0], current_row[1], current_row[2], current_row[3], current_row[4], current_row[5], current_row[6])
    current_row.decrypt(password)
    
    print current_row.username
    print current_row.first_name
    print current_row.last_name
    
    dnld_path = "C:\Users\khushboo\Desktop\python db\default download"
    dnld_file = os.path.join(dnld_path, current_row.username)
    
    # output_file = open(dnld_file,'wb')
    # output_file.write(row[3])
    
    with open (dnld_file, "wb") as output_file:
        output_file.write(current_row.file)
    
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