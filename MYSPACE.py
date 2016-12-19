from selenium import webdriver
import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import re
import os
import urllib

URL = 'https://myspace.com/signin'
driver = webdriver.Chrome(executable_path='/Users/ryan/Desktop/Programming/recipe_attempts/chromedriver')


driver.get(URL)


#login
e = driver.find_element_by_id("login.email")
e.send_keys('andtowhatdoiowe@yahoo.com')

e = driver.find_element_by_id("login.password")
e.send_keys('bestidea1')

e = driver.find_element_by_class_name("primary")
e.click()


#access albums
time.sleep(3)

driver.get("https://myspace.com/library/mixes")

e = driver.find_element_by_class_name("flexColumns")
text = e.text


e = driver.find_elements_by_class_name("noMedia")


#create list of links to albums
albums = []
for x in e:
	y = x.get_attribute('innerHTML')

	m = re.search('href=\"(.*?)\"', y)
	match = y[m.start():m.end()]
	match = match[7:-1]
	print('MATCH',match)
	albums.append(match)

albums = list(set(albums))

albumPhotos= {}



#iterate over each album, store photo links in dictionary for download later
for a in albums:

	time.sleep(1)
	link = "https://myspace.com/" + a

	driver.get(link)

	#get width of page continually scroll until we hit end so we see all the pictures
	width = driver.find_element_by_id("parallax").get_attribute('scrollWidth')
	oldWidth = int(width)

	driver.execute_script("document.getElementById('parallax').scrollLeft += " + str(width) + ";")

	time.sleep(1)

	while int(driver.find_element_by_id("parallax").get_attribute('scrollWidth')) > oldWidth:
		oldWidth = int(driver.find_element_by_id("parallax").get_attribute('scrollWidth'))
		driver.execute_script("document.getElementById('parallax').scrollLeft = " + str(oldWidth) + ";")
		time.sleep(1)


	#we've scrolled all the way, lets access and store picture links now	
	e = driver.find_elements_by_class_name("photo")

	photos = []
	for x in e:
		y = x.get_attribute('innerHTML')

		m = re.search('src=\"(.*?)\"', y)
		if m:
			match = y[m.start():m.end()]
			match = match[5:-1]
			# print('MATCH',match)
			photos.append(match)

	albumPhotos[a] = photos






#start downloading all the photos
root = os.getcwd()


for a in albumPhotos.keys():
	print('Downloading Album:', a )
	os.chdir(root)

	if not os.path.exists(a):
		os.makedirs(a)

	os.chdir( root + "/" + a)

	i = 1
	for p in albumPhotos[a]:
		item = 'Downloading: ' + str(i) + '/' + str(len(albumPhotos[a]))
		print(item, sep=' ', end='\r', flush=True)
		i +=1
		name = str(i) + ".jpg"
		urllib.request.urlretrieve(p, name)

os.chdir(root)









