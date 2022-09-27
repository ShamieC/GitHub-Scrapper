from scraper import *
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///repositories.db"

db = SQLAlchemy(app)

global initialised_database 
initialised_database = False

class repos_db(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	repo_name  = db.Column(db.String(1000))
	description = db.Column(db.String(1000))
	num_stars  = db.Column(db.String(1000))
	language  = db.Column(db.String(1000))
	license = db.Column(db.String(1000))
	last_updated = db.Column(db.String(1000))
	has_issues =db.Column(db.String(1000))


@app.route('/')
def application():
	return render_template("searchpage.html") 

@app.route('/paginated_api_results/<int:page_num>')
def paginated_api_results(page_num):
	repo_db_objects = repos_db.query.paginate(per_page=10, page=page_num, error_out=True)
	return render_template('api_results.html', repos=repo_db_objects)
	

@app.route('/api_results', methods = ['POST', 'GET'])
def api_results():

	if request.method == 'POST':
		query = request.form['query']
		if query == '':
			return 'Search term missing.'
		number_of_pages_str = request.form['number_of_pages']
		if number_of_pages_str == '':
			return 'You did not specify number of pages for the API search'
		n = number_of_pages_str.strip()
		number_of_pages_int = int(n)
		repos = github_api(query, number_of_pages_int)
		num_of_rows = len(repos)

		global initialised_database
		if initialised_database == True:
			meta = db.metadata
			for table in reversed(meta.sorted_tables):
				db.session.execute(table.delete())
			db.session.commit()

		db.create_all()
		initialised_database = True

		for i in range(num_of_rows):
			repo_name = repos[i]['repo_name']
			description = repos[i]['description']
			num_stars = repos[i]['num_stars']
			if repos[i]['language'] == None:
				language = 'None'
			else:
				language = repos[i]['language']
			if repos[i]['license'] == None:
				license = 'None'
			else:
				license = repos[i]['license']
			last_updated = repos[i]['last_updated']
			if repos[i]['has_issues'] == None:
				has_issues = 'None'
			elif repos[i]['has_issues'] == True:
				has_issues = 'True'
				has_issues = str(has_issues)
			elif repos[i]['has_issues'] == False:
				has_issues = 'False'
			row_entry = repos_db(repo_name=str(repo_name), description=description, num_stars=num_stars, language=language, license=license, last_updated=last_updated, has_issues=has_issues)
			db.session.add(row_entry)
			db.session.commit()

		return redirect(url_for('paginated_api_results', page_num=1))



@app.route('/scraper_results', methods = ['POST', 'GET'])
def get_scraper_query():
	if request.method == 'POST':
		query = request.form['query']
		repos = scrape_github(query)
		return render_template('scraper_results.html', repos=repos)
		

if __name__ == '__main__':
   app.run(debug=True)
