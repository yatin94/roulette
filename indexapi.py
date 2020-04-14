from flask import Flask, flash, redirect, render_template, request,session, abort, jsonify
import json
import os
import mysql.connector 
import random
from jinja2 import Environment
import time
import threading

app =Flask(__name__,static_folder='templates/')
def mysqlconne_all(query,option):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="roulette"
        )
        mycursor = mydb.cursor()
        mycursor.execute(query)
        if option == 'select':
            myresult = mycursor.fetchall()
            return myresult
        else:
            mydb.commit()


@app.route("/")
def Index():
    return jsonify([{"name":"test"}])

@app.route("/register",methods=['POST'])
def register():
    if request.method == 'POST':
        Name = request.form['Name']
        email = request.form['email']
        Password = request.form['Password']
        print(Name,email,Password)

@app.route("/home")
def home():
    if request.method == 'GET':
        try:
            session['loggedin']
            myresult = mysqlconne_all("select name,money,won from testing",'select')
            return render_template("index.html",result = myresult)
        except:
            return redirect('/login')

@app.route("/betamount/<amt>,<number>")
def betamount(amt,number):
    mysqlconne_all("update testing set Bet ='"+amt+"', number = '"+str(number)+"',money=money-"+str(amt)+" where username = '"+str(session['username'])+"'","update")
    return amt+" points Booked"

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method == 'POST':

        Username = request.form['Username']
        Password = request.form['Password']
        try:
            myresult = mysqlconne_all("SELECT money,username,password FROM testing where username = '" +str(Username)+"'",'select')
        except Exception as e:
            flash("Incorrect Password Or Username")
            print('error'+str(e))
            return redirect('/login')
        if Username == myresult[0][1] and Password == myresult[0][2]:
            session['username'] = myresult[0][1]
            session['loggedin'] = True
            session['money'] = myresult[0][0]
            return redirect("/home")
        flash("Incorrect Password Or Username")
        return redirect('/login')
    elif request.method == 'GET':
        try:
            if session['loggedin']:
                return redirect("/home")
            else:
                return render_template('login.html')
        except:
            return render_template('login.html')

@app.route("/getrand")
def getrand():
    number = mysqlconne_all("select number from value where id = 1","select")
    return str(number[0][0])

def recurfunc():
    mysqlconne_all("update value set number ='"+str(random.randint(0,35))+"' where id = '1'","update")
    time.sleep(15)
    recurfunc()

@app.route("/winner")
def winner():
    number = mysqlconne_all("select number from value where id = 1","select")
    winner = mysqlconne_all("select Bet,number,money from testing where username = '"+session['username']+"'","select")
    if winner[0][0] == '' or winner[0][1] == '':
        return jsonify({'money':winner[0][2],'data':"Did not receive your bet"})

    if int(number[0][0]) == int(winner[0][1]):
        win_amount = int(winner[0][0])*2
        mysqlconne_all("update testing set money = money+"+str(win_amount)+",BET='',number='' where username = '"+session['username']+"'","update")
        return jsonify({'money':winner[0][2],'data':"You Won "+str(win_amount)})
    else:
        mysqlconne_all("update testing set BET='',number='' where username = '"+session['username']+"'","update")
        return jsonify({'money':winner[0][2],'data':"You Lost "+str(winner[0][0])})


@app.route("/getmoneytable")
def getmoneytable():
    myresult = mysqlconne_all("select name,won,money from testing",'select')
    return jsonify({"data":myresult,"count":len(myresult)})




if __name__ == "__main__":
    # t1 = threading.Thread(target=recurfunc)
    # t1.start()
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='192.168.1.42',port="5060")
  
