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
		data = cur.fetchall()
		for row in data:
			for itr in row:
				resString=resString+str(itr)+","
		resString = city + " , "+resString
		answer=render_template('locationPlaceHolder',city=resString)
		print(resString)
		return statement(answer)
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
		res=cur.execute("Select name from hackathon where city=%s and state=%s",(city,state,))
		data = cur.fetchall()
		for row in data:
			for itr in row:
				resString=resString+str(itr)+","
		resString = city+" "+state+ " , "+resString
		answer=render_template('locationPlaceHolder',city=resString)
		print(resString)
		return statement(answer)
	answer=render_template('locationPlaceHolder', city=city)
	return statement(answer)


@ask.intent("DateIntent")
def find_hackathons_date(startDate=None,endDate=None):
	print(startDate,endDate)
	dateStr = str(startDate)+" and "+str(endDate)
	resString=""
	res=None

	if startDate!=None and endDate!=None:
		res=cur.execute("select name from hackathon where startDate>=%s and endDate <=%s",(startDate,endDate,))
		if res>0:
			data=cur.fetchall()
			for row in data:
				for itr in row:
					resString=resString+str(itr)+","
			resString = dateStr+" are "+resString
			answer=render_template('date',res=resString)
			print(resString)
			return statement(answer)
		elif res == 0:
			answer=render_template('noAnswer')
			return question(answer) 	
	elif startDate!=None and endDate==None:
		res=cur.execute("select name,city,state from hackathon where startDate=%s",(startDate,))
		if res>0:
			data=cur.fetchall()
			for row in data:
				resString=resString+str(row[0])+" at "+row[1]+" "row[2]+ ","	
			resString = str(startDate)+" are "+resString
			answer=render_template('onDate',res=resString)
			print(resString)
			return statement(answer)
		elif res ==0:
			answer=render_template('noAnswer')
			return question(answer)

	elif startDate==None and endDate == None:
		answer=render_template('noAnswer')
		return question(answer)
	answer=render_template('date',)


@ask.launch
def start_app():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


if __name__ == '__main__':

    app.run(debug=True)



