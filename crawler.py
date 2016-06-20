#!/usr/bin/env python
# coding: utf-8
#-Ochasen -d /usr/local/lib/dic/mecab-ipadic-neologd/
#crawl data from Yahoo rss and get meta information from wiki
#Check whether noun is stored in Neologd

import MeCab
import urllib
import lxml.html
import lxml.etree as et
import time
import csv

#input = u'よく東日本旅客鉄道が好き'
#mt = MeCab.Tagger("-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
#input = input.encode("utf-8")
#node = mt.parseToNode(input)
#while node:#
#	print node.surface, node.feature
#	node = node.next

#def analyze_sentence():


#get all rss information from Yahoo news rss list
def get_rss_from_Yahoo(yahoo):
	print("start get_rss_from_Yahoo")
	result = [];

	html_string = urllib.urlopen(yahoo)
	
	html_element = lxml.html.fromstring(html_string.read().decode("utf-8"));
	html_string.close();

	listbox = html_element.xpath('.//div[@class="rss_listbox"]')
	#print(listbox)
	for box in listbox:
		li = box.xpath('descendant::li')
		for link in li:
			url = [];
			temp = link.xpath('descendant::a')
			url.append(temp[1].get('href'))
			#print (url)
			result.append(url)

	print("end get_rss_from_Yahoo")
	return result
	
def write_to_csv(file, data):
	with open(file, 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(data)

def write_add_csv(file, data):
	#print(data)
	with open(file, 'a') as f:
		writer = csv.writer(f)
		writer.writerow(data)


#def get_news_from_rss():

def get_sentence_from_rss(news_rss):
	print("start get_sentence_from_rss")
	result = [];

	for news in news_rss:	
		file = urllib.urlopen(news[0])
		tree = et.fromstring(file.read())
		#print(tree)
		#root = tree.Element("rss")
		file.close()

		for title in tree.iter('title'):
			temp = [];
			temp.append(title.text.encode("utf-8"))
			temp.append(news[0]);
			#print(title.text)
			result.append(temp);

	print("end get_sentence_from_rss")
	return result


def get_entry_from_sentence(sentences):
	print("start get_entry_from_sentence")
	result = []


	mt = MeCab.Tagger("-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
	for sentence in sentences:
		temp = sentence[0]

		node = mt.parseToNode(temp)
		while node:
			#print node.surface
			if node.feature.find("名詞") != -1:
				word = [];
				#print "yes!"+node.surface
				word.append(node.surface)
				word.append(sentence[1])
				result.append(word)
			else:
				result.append("#")
			node = node.next
		result.append("#")

		#write_to_csv(entry_file, result)

	print("end get_entry_from_sentence")
	return result


def check_entry(entries):
	wiki = "https://ja.wikipedia.org/w/index.php?redirect=0&title="
	new_meta_file = "meta_entries.csv"
	new_entry_file = "new_entries.csv"
	temp = ""
	meta_data = []
	new_data = []
	i = 0
	j = 0
	for entry in entries:		
		if entry[0] == "#":
			temp = ""
			continue
		else:				
			meta = get_meta_from_wiki(wiki+entry[0], entry[0])
			if meta != -1:
				
				data = [];
				#print(entry[0]+"+"+meta)
				data.append(entry[0])
				data.append(meta)
				#print(data)
				data.append(entry[1])
				data.append("meta");
				#print(data)
				write_add_csv(new_meta_file, data)	
				i = i+1
			
			if temp != "":
				pron = get_pronunciation(wiki+entry[0], temp+entry[0])
				if pron != -1:
					data = [];
					data.append(entry[0])
					data.append(pron)
					data.append(entry[1])
					data.append("new")
					write_add_csv(new_entry_file, data)
					j = j+1

			info = 'meta:' + str(i) + ';new:' + str(j)
	    	print(info)
	
		
	

def get_pronunciation(wiki, entry):
	print("start get_pronunciation")
	result = [];

	html_string = urllib.urlopen(wiki)
	
	html_element = lxml.html.fromstring(html_string.read().decode("utf-8"));
	html_string.close();

	titlediv = html_element.xpath('.//div[@id="mw-content-text"]')

	if titlediv != -1:
		p = titlediv[0].xpath('descendant::p')
		pron = p[0].text_content().encode("utf-8");
		start = pron.find("(")
		end = pron.find(")")
		pron = pron[start+1:end-1]
		print("end get_pronunciation")
		return pron
	else:
		print("end get_pronunciation")
		return -1

def get_meta_from_wiki(wiki, entry):
	print("start get_meta_from_wiki")
	result = "";

	html_string = urllib.urlopen(wiki)
	
	html_element = lxml.html.fromstring(html_string.read().decode("utf-8"));
	
	html_string.close();

	titlediv = html_element.xpath('.//div[@id="mw-content-text"]')
	
	p = titlediv[0].xpath('descendant::p')
	if len(p) != 0:

		p = titlediv[0].xpath('descendant::p')

		#print len(p)
		meta = p[0].text_content().encode("utf-8");
		#print meta
		#start = meta.find('、')
		end = meta.find('。')
		#print(end)
		result = meta[0:]
		#print result
		print("end get_meta_from_wiki")
		return result
	else:
		print("end get_meta_from_wiki")
		return -1
	



if __name__ == "__main__":

	rss_resourse = "http://headlines.yahoo.co.jp/rss/list"
	wiki = "https://ja.wikipedia.org/w/index.php?redirect=0&title="
	dic = "-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/"
	new_entry_file = "new_entries.csv"
	new_meta_file = "meta_entries.csv"
	rss_list_file = "rss_list.csv"
	sentence_file = "sentence_list.csv"
	entry_file = "crawler entry.csv"

	print ("start")
	time_start = time.time();
	# 10 minutes to crawl
	if int(time.time()-time_start) != 60*10:
		news_rss = []
		sentences = []

		#get rss_list		
		news_rss = get_rss_from_Yahoo(rss_resourse)
		write_to_csv(rss_list_file, news_rss)

		#get content of every rss
		sentences = get_sentence_from_rss(news_rss)
		write_to_csv(sentence_file, sentences)
		
		#get entry from sentence 
		
		entries = get_entry_from_sentence(sentences);
		write_to_csv(entry_file, entries)

		#check if stored in Neologd and do action
		check_entry(entries);




	

