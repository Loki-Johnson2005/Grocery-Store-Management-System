from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLALchemy
from Database.database import session
from Service import importFunc

def login(username, password):
    if username and password:
        user = session.query(importFunc.User).filter(importFunc.User.username == username).first()
        if user:
            if user.password == password:
                return user
            else:
                return "User credentials not valid"
        else:
            return "User credentials not valid"  # User not found
    else:
        return "Please fill all fields"
