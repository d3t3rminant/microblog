import os
import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from pymongo import DESCENDING
from dotenv import load_dotenv

load_dotenv()

def create_app():   #zatím moc nechápu, proč by se to takhle mělo dělat
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.microblog



    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST": #request má hodnotu jen uvnitř fce asociované s endpointem
            #extrakce údajů z formuláře/requestu a přidání do databáze
            entry_content = request.form.get("content")   #data jsou odeslana zaroven s requestem/v requestu. request.form vypada dost jako dict
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})


        #tvorba listu obsahujícího všechny posty z databáze, provede se vždy
        entries_with_date = [
            (
                entry["content"], 
                entry["date"], 
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            ) 
                for entry in app.db.entries.find({}).sort("date", DESCENDING) #in app.db.entries.find({}) je list of dict (spíše cursor object, který se jako dict chová)
        ]

        return render_template("home.html", entries=entries_with_date)
    
    return app


