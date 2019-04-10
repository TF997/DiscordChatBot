#################
# API INSTALLS
# python3.5 -m |followed by |
# pip install wikipedia | https://pypi.org/project/wikipedia/
# pip install wikipedia-api | https://pypi.org/project/Wikipedia-API/
# pip install beautifulsoup4 | https://pypi.org/project/beautifulsoup4/
# pip install google | https://www.geeksforgeeks.org/performing-google-search-using-python-code/
# pip install weather-api | https://pypi.org/project/weather-api/
# pip install rotten_tomatoes_client | https://pypi.org/project/rotten_tomatoes_client/
# pip install PTable | https://github.com/kxxoling/PTable
#################

import urllib.request
import random
import discord
from discord.ext import commands
import asyncio
import datetime
from datetime import datetime
import time
from datetime import datetime, date, time, timedelta
import calendar
from googlesearch import search
import wikipediaapi
import wikipedia
from weather import Weather, Unit
from prettytable import PrettyTable
#####################################Callum#####################################

##CALLUM'S APIs##
import requests
import json
from rotten_tomatoes_client import RottenTomatoesClient, MovieBrowsingQuery, Service,Genre, SortBy, MovieBrowsingCategory
import html
import random
#################

SReply = False
InHGame = False

cities = "bath birmingham bradford brighton bristol cambridge canterbury carlisle chester chichester coventry derby durham ely exeter gloucester hereford kingston hull lancaster leeds leicester lichfield lincoln liverpool london manchester newcastle norwich nottingham oxford peterborough plymouth portsmouth preston ripon salford salisbury sheffield southampton stalbans stoke-on-trent sunderland truro wakefield westminster winchester wolverhampton worcester york"
location_city = cities.split(" ")
#location_city.lower()
conditions = {"Showers":"shower.png", "Partly Cloudy":"parlycloudy.png","Sunny":"sunny.png", "Cloudy":"cloudy.png", "Breezy":"breezy.png", "snow":"snow.png"}



wiki_wiki = wikipediaapi.Wikipedia('en')
wikipedia.set_rate_limiting(True, min_wait = timedelta(0, 0, 50000))

#Token for the bot to be able to login to discord
TOKEN = "DISCORD DEV TOKEN HERE"
client = discord.Client()

#Opens and wipes the text file which stores the context of the current response
f = open("context.txt", "r+")
f.write("")
f.truncate()

#stores the current date and time
CDT = datetime.now()


#A list and a dictionary, sboring a list of greetings to use, and some responses to a set of preset inputs.
greetings = ["hello", "hi", "howdy", "whassup", "yo", "hey"]
defaultResponses = {
  "haha": "Is something funny? 😂",
  "I am your father": "NooOOooOoOOoOooOOOooo!",
  "thanks": "no problem!",
  "thank you" : "you're welcome!"
}

###########Ben############
@client.event
async def Gsearch(message):
    try:
      QS = str(message.content)
      if 'google' in message.content.lower():
        QS = QS.split('google ',1)
      elif 'wonder' in message.content.lower():
        QS = QS.split('wonder ',1)
      print(str(QS[1]))
      query = str(QS[1])
      msg = "I found these results: ".format(message)
      await client.send_message(message.channel, msg)
      for Result in search(str(query), tld="co.uk", num=1, start=0, stop=3, pause=2):
        msg = "<" + Result.format(message) + ">"
        await client.send_message(message.channel, msg)
    except:
      msg = "I don't understand"

@client.event
async def Wsearch(message):
  Query = str(message.content)
  if 'who is' in message.content.lower():
    Query = Query.split('who is ',1)
  elif 'who' in message.content.lower():
     Query = Query.split('who ',1)
  elif 'what is' in message.content.lower():
     Query = Query.split('what is ',1)
  elif 'what' in message.content.lower():
     Query = Query.split('what ',1)
  elif 'wonder' in message.content.lower():
      Query = Query.split('wonder ',1)
  try:
      msg = str(wikipedia.summary(str(Query[1]), chars = 300)).format(message)
      msg = msg.replace("( listen);"," ")
      await client.send_message(message.channel, msg)
      link = "<" + wikipedia.page(Query[1]).url + ">"
      await client.send_message(message.channel, link)
  except Exception as err:
      await(Gsearch(message))

###########Callum############

#Uses the ODEON API to display a list of the 'hottest' films currently showing.
@client.event
async def getHottestFilms(message):
  odeonUrl = "https://www.odeon.co.uk/api/v2/"
  cinemasUrl = odeonUrl + "cinemas.json"

  filmsUrl = odeonUrl + "films.json"
  data = requests.get(cinemasUrl).json()

  filmData = requests.get(filmsUrl).json()
  filmList = []
  filmBuzzList = []
  for x in range(0,len(filmData)):
    if abs(howManyDaysAgo(filmData[x]['releaseDate'])) < 60 and int((filmData[x]['groupingId'])) == 0 and int(filmData[x]['performanceCount']) > 100:
      if filmData[x]['buzzRating']['rating'] != "" and filmData[x]['buzzRating']['count'] != "":
          filmList.append(filmData[x]['title'])
          ratingBuzz = float(filmData[x]['buzzRating']['rating'])
          ratingCountBuzz = float(filmData[x]['buzzRating']['count'])

          rating = float(filmData[x]['rating']['count'])
          ratingCount = float(filmData[x]['rating']['count'])
          buzz = float(rating) * float(ratingCountBuzz) * float(ratingCount) * float(ratingBuzz)
          filmBuzzList.append(buzz)

  finalList = [filmList for _,filmList in sorted(zip(filmBuzzList,filmList))]
  msg=("Here is a list of some of the hottest new films:")
  await client.send_message(message.channel, msg.format(message))
  for x in range(len(finalList)-1, len(finalList)-7, -1):
    #msg=(finalList[x] + " (RT: " + str(getRottenTomatoesScore(finalList[x])) + "%)")
    msg=(finalList[x])
    await client.send_message(message.channel, msg.format(message))
  return

#Uses the ODEON API to display additional inrotation about a specific cinema
@client.event
async def showCinemaInfo(answer, message):
  odeonUrl = "https://www.odeon.co.uk/api/v2/"
  cinemasUrl = odeonUrl + "cinemas.json"
  data = requests.get(cinemasUrl).json()
  for x in range(0,111):
      if answer.title() == data[x]['name']:
        msg= html.unescape(data[x]['information']['contact'])
        await client.send_message(message.channel, msg.format(message))
        msg= 'Telephone: ' + html.unescape(data[x]['telephone'])
        await client.send_message(message.channel, msg.format(message))
        msg= "Would you like more information about ODEON " + data[x]['name'] + "?"
        setContext(data[x]['name'] + " even more info")
        await client.send_message(message.channel, msg.format(message))
  return

#Finds and displays the Rotten Tomatoes Critic score for a specific film.
@client.event
async def getRottenTomatoesScore(filmName, message):
  RTSearch = RottenTomatoesClient.search(term=filmName, limit=5)
  try:
    msg = (str(RTSearch['movies'][0]['name']) + " Has a critic score of " + str(RTSearch['movies'][0]['meterScore']) + "%").format(message)
    await client.send_message(message.channel, str(msg))
    msg = calculateStars(RTSearch['movies'][0]['meterScore'])
    await client.send_message(message.channel, str(msg))
    msg = "Is this what you were looking for?"
    setContext(filmName + " rt right film")
    await client.send_message(message.channel, str(msg))
  except :
    msg = "I'm not sure about that. Enter the name of a film and I can provide the Rotten Tomatoes critic score."
    await client.send_message(message.channel, str(msg))
    setContext("rt get score")


#Uses the ODEON API, and takes a postcode input to find the nearest ODEON cinemas in that area.
@client.event
async def findNearbyCinemas(message):
  f = open("context.txt", "r+")
  odeonUrl = "https://www.odeon.co.uk/api/v2/"
  cinemasUrl = odeonUrl + "cinemas.json"

  filmsUrl = odeonUrl + "films.json"
  data = requests.get(cinemasUrl).json()
  inputString = message.content.lower()

  if any(char.isdigit() for char in inputString):
    sentence = message.content.lower().split()
    for x in range(0, len(sentence)):
      for x in range(0, len(sentence)):
        try:
          if not any(char.isdigit() for char in sentence[x]):
            del sentence[x]
        except IndexError:
          continue
    postcode = ' '.join(sentence).upper()
    nearbyCinemas = []
    for x in range(0,111):
      if postcode[0:4] in data[x]['address']['postcode']:
          nearbyCinemas.append(data[x]['name'])
      elif postcode[0:3] in data[x]['address']['postcode']:
          nearbyCinemas.append(data[x]['name'])
      elif postcode[0:2] in data[x]['address']['postcode']:
          nearbyCinemas.append(data[x]['name'])
    if len(nearbyCinemas) > 0:
      msg=("Here is a list of nearby ODEON cinemas.")
      await client.send_message(message.channel, msg.format(message))
      for x in range(0, len(nearbyCinemas)):
        msg=(nearbyCinemas[x])
        await client.send_message(message.channel, msg.format(message))
      msg=("Would you like more info about these cinemas?")
      await client.send_message(message.channel, msg.format(message))
      setContext(postcode + " more information cinemas")
    else:
      msg= "Sorry, I couldn't find any nearby ODEON cinemas"
      await client.send_message(message.channel, msg.format(message))
      setContext("")
  else:
    msg= "Enter a postcode to find your nearest ODEON cinema"
    await client.send_message(message.channel, msg.format(message))
    setContext("get postcode")
  return

#Sets the 'CONTEXT' to a specific string value. This is used for getting responses to specific questions or requests.
def setContext(contextToSet):
  f.seek(0)
  f.write(contextToSet)
  f.truncate()

#Calculates how many star symbols to display based on the Rotten Tomatoes score for a film.
def calculateStars(meterScore):
  numberOfStars = round(meterScore/20)
  #print(numberOfStars)
  rating = ""
  for x in range(numberOfStars):
    rating = rating + "★"
  for x in range(5-numberOfStars):
    rating = rating + "☆"
  return(rating)

#Used for fformatting the release dates stored in ODEON's API.
def convert(s):
    return datetime.strptime(s, '%Y/%m/%d').date()

#Calculates how many days ago a specific date was... used for calculating how long ago any film came out
def howManyDaysAgo(releaseDate):
  d0 = datetime.today().date()
  d1 = convert(releaseDate)
  delta = d1 - d0
  return (delta.days)

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    content = message.content
    channel = message.channel

    #Wipes the context variable's current value and retrieves the new value from the context.txt file.
    context = "..."
    f = open("context.txt", "r+")
    context = f.read()

    #In the case that the user enters any of the preset greetings, the bot will respond with a random greeting from the same list.
    if message.content.lower() in greetings or message.content.lower() + "!" in greetings:
      msg = greetings[random.randint(0, len(greetings) - 1)].title() + "!"
      await client.send_message(message.channel, msg.format(message))

    #If the context demands that the user enter their postcode...
    if context == "get postcode":
      await findNearbyCinemas(message)

    #Provides even more info about cinema.
    elif "even more info" in context:
      setContext("")
      odeonUrl = "https://www.odeon.co.uk/api/v2/"
      cinemasUrl = odeonUrl + "cinemas.json"

      filmsUrl = odeonUrl + "films.json"
      data = requests.get(cinemasUrl).json()
      cinemaName = context.split()
      for x in range(0, len(cinemaName)):
        for x in range(0, len(cinemaName)):
          try:
            if "info" in cinemaName[x] or "even" in cinemaName[x] or "more" in cinemaName[x]:
              del cinemaName[x]
          except IndexError:
            continue
      cinema = ' '.join(cinemaName).title()
      for x in range(0,111):
        if cinema == data[x]['name']:
          if "yes" in message.content.lower():
            msg = str(html.unescape(data[x]['information']["location"]))
            await client.send_message(message.channel, msg.format(message))
            msg = 'Driving Directions: ' + html.unescape(data[x]['information']['drivingDirections'])
            await client.send_message(message.channel, msg.format(message))
            msg = html.unescape(data[x]['information']['localFacilities'])
            await client.send_message(message.channel, msg.format(message))
          else:
            msg = "okay."
            await client.send_message(message.channel, msg.format(message))


    #The bot will ask if it has displayed the correct film (Rotten Tomatoes Search). This deals with the response to that query.
    elif "rt right film" in context:
      filmName = context.split()
      for x in range(0, len(filmName)):
        for x in range(0, len(filmName)):
          try:
            if "rt" in filmName[x] or "right" in filmName[x] or "film" in filmName[x]:
              del filmName[x]
          except IndexError:
            continue
      film = ' '.join(filmName).title()

      #...if not, then the bot offers other films which come under the same search.
      if "no" in  message.content.lower():
        await client.send_message(message.channel, "Okay, here are some similar options:".format(message))
        RTSearch = RottenTomatoesClient.search(term=film, limit=5)
        for x in range(1, len(RTSearch['movies'])-1, 1):
          msg = (str(RTSearch['movies'][x]['name']) + "").format(message)
          await client.send_message(message.channel, msg.format(message))
          msg = str(RTSearch['movies'][x]['meterScore']) + "%:     " + calculateStars(RTSearch['movies'][x]['meterScore'])
          await client.send_message(message.channel, str(msg))
          setContext("")
      else:
        await client.send_message(message.channel, "Okay.".format(message))
        setContext("")

    #This is the case in which the bot cannot find the Rotten Tomatoes Score for the requested film, and so asks the user to query a different title.
    elif context == "rt get score":
      filmName = message.content
      await getRottenTomatoesScore(filmName, message)


    #The case in which the user has requested more information about a cinema
    elif "more information cinemas" in context:
      odeonUrl = "https://www.odeon.co.uk/api/v2/"
      cinemasUrl = odeonUrl + "cinemas.json"
      data = requests.get(cinemasUrl).json()

      postcodeSentence = context.split()
      for x in range(0, len(postcodeSentence)):
        for x in range(0, len(postcodeSentence)):
          try:
            if "more" in postcodeSentence[x] or "information" in postcodeSentence[x] or "cinemas" in postcodeSentence[x]:
              del postcodeSentence[x]
          except IndexError:
            continue
      postcode = ' '.join(postcodeSentence).upper()
      print(postcode)
      nearbyCinemas = []
      for x in range(0,111):
        if postcode[0:4] in data[x]['address']['postcode']:
            nearbyCinemas.append(data[x]['name'])
        elif postcode[0:3] in data[x]['address']['postcode']:
            nearbyCinemas.append(data[x]['name'])
        elif postcode[0:2] in data[x]['address']['postcode']:
            nearbyCinemas.append(data[x]['name'])
      if message.content.lower() == "yes" or message.content.title() in nearbyCinemas:
        if message.content.title() in nearbyCinemas:
          setContext("")
          await showCinemaInfo(message.content, message)
        else:
          msg= "For which one?"
          await client.send_message(message.channel, msg.format(message))

    #When the user is asked for which specific cinema they would like more information on, the information for that cinema is displayed once they respond.
    elif context == "for which cinema":
      showCinemaInfo(message.content, message)
      setContext("")

    #Responds to the user's input if they enter any of the preset inputs for the 'default responses' dictionary.
    if message.content.lower() in defaultResponses:
      msg = defaultResponses[message.content.lower()]
      await client.send_message(message.channel, msg.format(message))


#####################################BEN#####################################


    #Welcome help menu
    if InHGame == False:
      if message.content.startswith('!hello'):
        msg = 'Hello, here are a list of features:\nDisplay the current time, keywords: time is/is the time\nWiki search, keywords: who is/who/what is/what\nFind out the weather in a city, keywords: weather |city|\nGoogle Search, keywords: google/wonder\n To find local cinemas and movie ratings use keywords: Cinema/How good is\n for a joke use keywords: Tell me a joke'.format(message)
        await client.send_message(message.channel, msg)

    #ask what the current time is
    if InHGame == False:
      if 'time is' in message.content.lower() or 'is the time' in message.content.lower():
        if message.content.endswith("time") or message.content.endswith("it"):
          msg = CDT.strftime("%H:%M").format(message)
          await client.send_message(message.channel, msg)

    #search google
    if InHGame == False:
      if 'google ' in message.content.lower():
        if "cinema" not in message.content.lower():
          if "weather" not in message.content.lower():
            if "time" not in message.content.lower():
               if 'hangman' not in message.content.lower():
                  await(Gsearch(message))

     #wiki search
    if InHGame == False:
      if 'hangman' not in message.content.lower():
        if 'who is' in message.content.lower() or 'who' in message.content.lower() or 'what is' in message.content.lower() or 'what' in message.content.lower() or 'wonder ' in message.content.lower():
          if "cinema" not in message.content.lower():
            if "weather" not in message.content.lower():
              if "time" not in message.content.lower():
                  await(Wsearch(message))
############################Goncalo############################################
    global InHGame
    #If the message has hangman in it, the bot starts the hangman game
    if 'hangman' in message.content.lower():
      InHGame = True
      await hangman(message)
      InHGame = False



#####################################Callum#####################################

    #The user can ask how good a film is. The question is then cut up, so that the film title can be deduced, and the function is run.
    if InHGame == False:
      if 'how good is' in message.content.lower() or 'rotten tomatoes' in message.content.lower():
        sentence = message.content.lower().split()
        for x in range(0, len(sentence)):
          for x in range(0, len(sentence)):
            try:
              if sentence[x] == 'how' or sentence[x] == 'good' or sentence[x] == 'is' or sentence[x] == '?':
                del sentence[x]
            except IndexError:
              continue
        filmName = ' '.join(sentence)
        await getRottenTomatoesScore(filmName, message)

    #If the user makes a cinema-specific query, then, based on their input, either the nearest cinemas are shown, or the hottest films displayed.
    if InHGame == False:
      if 'cinema' in message.content.lower() or 'movie' in message.content.lower() or 'film' in message.content.lower():
        if 'movies out' in message.content.lower() or 'new movies' in message.content.lower() or 'new films' in message.content.lower() or ('what' in message.content.lower() and 'on' in message.content.lower()) or 'coming out' in message.content.lower():
          await getHottestFilms(message)
        elif 'nearby' in message.content.lower() or 'near me' in message.content.lower() or 'closest cinema' in message.content.lower() or 'nearest' in message.content.lower() or ' playing ' in message.content.lower():
          await findNearbyCinemas(message)

############################################  Weather/Forecast #####################  Haider  #########################################
    content = message.content
    channel = message.channel
    global SReply ###Ben's fix for dealing with holding context.

    if "sunny" in message.content.lower() or "cloudy" in message.content.lower() or "rain" in message.content.lower() or "day" in message.content.lower() or "weather" in message.content.lower() or "cold" in message.content.lower():  ## fixed so it will pickup if theyre in the message or not - Ben
        SReply = True ###Ben's fix for dealing with holding context.
        LCheck = str(message.content)
        LCheck = LCheck.split(" ")
        print(LCheck)
        print("Working")
        for i in range(0,len(LCheck)):
          print("Running")
          print(LCheck[i] in location_city)
          if str(LCheck[i]) in location_city:
            for value in location_city:
              if "forecast" in content.lower() or "weather forecast" in content.lower():
                  #reply = "I dont know where you live, To know the weather tell me where you live?".format(message)
                  #await client.send_message(message.channel, reply)
                  forcaste = weatherTable(value)
                  await client.send_message(message.channel,forcaste )
                  SReply = False ###Ben's fix for dealing with holding context.
                  break
              elif ("weather" and value.lower()) in content.lower():
                image = ""
                weather = weatherLookup(value)
                msg  = "its "+ weather + " in " + value
                for k,v in conditions.items():
                  if k in msg:
                    image = v
                    SReply = False ###Ben's fix for dealing with holding context.
                    break
                await client.send_message(message.channel, msg)
                SReply = False ###Ben's fix for dealing with holding context.
                await client.send_file(channel, image)
                break
            return
        reply = "I dont know where you live, To know the weather tell me where you live?".format(message)
        await client.send_message(message.channel, reply)
        """
    if  content.lower() == "weather":
        reply = "I dont know where you live, To know the weather tell me where you live?".format(message)
        SReply = True ###Ben's fix for dealing with holding context.
        await client.send_message(message.channel, reply)
        """

    if SReply == True:
      # check the city name in userMessage and send the weather report
      for value in location_city:
          if ("weather" and value.lower()) in content.lower():
            image = ""
            weather = weatherLookup(value)
            msg  = "its "+ weather + " in " + value
            for k,v in conditions.items():
              if k in msg:
                image = v
                SReply = False ###Ben's fix for dealing with holding context.
                break
            await client.send_message(message.channel, msg)
            SReply = False ###Ben's fix for dealing with holding context.
            await client.send_file(channel, image)
            break

    if ("joke" or "tell me a joke") in content.lower():
            _jokes = Jokes("jokes.txt")
            msg = random.choice(_jokes)
            await client.send_message(message.channel, msg, tts=True)

def weatherTable(content):
    """
    input: content as string
    return: weather inforamtion tempreture, condition as a table
    """
    weatherReport = PrettyTable()
    weatherReport.field_names = ["conditions", "Date", "High", "Low"]
    weather = Weather(unit=Unit.CELSIUS)
    location = weather.lookup_by_location(content)
    forecasts = location.forecast
    for forecast in forecasts:
        weatherReport.add_row([forecast.text,forecast.date,forecast.high + "°",forecast.low+"°"])
        weatherReport.add_row(["  ", "  ", "  ", "  "])
        weatherReport.add_row(["  ", "  ", "  ", "  "])
    return weatherReport


def Jokes(file_name):

    """
    input: file name eg, text.txt
    retun list with jokes
    """
    file = open(file_name,'r')
    jokes = []
    for value in file:
        value = value.strip('\n')
        jokes.append(value)
    file.close()
    return jokes


def weatherLookup(area):
    """
    Input: Name of city
    Output: weather condition depending on the location/city.
    """
    weather = Weather(unit=Unit.CELSIUS)
    weatherLookp = weather.lookup_by_location(area)
    condition = weatherLookp.condition
    return condition.text
############################Ben############################################

@client.event
#displays 'i am alive!' message followed by the day and turrent time.
async def on_ready():
    print(client.user.name)
    print(client.user.id)
    print("Is Ready & Logged On!")
    await client.send_message(client.get_channel(id= '517262588825042946'), 'I am alive!')
    await client.send_message(client.get_channel(id= '517262588825042946'), '!hello for help')
    await client.send_message(client.get_channel(id= '517262588825042946'), "It is " + calendar.day_name[datetime.today().weekday()] + " today and it is currently: " + CDT.strftime("%H:%M"))

############################Goncalo############################################

global InHGame
#Gets images from their url address for use by the hangman function
urllib.request.urlretrieve("https://www.proprofs.com/games/word-games/hangman/image/First.png?v=1", "hm1.png")
urllib.request.urlretrieve("https://i.stack.imgur.com/RnemK.jpg", "hm2.png")
urllib.request.urlretrieve("https://upload.wikimedia.org/wikipedia/commons/7/70/Hangman-2.png", "hm3.png")
urllib.request.urlretrieve("https://vignette.wikia.nocookie.net/huntik/images/2/27/Hangman-4.png/revision/latest?cb=20130529180834", "hm4.png")
urllib.request.urlretrieve("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStmRYpp6H1qwGlPM_RVwVCHXAGMaDdpbBTVJZvpQjoOWNTlD1niA", "hm5.png")
urllib.request.urlretrieve("https://cdn.instructables.com/FZN/8U7N/JCGKCTA9/FZN8U7NJCGKCTA9.LARGE.jpg", "hm6.png")

hangmanPics = {6:"hm0.png",5:"hm1.png", 4:"hm2.png",3:"hm3.png",2:"hm4.png",1:"hm5.png",0:"hm6.png"}

animalList = []
def listMaker(file, lst):
    """Takes file as input
    and modifies a list appending lines in the file"""
    f = open(file, "r")
    for line in f:
        if line.count(" ") < 1: #So animal names with multiple words dont get added
            lst.append(line[:-1])
listMaker("animalList.txt", animalList)


def slotMaker(word, guess):
    """word: string
       guess: string with only one character
       Creates the slot for word
       and returns it"""
    slot = ""
    for c in word:
        if c in " ":
            slot += " "
        if c in guess:
            slot += c
        else:
            slot += "-"
    return slot


def letterChecker(word, guess):
    """word: string
       guess: string with only one character
       Checks if the letter guessed is part of
       the word"""
    lettersGuessed = ""
    if guess[-1] in word:
        return True
    else:
        return False


@client.event
async def hangman(ctx):
    """Plays the hangman game with the user that invoked the command"""
    guess = ""
    hp = 6
    word = animalList[random.randrange(len(animalList))].lower() #Gets a random animal name from animalList
    slot = slotMaker(word, guess)
    await client.send_message(ctx.channel, "Let`s play the hangman! \n The word is an animal \n" + slot)
    while slot != word and hp > 0: #Continues playing the game until either hp is 0 or the user as guessed all letters
        msg = await client.wait_for_message( author=ctx.author)
        guess += str(msg.content)
        slot = slotMaker(word, guess)
        await client.send_message(ctx.channel,slot)
        if letterChecker(word, guess): #when a user makes a right guess
            if slot == word: #If the user has guessed all letters prints a congratulatory message
              await client.send_message(ctx.channel,"Congrats! You got the word right. Have a cookie: :cookie:")
        else: #When the user makes a wrong guess
            hp -= 1
            await client.send_message(ctx.channel, "Your hp is now " + str(hp) + ".")
            await client.send_file(ctx.channel,hangmanPics[hp])
            if hp == 0:
                await client.send_message(ctx.channel, "Feels bad bro, no cookie for losers.")




client.run(TOKEN)
