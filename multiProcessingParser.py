from multiprocessing import Pool
import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

URL = 'https://www.systemrequirementslab.com/all-games-list/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
TEST = 'https://www.systemrequirementslab.com/cyri/requirements/age-of-empires-iii-warchiefs/10699'

def get_html(url):
	response = requests.get(url, headers=HEADERS)
	if response.status_code != 200:
		print("Error")
		return
	return response.text

def get_all_links(html):
	soup = BeautifulSoup(html, 'html.parser')
	dirty_links = soup.find('ul', {'class':'list-unstyled'}).find_all('a')
	all_links = []
	for link in dirty_links:
		all_links.append(link.get('href'))
	return all_links

def get_name(name:str):
	name = name.split()
	return ' '.join(name[0:len(name) - 2])

def get_data(html):
	soup = BeautifulSoup(html, 'html.parser')
	try:
		name = get_name(soup.find('div', {'id':'main'}).find('h1', {'class':'game-description'}).text)
	except:
		name = ''
	try:
		srTemp = soup.find('ul', {'style': 'display: table;padding: 0;padding-left: 20px;'}).find_all('li')
		systemRequirements = {'Name' : name}
		for item in srTemp:
			item = item.text.split(':')
			systemRequirements[item[0]] = item[1]

	except:
		systemRequirements = {} 

	return systemRequirements

def get_all_data(links:list):
	allData = []
	for link in links:
		allData.append(get_data(get_html(link)))
	return allData


def write_to_csv(name:str, data:dict):
	if data == {}:
		with open(name, 'w') as file:
			fieldNames = ['Name', 'CPU', 'CPU SPEED', 'RAM', 'OS', 'VIDEO CARD']
			writer = csv.DictWriter(file, fieldnames=fieldNames)
			writer.writeheader()
	else:
		with open(name, 'a') as file:
			fieldNames = ['Name', 'CPU', 'CPU SPEED', 'RAM', 'OS', 'VIDEO CARD']
			writer = csv.DictWriter(file, fieldnames=fieldNames)
			try:
				writer.writerow({'Name' : data['Name'], 'CPU' : data['CPU'], 'CPU SPEED': data['CPU SPEED'], 'RAM': data['RAM'], 
								'OS': data['OS'], 'VIDEO CARD': data['VIDEO CARD']})
			except: continue

def make_all(link):
	write_to_csv('test.csv', get_data(get_html(link)))


write_to_csv('test.csv', {})
all_links = get_all_links(get_html(URL))
with Pool(15) as process:
	process.map(make_all, all_links[:100])