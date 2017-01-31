import json
import requests
from lxml import html
import roman
from datetime import datetime
import click

domainUrl = 'http://www.depthcore.com'
allWorksUrl = domainUrl + '/work/'
chapterUrl = domainUrl + '/chapter/'
artWorkUrl = domainUrl + '/img/artwork/'

with requests.Session() as downloadSession:
	# Makes the server think this is firefox accessing it, probably not neccessary but I did it anyways. This is called a User-Agent.
	downloadSession.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',})

	# Download the main page that shows all chapters
	page = downloadSession.get(allWorksUrl)
	pageTree = html.fromstring(page.content)
	
	# Used firebug on firefox to inspect the correct element (title, image, artist, etc.) and once highlighted right clicked and copied XPath
	chapterNumberList = pageTree.xpath('/html/body/div[2]/div/div[*]/div/div[1]/strong/text()')
	chapterUrlList = pageTree.xpath('/html/body/div[2]/div/div[*]/div/h2/a/@href')
	chapterNameList = pageTree.xpath('/html/body/div[2]/div/div[*]/div/h2/a/text()')
	chapterDateList = pageTree.xpath('/html/body/div[2]/div/div[*]/div/div[1]/span/text()')
	
	# Iterate through chapterUrlList and create the LIST of DICTIONARIES so we can easily lookup the chapter and image info (i.e. (type list).append((type dictionary))
	# Notice the empty images list on the end. That is because we are going to populate it with all the images for a chapter here in a sec
	allData = []
	for indexChapter,chapterUrl in enumerate(chapterUrlList):
		print('Progress: ' + str(indexChapter + 1) + '/' + str(len(chapterUrlList)))
		allData.append({'chapterNumber': roman.fromRoman(chapterNumberList[indexChapter][8:]), 'chapterUrl': chapterUrl, 'chapterTitle': chapterNameList[indexChapter], 'chapterDate': datetime.strptime(chapterDateList[indexChapter], '%b %d, %Y').strftime('%Y%m%d'), 'images': []})
	
		# Download the page for the current chapter we are working on
		page = downloadSession.get(domainUrl + chapterUrl)
		pageTree = html.fromstring(page.content)
		
		# Same as for the first set of XPaths, just a different page (one single chapter page)
		chapterImageTitleList = pageTree.xpath('/html/body/div[2]/div/div[3]/div[position()>1]/div[*]/h2/text()')
		chapterImagePageUrlList = pageTree.xpath('/html/body/div[2]/div/div[3]/div[position()>1]/div[*]/div/a/@href')
		
		#------------------------------------------------------
		# This is unique on how it's done because there can be multiple artist but they are just a tags in the html so doing
		# '/html/body/div[2]/div/div[3]/div[position()>1]/div[*]/h3/a/text()' will just add each listed artist to the list
		# What ends up happening is you get X image titles with Y artist. We should get X image titles with X artists where
		# X artist can be a list of artists if an image has more than one artist.
		# -----
		# Instead we pull all a tags from the h3 tag and generate a list of artists (a list of one if there is one artist or a list of z artists if there are z artists for an image)
		# I used a list comprehinsion to do it but I wrote the nested for loop that does the same thing (commented out)
		#------------------------------------------------------
		chapterImageArtistElements = pageTree.xpath('/html/body/div[2]/div/div[3]/div[position()>1]/div[*]/h3')
		chapterImageArtistList = [[artist.text_content() for artist in element] for element in chapterImageArtistElements]
		
				# chapterImageArtistList = []
				# for element in chapterImageArtistElements:
					# artistList = []
					# for artist in element:
						# artistList.append(artist.text_content())
					# chapterImageArtistList.append(artistList)
		
		# The commented for loop is how it is done without the progressbar, you have to uncomment and then delete the with for block and correct the tabbing
		#for indexImage, chapterImagePageUrl in enumerate(chapterImagePageUrlList):
		with click.progressbar(chapterImagePageUrlList) as bar:
			for indexImage, chapterImagePageUrl in enumerate(bar):

				# Download the current image page so we can get the images actual location (url)
				page = downloadSession.get(domainUrl + chapterImagePageUrlList[indexImage])
				pageTree = html.fromstring(page.content)
				
				# So......they are being annoying and somethings it has an a tag, sometimes it doesn't so if it needs an a tag the list is empty
				# Empty list have a value of false. not false is true. If list is empty then do it with the a tag.
				# Found this by it erroring out.
				chapterImageUrlList = pageTree.xpath('/html/body/div[2]/div/div[3]/div[3]/img/@src')
				if not chapterImageUrlList:
					chapterImageUrlList = pageTree.xpath('/html/body/div[2]/div/div[3]/div[3]/a/img/@src')
				
				# If chapterImageUrlList is still somehow empty then just skip that url.
				# Why is this here? Because one of the things it tried to download was a song on soundcloud but there was no link
				if chapterImageUrlList:
					allData[indexChapter][u'images'].append({'imageTitle': chapterImageTitleList[indexImage], 'imageArtist': chapterImageArtistList[indexImage], 'imageUrl': chapterImageUrlList[0]})
	
		#print(allData)
		
		# This dumps to the file on every loop. Yes this is time consuming but when it errors out you will have a dump up to the chapter you finished at least.
		# Suggest put this outside of loop after everything is working
		with open('full_dump_depthcore_20170131.txt', 'w') as outfile:
			json.dump(allData, outfile)
