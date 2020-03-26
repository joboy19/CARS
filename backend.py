import numpy as np 
import pandas as pd 
import json
import csv
import recommender as rc

from flask import Flask, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "this_is_a_secret"

PATH_TO_LISTENING_DATA = "data/mm/listening_data.csv"
PATH_TO_USERS = "data/mm/user_data.csv"
PATH_TO_COUNTRIES = "data/mm/country_mapping.csv"
PATH_TO_STORE = "data/mm/store.h5"
PATH_TO_TRACK = "data/mm/track_mapping.csv"
PATH_TO_ARTIST = "data/mm/artist_mapping.csv"

##getID for a single user
def getID(username):
    with open(PATH_TO_USERS, "r", encoding='utf-8', newline='\n') as data1:
        for line in data1:
            data = line.rstrip().split(",")
            if data[1] == username:
                return data[0]
    return "False"

#get individual ratings for each user
@app.route("/get_ratings", methods=["GET"])
def get_ratings():
    print("get ratings for user:", session["id"])
    out = rc.get_listens_user(session["id"])
    print("ratings:", out)
    return json.dumps(out)

#get book details from an id
def get_book(id_):
    with open("data/books.csv", "r", encoding='utf-8', newline='\n') as data1:
        for line in data1:
            data = line.rstrip().replace(", ", " ").replace("\"", "").split(",")
            if data[0] == id_:
                return data[1], data[2]
    return "False" 

#default page render 
@app.route('/')
def hello_world():
    return render_template("index.html")

def checkuser(username, password):
    with open(PATH_TO_USERS, "r", encoding='utf-8', newline='\n') as data1:
        for line in data1:
            data = line.rstrip().split(",")
            if data[0] == username:
                if data[1] == password:
                    return True
    return False
        

@app.route('/login', methods=["GET"])
def login():
    val = checkuser(request.args["username"], request.args["password"])
    if val:
        session["id"] = request.args["username"]
        print("logged in", session["id"], request.args["username"])
        return "True"
    return "False"

@app.route("/update_details", methods=["POST"])
def update_details():
    r = csv.reader(open(PATH_TO_USERS))
    data = list(r)
    for x in range(len(data)):
        if data[x][0] == session["id"]:
            print("here")
            print(request.form)
            data[x] = [data[x][0], request.form["username"], data[x][2]]
            writer = csv.writer(open('data/users.csv', 'w', newline='\n', encoding='utf-8'))
            writer.writerows(data)
            return "True"
    return "False"

def delete_rating(bookid):
    r = csv.reader(open("data/ratings.csv"))
    data = list(r)
    for x in range(len(data)):
        if data[x][0] == session["id"]:
            if data[x][1] == bookid:
                data.pop(x)
                writer = csv.writer(open('data/ratings.csv', 'w', newline='\n', encoding='utf-8'))
                writer.writerows(data)
                return "True"

@app.route("/make_rating", methods=["POST"])
def make_rating():
    if request.form["rating"] == "-1":
        delete_rating(request.form["bookid"])
        return "True"
    else:
        r = csv.reader(open("data/ratings.csv"))
        data = list(r)
        for x in range(len(data)):
            if data[x][0] == session["id"]:
                if data[x][1] == request.form["bookid"]:
                    print("here")
                    data[x] = [data[x][0], data[x][1], request.form["rating"]]
                    writer = csv.writer(open('data/ratings.csv', 'w', newline='\n', encoding='utf-8'))
                    writer.writerows(data)
                    return "True"
        data.append([session["id"], request.form["bookid"], request.form["rating"]])
        writer = csv.writer(open('data/ratings.csv', 'w', newline='\n', encoding='utf-8'))
        writer.writerows(data)
        return "True"

@app.route("/add_book", methods=["POST"])
def add_book():
    r = csv.reader(open('data/books.csv', encoding="utf-8"))
    data = list(r)
    book_id = len(data)
    print(book_id)
    data.append([book_id, request.form["bookname"], request.form["genre"]])
    writer = csv.writer(open('data/books.csv', 'w', newline='\n', encoding='utf-8'))
    writer.writerows(data)
    return str(book_id)

@app.route("/get_countries", methods=["GET"])
def get_countries():
    out = rc.get_countries()
    return json.dumps(out)

@app.route("/get_recoms", methods=["GET"])
def get_recoms():
    out = rc.get_recommendation(session["id"], 10)
    return json.dumps(out)


@app.route("/get_recoms", methods=["POST"])
def change_context():
    rc.calc_svd(context_val=request.form["country"])

@app.route("/search_tracks", methods=["GET"])
def search_books():
    book = request.args["trackname"]
    with open(PATH_TO_TRACK, "r", encoding='utf-8') as data1:
        for line in data1:
            data = line.rstrip().split(",")
            if data[1] == book:
                return str(data[0])
    return "False"


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return "True"
    

if __name__ == '__main__':
    app.config.update(TEMPLATES_AUTO_RELOAD = True) 
    app.run(debug=True, use_reloader=False)