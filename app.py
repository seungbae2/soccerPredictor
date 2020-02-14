from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_data
import requests
import os


app = Flask(__name__)
#app._static_folder = os.path.abspath("templates/static/")
mongo = PyMongo(app, uri = 'mongodb://localhost:27017/nhl_db')

@app.route("/")
def home():

	# insert event data to db
	mongo.db.event_data.remove({})
	nhl_data = scrape_data.event()
	mongo.db.event_data.insert_many(nhl_data)

	# insert 
	mongo.db.stat_summary.remove({})
	stat = scrape_data.summary()
	#print(stat)
	mongo.db.stat_summary.insert(stat)

	return render_template("index.html", data = stat)


if __name__ == "__main__":
	app.run(debug=True)