import requests
import urllib.parse
from bs4 import BeautifulSoup

def scrape_github(search_term, num_pages=1):
	query = urllib.parse.quote_plus(search_term) 
	url = 'https://github.com/search?q=' + query 
	page = requests.get(url)

	soup = BeautifulSoup(page.content, 'html.parser')
	repo_list= soup.find_all('div', class_='mt-n1')

	results_info = []
	
	for repo in repo_list:
		req_info = {}


		repo_name = repo.find('a', class_='v-align-middle').text.strip()
		req_info['repo_name'] = repo_name
		

		description = repo.find('p', class_='mb-1')
		if description == None:
			req_info['description'] = None
		else:
			req_info['description'] = description.text.strip()
		

		tags = repo.find_all('a', class_='topic-tag')
		tag_list = []
		for t in tags:
			tag = t.text.strip()
			tag_list.append(tag)
		if len(tag_list) > 0:
			req_info['tags'] = tag_list
		else:
			req_info['tags'] = None


		num_stars = repo.find('a', class_='Link--muted')
		if num_stars == None:
			req_info['num_pages'] = None
		else:
			req_info['num_stars'] = num_stars.text.strip()
	
	
		
		language = repo.find(itemprop="programmingLanguage")
		if language == None:
			req_info['language'] = None
		else:
			language = language.text.strip()
			req_info['language'] = language
			

		license_info = repo.find_all('div', class_="d-flex flex-wrap text-small color-text-secondary")
		if len(license_info) > 0:
			for element in license_info:
				div_list = element.find_all('div', class_="mr-3")
				
				for tag in div_list:
					text = tag.text.strip()
					has_license = text.find('license')
					if has_license >= 0:
						req_info['license'] = text
						break;
					else: 
						req_info['license'] = None
						

				last_updated = repo.find('relative-time')['datetime']
				req_info['last_updated'] = last_updated
				
				
				issues = element.find('a', class_="Link--muted f6")
				if issues == None:
					req_info['num_issues'] = None
				else:
					issues = issues.text.strip().split()
					req_info['num_issues'] = int(issues[0])
					
		results_info.append(req_info)

	return results_info



def github_api(search_term, num_pages=1):

	
	# Number of items per page
	per_page = 10 * num_pages;

	results_info = []
	
	query   = urllib.parse.quote_plus(search_term)
	url     = "https://api.github.com/search/repositories?q=" + query + '&per_page=' + str(per_page)
	response = requests.get(url).json()

	items = response['items']

	for item in items:
		req_info  = {}

		repo_name = item['full_name']
		req_info['repo_name'] = repo_name

		# if applicable
		description = item['description'] 
		if description == None:
			req_info['description'] = None
		else:
			req_info['description'] = description


		# if applicable
		num_stars = item['stargazers_count']
		if num_stars == None:
			req_info['num_stars'] = None
		else:
			req_info['num_stars'] = int(num_stars)

		#if applicable
		language = item['language']
		if language == None:
			req_info['language'] = None
		else:
			req_info['language'] = language
		
		license = item['license']
		if license == None:
			req_info['license'] = license
		else:
			license = item['license']['name']        
			if  license == 'Other' or license == None:
				license = None
				req_info['license'] = license
			else:
				req_info['license'] = license		
		
		last_updated = item['updated_at']
		req_info['last_updated'] = last_updated
		
		
		has_issues = item['has_issues']
		req_info['has_issues'] = has_issues

		results_info.append(req_info)

	return results_info


 	
# if __name__ == '__main__':
# 	api_results = github_api('image processing')
# 	print(api_results)
	
# 	print()
	
# 	scraped_data = scrape_github('image processing')
# 	print(scraped_data)


