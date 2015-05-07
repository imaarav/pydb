import sqlite3
from Functions import functions

conn, c = functions.connect_DB()
c.execute('''CREATE TABLE IF NOT EXISTS myData(usernameC TEXT PRIMARY KEY, first_nameC TEXT, last_nameC TEXT, fileC BLOB, passwordC TEXT, IVC TEXT, saltC TEXT);''')
conn.commit()
conn.close()

def main():
    
    print "\n\n              Welcome to the APP"
    initial = raw_input("Enter 1 to Sign Up OR 2 to Log In: ")
    if initial == "1":
        functions.user_sign_up()
    elif initial == "2":
        functions.user_log_in()
    else:
        print "\n Please enter relevant data"
        main()

    
if __name__ == '__main__':
    main()