import mysql.connector

def sugar(bookid):
    mydb=mysql.connector.connect(host='localhost',user='root',password='root',database='books')
    mycursor=mydb.cursor()
    mycursor.execute(f"select * from book where book_id={int(bookid)}")
    myresult=mycursor.fetchall()
    bookid=[x[0] for x in myresult]
    title=[x[1] for x in myresult]
    price=[x[2] for x in myresult]
    ratings=[x[3] for x in myresult]
    genre=[x[4] for x in myresult]
    description=[x[-1] for x in myresult]
    img_src=[x[11] for x in myresult]
    d={"bookid":bookid[0],"booktitle": (title[0]), 'price': price[0], 'ratings': ratings[0], 'genre': (genre[0]), 'description': (description[0]), 'img_src': (img_src[0])}
    mycursor.close()
    mydb.close()
    return d
    
def salt(title):
    mydb=mysql.connector.connect(host='localhost',user='root',password='root',database='books')
    mycursor=mydb.cursor()
    mycursor.execute(f"select book_id from book where book_title={title}")
    myresult=mycursor.fetchall()
    id=[x[0] for x in myresult]
    # d={"booktitle": (title[0]).decode(), 'price': price[0], 'ratings': ratings[0], 'genre': (genre[0]).decode(), 'description': (description[0]).decode(), 'img_src': (img_src[0]).decode()}
    
    mycursor.close()
    mydb.close()
    return id



def masala(username):
    mydb=mysql.connector.connect(host='localhost',user='root',password='root',database='books')
    mycursor=mydb.cursor()
    mycursor.execute(f'SELECT book_name, amount, book_id, img_src FROM rent WHERE username="{username}"')
    mybooks = mycursor.fetchall()       
    book_title= [x[0] for x in mybooks]  
    price= [x[1] for x in mybooks]
    book_id= [x[2] for x in mybooks]
    img_src=[x[3]  for x in mybooks]
    # rows = [mybooks[i:i+4] for i in range(0, len(mybooks))]
    
    book={'book_title': book_title, 'price': price, 'book_id': book_id, 'img_src': img_src}
    mycursor.close()
    mydb.close()
    # print(rows)
    return book    
                    #rows = [mybooks[i] for i in range(0, len(mybooks))]
                    #return render_template('mybooks.html', strength="", book={, 'price': [x[1] for x in mybooks], 'book_id': [x[2] for x in mybooks], 'img_src': [x[3]  for x in mybooks]}, rows=rows)
                # except Exception as e:
                #     print("Some error occured: ", e)
                #     rows = []
                # finally:
                #     mycursor.close()
                #     mydb.close()
masala('aaa')