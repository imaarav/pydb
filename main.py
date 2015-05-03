import sqlite3
from Functions import functions

conn, c = functions.connectDB()
c.execute('''CREATE TABLE IF NOT EXISTS myData(userNameC TEXT, firstNameC TEXT, lastNameC TEXT, fileC BLOB, passwordC TEXT, PRIMARY KEY(userNameC))''')
functions.closeDB(conn)

def main():
    
    print "\n\n              Welcome to the APP"
    initial = raw_input("Enter 1 to Sign Up OR 2 to Log In: ")
    if initial == "1":
        functions.userSignUp()
    elif initial == "2":
        functions.userLogIn()
    else:
        print "\n Please enter relevant data"
        main()

    
if __name__ == '__main__':
    main()