from flask import Flask, flash, redirect, render_template, request,session, abort, jsonify
import json
import os
import mysql.connector 
from jinja2 import Environment

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
        myresult = mysqlconne_all("select name,money,won from testing",'select')
        return render_template("index.html",result = myresult)

@app.route("/betamount/<amt>")
def betamount(amt):
    mysqlconne_all("update testing set Bet ='"+amt+"' where username = '"+str(session['username'])+"'","update")
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



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='192.168.1.42',port="5060")
  