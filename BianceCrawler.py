#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Dev : dev1ender@gmail.com
"""
# This is liberay for the html parser
from lxml import html
#lib to handle the https requests
import requests
#lib for the datetime format 
from datetime import datetime

import time


#This is the requered method which take argument 
def get_Binance_listings(last_datetime):
   #this variable hold the url that conatin all the listing of the coin
   Url = "https://support.binance.com/hc/en-us/sections/115000106672-New-Listings"
   #this variable hold the last date till which the listing to be done 
   last_date = last_datetime
   #this is the list which hold list of post data in the format of 
   #[listing_datetime,listing_coin,text]
   new_listings = []
   #this variable hold the address of the new listing page which will we updated 
   #when we move to the next new_listing page 
   links_page_url = Url
   
   #This method will append the listing before the given date 
   def get_post(Url,date):
       #converting the last_date/given date to datetime type
       last_date = datetime.strptime(date, "%d/%m/%Y")
       #it is a list of all the post urls on the new_listing page
       listing_urls = get_listing_links(Url)
       #this counter is secerate counter which used to check end of the 
       #listing_url and do we have to fetch and append some more post urls 
       #to listing_urls or not
       counter=1
       # this loop will loop through all the post urls 
       for link in listing_urls:
           #this is the condition to check do we reached end of the list or not
           if (counter == len(listing_urls)):
               #if we reached end of the list we will move to next page from 
               #pegination and fetch all the links and extend our listing_url list
               listing_urls.extend(page_turn_over(links_page_url))
           #this list hold the date of the data of the single post 
           complete_post_data = get_listing_post_data(link)
           #we will check do we have to append this post data to new_listing list
           #or not by checking its date 
           if complete_post_data[0] > last_date:
               #if the post date is greater than the last_date/given date then
               # we will append this post data to the new_listing list 
               new_listings.append(complete_post_data)
               #and increment the counter 
               counter=counter+1
            time.sleep(5)
           # if the post date is less than the last date then we will break 
           # the loop and stop further scraping as the listing is in asc order
           else:
               break
        
    # this method will help you turn to next page of new_listing
   def page_turn_over(link):
       #this is the global url varible that to be update 
       global links_page_url
       #this request the page from the server
       start_page = requests.get(link)
       #This will parse the page into the Dom
       tree = html.fromstring(start_page.text)
       # this will fetch the next listing_page url from the 
       #pegination that is at the bottom of the page 1  2 3 ... 
       next_page_xpath = tree.xpath('//a[@rel="next"]/@href')[0]
       #this will convert the url into the absoulte url for the next page
       next_page_absolute_path = 'https://support.binance.com'+next_page_xpath
       #this update the links_page_url which will be used to go more deeper in the listing
       links_page_url = next_page_absolute_path
       #this will get all the links on next new listing page 
       links = get_listing_links(next_page_absolute_path)
       #return the list of the links 
       return links
       
       
   # this method return all the URL form the new listing page which absoule Url 
   def get_listing_links(link):
       # this requests the page form the server 
       start_page = requests.get(link)
       #This will parse the page into the Dom
       tree = html.fromstring(start_page.text)
       #it store the list of all the links of the listing 
       links = tree.xpath('//a[@class="article-list-link"]/@href')
       #this lamda fucntion which will complete the hyper link into absolute URL 
       complete_Url = ['https://support.binance.com'+link for link in links ]
       #return the list of absolute URl 
       return complete_Url
   
    #this method will scrap the post page of the every Url and return the coin datetime and post text 
   def get_listing_post_data(link):
       link_page = requests.get(link)
       tree = html.fromstring(link_page.text)
       #this will fetch the post heading using the xpath and strip the white space
       #and split into the array using space a delimiter
       post_title = tree.xpath('//h1[@class="article-title"]/text()')[0].strip().split(" ")
       #This will featch the coin name using the lamda fuction on the array of the post_tile and 
       #check for the upper case word and fetch the frist word 
       listing_coin = [coin.strip("()") for coin in post_title if coin.isupper()][0].split("/")[0]
       #ths will fetch the date from the page in the format Maay 21 2018 21:50
       date = tree.xpath('//time/text()')[0].strip().replace(",", "")
       #this will convert the the date into the datetime format?datatype 
       listing_datetime = datetime.strptime(date, '%B %d %Y %H:%M')
       #this will fetch the all text of the article 
       text = tree.xpath('//div[@class="article-body"]//text()')
       #return the list of of the fetch data 
       return [listing_datetime,listing_coin,text]
   #this will start the scraping of the given url till last_date
   get_post(Url,last_date) 
   #this will return the list of lists of data in the format [data_lsit1,datalist2,datalist3...]
   # where datalisti looks like this [listing_datetime,listing_coin,textlist]
   #textList is also a list of post text whose format is still maintained and stored in a llist
   return new_listings


get_Binance_listings("10/10/2008")




