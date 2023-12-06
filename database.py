import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="",
    password="",
    database="testDB"
)
mydata = db.cursor()
mydata.execute("USE testDB")
mydata.execute("SELECT salt,tag,nonce,cipher_text FROM password_vault")


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

read_Database()