import logging
import MySQLdb
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
db = MySQLdb.connect(host="webscrapper-instance.c2ay3hczfmtj.us-east-2.rds.amazonaws.com", 
			user="admin_webscrap", 
			passwd="password", 
			db="mlh_data")

cur = db.cursor()


@ask.intent("PlaceIntent")
def find_hackathons_Place(city=None,state=None):
	print(city,state)
	res=None
	resString=""
	if city==None and state==None:
		answer=render_template('NolocationPlaceHolder')
		return statement(answer)
	elif city ==None and state!=None:
		city=state
		res=cur.execute("Select name from hackathon where state=%s",(state,))
	elif state==None and city!=None:
		res=cur.execute("Select name from hackathon where city=%s",(city,))
		data = cur.fetchall()
		for row in data:
			for itr in row:
				resString=resString+str(itr)+","
		resString = city + " , "+resString
		answer=render_template('locationPlaceHolder',city=resString)
		print(resString)
		return statement(answer)
	elif state !=None and city!=None:
		pass
	answer=render_template('locationPlaceHolder', city=city)
	return statement(answer)



@ask.launch
def start_app():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


if __name__ == '__main__':

    app.run(debug=True)



