from flask import Flask, flash, redirect, render_template, request,session, abort, jsonify
import json
import os

app =Flask(__name__)

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



if __name__ == "__main__":
    app.run(debug=True,host='192.168.1.33',port="5060")