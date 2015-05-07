from Crypto.Cipher import AES
import Crypto.Random as rand
from Crypto.Util import Counter
import Crypto.Protocol.KDF as KDF
import Crypto.Hash as Hash
from binascii import hexlify
import os
import base64

block_size = 32
IV_size = 16
SALT_BITS = 8

directory = os.path.join(os.getcwd(), "..")
data_directory = os.path.join(directory, "data")
code_directory = os.path.join(directory,"code")


pad = lambda s: s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

def hashed(data_value, salt_value):
    hasher = Hash.SHA256.new()
    hasher.update(salt_value + ":" + data_value)
    data_value = base64.b64encode(hasher.digest())
    return data_value
    

class row:

    def __init__(self, username, first_name, last_name, file, password, IV = None, salt = None):
        
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.file = file
        self.password = password
        
        self.IV = IV
        
        if salt == None:
            self.salt = base64.b64encode(str(rand.new().read(SALT_BITS)))
        else:
            self.salt = salt
        

    def encrypt(self, password):
        key = KDF.PBKDF2(password, self.salt, 32, 2000)
        m = AES.MODE_CBC
        self.IV = str(rand.new().read(IV_size))
        aes_encryptor = AES.new(key, m, self.IV)
        
        self.password = hashed(self.password, self.salt)
        self.password = pad(self.password)
        self.password = base64.b64encode(aes_encryptor.encrypt(self.password))

        self.first_name = base64.b64encode(self.first_name)
        self.last_name = base64.b64encode(self.last_name)
        self.file = base64.b64encode(self.file)
        self.IV = base64.b64encode(self.IV)
        self.salt = base64.b64encode(self.salt)
        
        key = None
        aes_encryptor = None
        password = None
        
    def decrypt(self, password):

        self.salt = base64.b64decode(self.salt)
        key = KDF.PBKDF2(password, self.salt, 32, 2000)
        
        self.IV = base64.b64decode(self.IV)
        
        self.password = base64.b64decode(self.password)
        
        m = AES.MODE_CBC
        aes_decryptor = AES.new(key, m, self.IV)
        
        self.password = aes_decryptor.decrypt(self.password)
        self.password = unpad(self.password)
        
        self.first_name = base64.b64decode(self.user_name)
        self.last_name = base64.b64decode(self.last_name)
        self.file = base64.b64decode(self.file)
        key = None
        aes_decryptor = None
        master_password = None


    def write(self, filename, target_directory):
        os.chdir(target_directory)
        myfile = open(filename,"a")
        write_string = self.service + " " + self.username + " " + self.password + " " + self.mode + " " + str(self.IV) + " " + self.salt + "\n"
        myfile.write(write_string)
        myfile.flush()
        myfile.close()
        os.chdir(code_directory)
        return True