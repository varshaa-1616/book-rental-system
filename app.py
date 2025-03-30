from flask import Flask, render_template, request, redirect
import mysql.connector
from mysql.connector import Error
from book2 import *
from book1 import *
from book3 import *

app = Flask(__name__)

def get_db_connection():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='books'
    )
    return mydb

@app.route('/bah', methods=['GET','POST'])
def bah():
    if request.method=='GET':
        return render_template('bah.html')
    else:
        return render_template('bah.html')

@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='GET':
        return render_template('homepage.html')
    else:
        return render_template('homepage.html')
    


class A:
    usern=""
    
    
    @app.route('/<int:bookid>', methods=['GET', 'POST'])
    def bookpage(bookid):
        bo=bookid
        if request.method=='GET':
            # b=salt(bo)
            A.c=sugar(bo)
            if len(A.usern)==0:
                p="login.html"
                return render_template('bookpage.html', context=A.c, ohgod=p)
            elif len(A.usern)!=0:
                p="payment.html"
                return render_template('bookpage.html', context=A.c, ohgod=p)
        else:
            return ""

    @app.route('/logout.html', methods=['GET','POST'])
    def logout():
        if request.method=='GET':
            A.usern=""
            return render_template("logout.html")

    @app.route('/mybooks.html', methods=['GET','POST'])
    def mybooks():
        if request.method=='GET':
            if len(A.usern)!=0:
                book=masala(A.usern)         
                    #rows = [mybooks[i] for i in range(0, len(mybooks))]
                return render_template('mybooks.html', strength="", book=book, number=range(len(book['book_id'])))
                # except Exception as e:
                #     print("Some error occured: ", e)
                #     rows = []
                # finally:
                #     mycursor.close()
                #     mydb.close()
                
            # else:
                # return render_template('mybooks.html',strength="Some error occured!")
            
    


            

    @app.route('/login.html',methods=['POST','GET'])
    def login():
        
        if request.method=='POST':
            A.usern=request.form['usern']
            passw=request.form['passw']
            try:
                actual_pass=DB.get_pass(A.usern)
                if passw==actual_pass:
               
                    return render_template('bah.html',username=A.usern)
                else:
                    s="incorrect username or password"
                    return render_template('index_after_deletion.html',string=s)
            except:
                s="incorrect username or password"
                return render_template('index_after_deletion.html',string=s)
        else:
            return render_template('login.html')
        


    @app.route("/payment.html")
    def payment_page():
        A.bn=A.c['booktitle']
        A.f=A.c['booktitle']
        return render_template('payment.html',booktitle=A.c['booktitle'], price=A.c['price'])



    @app.route('/confirm_payment.html', methods=['GET', 'POST'])
    def confirm_payment():
    
        if request.method == 'POST':
            transaction_id = request.form['transaction_id']
            amount = request.form['amount']
            payee_name = request.form['payee_name']
            username = request.form['username']
            password = request.form['password']
        
            try:
                actual_password=DB.get_pass(username)
                if password == actual_password:
                    a=mub(transaction_id, amount, payee_name, username, password, A.f)
                    return redirect('thank_you.html')
                else:
                    s="incorrect username or password"
                    return render_template('confirm_payment.html', strong=s)
        
            except Error as e:
                s="some error occured: "+str(e)
                return render_template('confirm_payment.html', strong=s)
           
    
        return render_template('confirm_payment.html',strong="")


@app.route('/thank_you.html')
def thank_you():
    return render_template('thank_you.html')



@app.route('/genre')
def index():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    try:
        cursor.execute('SELECT DISTINCT genre FROM book')
        genres = cursor.fetchall()
    except Exception as e:
        print("Error fetching genres:", {e})
        genres = []
    finally:
        cursor.close()
        mydb.close()
    
    return render_template('index.html', genres=genres)

@app.route('/genre/<string:genre_name>')
def genre_page(genre_name):
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    try:
        cursor.execute('SELECT book_title, price, ratings, img_src, book_id FROM book WHERE genre = %s', (genre_name,))
        books = cursor.fetchall()

        
        rows = [books[i:i+4] for i in range(0, len(books))]
    except Exception as e:
        print("Error fetching books for genre", genre_name + ":", e)
        rows = []
    finally:
        cursor.close()
        mydb.close()
    
    return render_template('genre.html', genre={'name': genre_name}, rows=rows)
    



@app.route('/delete_account.html',methods=['POST','GET'])
def delete_account():
    if request.method=='POST':
        usern=request.form['usern']
        passw=request.form['passw']
        try:
            actual_pass=DB.get_pass(usern)
            if passw==actual_pass:
                s="Account deleted successfully!"
                DB.rem_data(usern)
                return render_template('index_after_deletion.html',string=s)
            else:
                s="Please check the username or password and try again"
                return render_template('index_after_deletion.html',string=s)
        except:
            s="Error occured! try again later..."
            return render_template('index_after_deletion.html',string=s)
    else:
        return render_template('delete_account.html')


@app.route("/index_after_deletion.html",methods=["GET","POST"])
def index_after_deletion():
    if request.method=='POST':
        usern=request.form['usern']
        passw=request.form['passw']
        try:
            actual_pass=DB.get_pass(usern)
            if passw==actual_pass:
                return render_template('base.html',username=usern)
            else:
                s="Please check the username or password and try again"
                return render_template('index_after_deletion.html',string=s)
        except:
            s="Error occured! try again later..."
            return render_template('index_after_deletion.html',string=s)
    else:
        return render_template('index.html')


@app.route("/create_account.html",methods=["GET","POST"])
def create_account():
    if request.method=="POST":
        usern=request.form['usern']
        passw=request.form['passw']
        mail=request.form['email']
        try:
            if usern and passw and mail:
                if DB.check_account(usern)==0:
                    DB.add_data(usern,passw,mail)
                    return render_template("login.html")
                else:
                    s="error the username is already present"
                    return render_template('index_after_deletion.html',string=s)
            else:
               s="Error occured! try again later..."
               return render_template('index_after_deletion.html',string=s) 
                
        except:
            s="some error occured please try again!"
            return render_template('index_after_deletion.html',string=s)
    else:
        return render_template('create_account.html')

    
@app.route("/update_account.html",methods=["GET","POST"])
def update_account():
    if request.method=="POST":
        usern=request.form['usern']
        passw=request.form['passw']
        npass=request.form["npass"]
        mail=request.form["nmail"]
        try:
            if npass and mail:
                actual_pass=DB.get_pass(usern)
                if passw==actual_pass:
                    DB.update(usern,npass,mail)
                    return "successfully updated"
                else:
                    s="wrong credentials"
                    return render_template("update_account.html",string=s)
            else:
                s="Error occured try again later!"
            return render_template("update_account.html",string=s)
        except:
            s="Error occured try again later!"
            return render_template("update_account.html",string=s)
    else:
        return render_template("update_account.html")
            
        




if __name__ == '__main__':
    app.run(debug=True)





