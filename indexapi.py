from flask import Flask, flash, redirect, render_template, request,session, abort, jsonify
import json
import os

app =Flask(__name__,static_folder='templates/')

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

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method == 'POST':
        Username = request.form['Username']
        Password = request.form['Password']
        if Username == 'test' and Password == 'test':
            return render_template("index.html")
        flash("Incorrect Password Or Username")
        return redirect('/login')
    elif request.method == 'GET':
        return render_template('login.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='192.168.1.36',port="5060")