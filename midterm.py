from flask import Flask, request, render_template, redirect, url_for, flash, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import requests
import json
import re
import wikipedia

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pass123'

class WikiForm(FlaskForm):
	searchword = StringField('Enter the name of a president: ', validators=[ Required() ])
	submit = SubmitField('Submit')

@app.errorhandler(404)
def not_found(e):
	return render_template('404error.html')

@app.errorhandler(505)
def server_error(e):
	return render_template('505error.html')

@app.route('/form')
def wiki_form():
	myform = WikiForm()
	return render_template('wikiform.html', form=myform)

@app.route('/wikiresult', methods=['GET', 'POST'])
def result():
	form = WikiForm(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		searchword = form.searchword.data
		result = request.args
		president = searchword
		president += ' president'
		pres_data = wikipedia.search(president)
		wiki_page = wikipedia.WikipediaPage(pres_data[0])
		pres_summary = wiki_page.summary
		resp = make_response(render_template('wikisummary.html', result=pres_summary))
		resp.set_cookie('result', 'pres_summary')
		return resp
	flash('Please try again!')
	return redirect(url_for('wiki_form'))

@app.route('/wikitext/<president>', methods=['GET', 'POST'])
def wiki_text(president):
	try:
		president += ' president'
		pres_data = wikipedia.search(president)
		wiki_page = wikipedia.WikipediaPage(pres_data[0])
		pres_links = wiki_page.links
		pres_content = wiki_page.content
		return render_template('wikilinks.html', links=pres_links, content=pres_content)
	except:
		flash('Please try again!')
		return redirect(url_for('wiki_form'))

if __name__=='__main__':
    app.run(debug=True)