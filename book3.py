import mysql.connector

def mub(transaction_id, amount, payee_name, username, password, book_name):
    mydb = mysql.connector.connect(host='localhost',user='root',password='root',database='books')
    mycursor = mydb.cursor()
    
    sql="insert into rent (transaction_id, amount, payee_name, username, password, book_name, book_id, img_src) values (%s,%s,%s,%s, %s, %s, %s, %s)"
    
    mycursor.execute(f'select book_id, img_src from book where book_title="{book_name}"')
    myresult=mycursor.fetchall()
    book_id=[x[0] for x in myresult]
    img_src=[x[1] for x in myresult]
    val=(int(transaction_id), float(amount), payee_name, username, password, book_name, int(book_id[0]),  img_src[0])
    mycursor.execute(sql,val)
    mydb.commit()
    mycursor.close()
    mydb.close()

