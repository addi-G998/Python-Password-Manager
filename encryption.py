import hashlib
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
    host="localhost",
    user="Eldrix",
    password="f_w$KE.4",
    database="testDB"
)

mydata = db.cursor()


def encrypt(plain_text, password):
    # generate a random salt
    salt = get_random_bytes(AES.block_size)

    # use the Scrypt KDF to get a private key from the password
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # return a dictionary with the encrypted text
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
    #mydata.execute("USE testDB")
    mydata.execute("INSERT INTO password_vault (salt, cipher_text,nonce,tag) VALUES(%s,%s,%s,%s)", (b64encode(salt).decode('utf-8'),b64encode(cipher_text).decode('utf-8'),b64encode(cipher_config.nonce).decode('utf-8'),b64encode(tag).decode('utf-8')))
    db.commit()
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }



def decrypt(enc_dict, password):
    # decode the dictionary entries from base64
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])

    # generate the private key from the password and salt
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted


def create_id(Lable):
    #salt = str(get_random_bytes(AES.block_size))
    #currentdate = datetime.now()
    #unique_id = str(Lable + currentdate.strftime("%d/%m/%Y") + salt)
    #hashify = hashlib.sha224(unique_id.encode('utf-8'))
    #hashed_id = hashify.hexdigest()
    #return hashed_id
    newid = Lable + "newObj"
    return newid

def read_Database():
    for x in mydata:
        name = (" ".join(x))
        #print(name)
        #while loop
        salt = name[0:24]
        tag = name[25:49]
        nonce = name[50:74]
        cipher = name[75:99]
        print(salt)
        print(tag)
        print(nonce)
        print(cipher)
        data_dict = {
            'cipher_text': cipher,
            'salt': salt,
            'nonce': nonce,
            'tag': tag
        }
        decrypt(data_dict, )

read_Database()

def main():
    password = input("Password: ")

    # First let us encrypt secret message
    encrypted = encrypt("The secretest message here", password)
    print(encrypted)

    # Let us decrypt using our original password
    decrypted = decrypt(encrypted, password)
    print(bytes.decode(decrypted))

main()