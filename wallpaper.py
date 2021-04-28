from requests import get
import json , subprocess , getpass
import random as rdm
import time
import pprint

APP_ID = "46OdirGqDll9GBcN6FAr1NwWP3GOl-454Xs8sDMIXEg"
URL = "https://api.unsplash.com/search/photos/"
FILE_PATH = "/home/pranav/unsplash/"
PAYLOAD = {"per_page":10000,"page":1,"orientation":"landscape"}


def fetchImage(app_id , url ,query, payload):
  r = get(url+"?query="+query,params=payload ,headers={'Authorization': 'Client-ID '+app_id}).json()
  #pprint.pprint(r)
  randomNumber = rdm.randint(0, len(r["results"]))
  downLink = r["results"][randomNumber]["links"]["download_location"]
  id = r["results"][randomNumber]["id"]
  downLink = get(downLink,headers={'Authorization': 'Client-ID '+app_id}).json()
  downLink = downLink["url"]
  return downLink,id



def saveImage(file_name , url):
  print("save image to "+file_name)
  # open in binary mode
  with open(file_name, "wb") as file:
    # get request
    response = get(url)
    # write to file
    file.write(response.content)

def setWallpaper(file_name):
  print ("wallpaper set from "+file_name)
  result = subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri" ,"'file://"+file_name+"'"] , stdout=subprocess.PIPE)
  print (result.stdout)

subprocess.call(["notify-send" , "Daily Wallpaper", "fetching image"])
categories = ['wallpaper/','fluid/']
category = rdm.choice(categories)
imageUrl,uniqueID  = fetchImage(APP_ID , URL , category,PAYLOAD)
fileName = FILE_PATH + uniqueID +".jpg"
saveImage(fileName , imageUrl)
setWallpaper(fileName)
subprocess.call(["notify-send" , "Daily Wallpaper", "wallpaper set"])
