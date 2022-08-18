from flask import Flask,render_template


def index():
    return render_template("index.html")


def auth():
    
    return "Hello"


