import os
import mysql.connector

class DB:
    mydb=mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', 'root'),
            database=os.environ.get('DB_NAME', 'books'),
            port=int(os.environ.get('DB_PORT', '3306')),
            ssl_disabled=os.environ.get('DB_SSL_DISABLED', 'false').lower() == 'true')
    mycursor=mydb.cursor()
    @classmethod
    def add_data(cls,usern,passw,email):
        sql="insert into users(username,password,email) values(%s,%s,%s)"
        val=(usern,passw,email)
        DB.mycursor.execute(sql,val)
        DB.mydb.commit()


    @classmethod
    def get_pass(cls,usern):
        l=[]
        DB.usern=usern
        sql="select password from users where username=%s"
        val=(usern,)
        DB.mycursor.execute(sql,val)
        for i in DB.mycursor:
            l.append(list(i))
        return l[0][0]

    @classmethod
    def check_account(cls,usern):
        l=[]
        try:
            sql="select password from users where username=%s"
            val=(usern,)
            DB.mycursor.execute(sql,val)
            for i in DB.mycursor:
                l.append(list(i))
            return len(l)
        except:
            return len(l)
        

    @classmethod
    def rem_data(cls,usern):
        sql="delete from users where username=%s"
        val=(usern,)
        DB.mycursor.execute(sql,val)
        DB.mydb.commit()
    @classmethod
    def update(cls,usern,npass,nmail):
        sql="update users set password=%s,email=%s where username=%s"
        val=(npass,nmail,usern)
        DB.mycursor.execute(sql,val)
        DB.mydb.commit()      
