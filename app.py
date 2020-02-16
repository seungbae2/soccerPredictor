from flask import Flask, render_template, request
import predict_model
import os
import csv

saved_hometeam = []
saved_awayteam = []

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
#app._static_folder = os.path.abspath("templates/static/")
# mongo = PyMongo(app, uri = 'mongodb://localhost:27017/nhl_db')

@app.route("/")
def index():
	# insert event data to db
	model = predict_model.model()
	
	hometeam = model['HomeTeam']
	awayteam = model['AwayTeam']

	# print(hometeam)
	# print(awayteam)
	
	# selected_hometeam = request.args.get('type1')
	# selected_awayteam = request.args.get('type2')
	
	# print(selected_hometeam)
	# print(selected_awayteam)

	# saved_hometeam.append(selected_hometeam)
	# saved_awayteam.append(selected_awayteam)

	# print(saved_hometeam)
	# print(saved_awayteam)

	return render_template("index.html", data = model, hometeams = hometeam, awayteams= awayteam)

@app.route("/individual.html")
def savefunction():

	selected_hometeam = request.args.get('type1')
	selected_awayteam = request.args.get('type2')

	# print(selected_hometeam)
	# print(selected_awayteam)

	saved_hometeam.append(selected_hometeam)
	saved_awayteam.append(selected_awayteam)

	# print(saved_hometeam)
	# print(saved_awayteam)

	# model = predict_model.model()
	summary = predict_model.summary()

	hometeam = saved_hometeam[0]
	awayteam = saved_awayteam[0]

	print(summary)

	# print(hometeam)
	# print(awayteam)

	# hometeam = model['HomeTeam']
	# awayteam = model['AwayTeam']

	# percenthomewin = summary['HAS']
	# percentdraw = summary['HDS']
	# percentawaywin = summary['AAS']
	# percentdraws = percentdraw, 

	return render_template("individual.html", data = summary, hometeam = hometeam, awayteam = awayteam)

@app.route("/index.html")
def reset():

	saved_hometeam.clear()
	saved_awayteam.clear()

	model = predict_model.model()
	
	hometeam = model['HomeTeam']
	awayteam = model['AwayTeam']
	
	# print(hometeam)
	# print(awayteam)
	
	# selected_hometeam = request.args.get('type1')
	# selected_awayteam = request.args.get('type2')

	# print(selected_hometeam)
	# print(selected_awayteam)

	# saved_hometeam.append(selected_hometeam)
	# saved_awayteam.append(selected_awayteam)

	# print(saved_hometeam)
	# print(saved_awayteam)

	return render_template("index.html", data = model, hometeams = hometeam, awayteams= awayteam)

if __name__ == "__main__":
	app.run(debug=True)