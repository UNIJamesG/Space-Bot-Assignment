###############################################################
#This is just a starter code for the assignment 1, 
# you need to follow the assignment brief to complete all the tasks required by the assessemnt brief
#
#  This program:
# - Asks the user to enter an access token or use the hard coded access token.
# - Lists the user's Webex rooms.
# - Asks the user which Webex room to monitor for "/seconds" of requests.
# - Monitors the selected Webex Team room every second for "/seconds" messages.
# - Discovers GPS coordinates of the ISS flyover using ISS API.
# - Display the geographical location using geolocation API based on the GPS coordinates.
# - Formats and sends the results back to the Webex Team room.
#
# The student will:
# 1. Import libraries for API requests, JSON formatting, epoch time conversion, and iso3166.
# 2. Complete the if statement to ask the user for the Webex access token.
# 3. Provide the URL to the Webex room API.
# 4. Create a loop to print the type and title of each room.
# 5. Provide the URL to the Webex messages API.
# 6. Provide the URL to the ISS Current Location API.
# 7. Record the ISS GPS coordinates and timestamp.
# 8. Convert the timestamp epoch value to a human readable date and time.
# 9. Provide your Geoloaction API consumer key.
# 10. Provide the URL to the Geoloaction address API.
# 11. Store the location received from the Geoloaction API in a variable.
# 12. Complete the code to format the response message.
# 13. Complete the code to post the message to the Webex room.
###############################################################
 
# 1. Import libraries for API requests, JSON formatting, epoch time conversion, and iso3166.

import requests, json, time
from iso3166 import countries

# 2. Complete the if statement to ask the user for the Webex access token.
choice = input("Do you wish to use the hard-coded Webex token? (y/n) ")
if choice.lower() == "n":
    user_token = input("Please enter your Webex access token: ")
    accessToken = f"Bearer {user_token}"
else:
    accessToken = "Bearer Y2MxMzU5MTAtYmVlMS00MmIyLWE0ZTItNDE1ZTExYTlmOGY4Njg4ZTgwM2MtOWIw_PE93_d68b3fe9-4c07-4dad-8882-3b3fd6afb92d"

# 3. Provide the URL to the Webex room API.
                
r = requests.get(
    "https://webexapis.com/v1/rooms",
    headers={"Authorization": accessToken}
)

#######################################################################################
# DO NOT EDIT ANY BLOCKS WITH r.status_code
if not r.status_code == 200:
    raise Exception("Incorrect reply from Webex API. Status code: {}. Text: {}".format(r.status_code, r.text))
#######################################################################################

# 4. Create a loop to print the type and title of each room.
print("\nList of available rooms:")
rooms = r.json()["items"]
for room in rooms:
    print(f"Type: {room['type']}, Title: {room['title']}")

#######################################################################################
# SEARCH FOR WEBEX ROOM TO MONITOR
#  - Searches for user-supplied room name.
#  - If found, print "found" message, else prints error.
#  - Stores values for later use by bot.
# DO NOT EDIT CODE IN THIS BLOCK
#######################################################################################

while True:
    roomNameToSearch = input("Which room should be monitored for the /seconds messages? ")
    roomIdToGetMessages = None
    
    for room in rooms:
        if(room["title"].find(roomNameToSearch) != -1):
            print ("Found rooms with the word " + roomNameToSearch)
            print(room["title"])
            roomIdToGetMessages = room["id"]
            roomTitleToGetMessages = room["title"]
            print("Found room: " + roomTitleToGetMessages)
            break

    if(roomIdToGetMessages == None):
        print("Sorry, I didn't find any room with " + roomNameToSearch + " in it.")
        print("Please try again...")
    else:
        break       
######################################################################################
# WEBEX BOT CODE
#  Starts Webex bot to listen for and respond to /seconds messages.
######################################################################################

while True:
    time.sleep(1)
    GetParameters = {
        "roomId": roomIdToGetMessages,
        "max": 1
    }
    # 5. Provide the URL to the Webex messages API.    
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=GetParameters,
        headers={"Authorization": accessToken}
    )
    if not r.status_code == 200:
        raise Exception(f"Incorrect reply: {r.status_code} {r.text}")
    
    # Fix message parsing - get the actual message text from JSON response
    json_response = r.json()
    if len(json_response["items"]) > 0:
        message = json_response["items"][0]["text"]
        if message.find("/") == 0:
            if (message[1:].isdigit()):
                seconds = int(message[1:])
        else:
            seconds = 1
        if seconds > 5:
            seconds = 5    
    else:
        seconds = 1
            
    time.sleep(seconds)
    
    # 6. Provide the URL to the ISS Current Location API.         
    r = requests.get("http://api.open-notify.org/iss-now.json")
    if r.status_code != 200: 
        raise Exception("Error fetching ISS data.")     
    json_data = r.json()
    
    # 7. Record the ISS GPS coordinates and timestamp.
    lat = json_data["iss_position"]["latitude"]
    lng = json_data["iss_position"]["longitude"]
    timestamp = json_data["timestamp"]
        
    # 8. Convert the timestamp epoch value to a human readable date and time.
    timeString = time.ctime(timestamp)      
   
    # 9. Provide your Geolocation API consumer key.
    mapsAPIGetParameters = { 
        "lat": lat,
        "lon": lng,
        "appid": "23b3179ed699a6446e1c10664a3ef5da"
    }
    
    # 10. Provide the URL to the Reverse GeoCode API.
    # Fix the OpenWeatherMap API URL - remove the placeholder variables
    r = requests.get("https://api.openweathermap.org/data/2.5/weather", 
                     params=mapsAPIGetParameters
                    )

    # Verify if the returned JSON data from the API service are OK
    if r.status_code != 200:
        print("Invalid Message from OpenWeatherMap API")
        # Set default values when API fails
        CountryResult = "XZ"
        CityResult = "Unknown location"
        StateResult = ""
    else:
        json_data_weather = r.json()
        
        # 11. Store the location received from the API in required variables
        CountryResult = json_data_weather.get("sys", {}).get("country", "XZ")
        if CountryResult:
            CountryResult = CountryResult.upper()
        else:
            CountryResult = "XZ"
        CityResult = json_data_weather.get("name", "Unknown location")
        StateResult = ""  # OpenWeatherMap doesn't provide state information

    # Find the country name using ISO3166 country code
    if not CountryResult == "XZ":
        try:
            CountryResult = countries.get(CountryResult).name
        except:
            CountryResult = "Unknown Country"

    # 12. Complete the code to format the response message.
    if CountryResult == "XZ":
        responseMessage = f"On {timeString}, the ISS was flying over a body of water at latitude {lat}° and longitude {lng}°."
    else:
        responseMessage = f"On {timeString}, the ISS was flying over {CityResult}, {CountryResult}. ({lat}°, {lng}°)"
    
    print("Sending to Webex:", responseMessage)

    # 13. Complete the code to post the message to the Webex room.         
    HTTPHeaders = {
        "Authorization": accessToken,
        "Content-Type": "application/json"
    }

    PostData = {
        "roomId": roomIdToGetMessages,
        "text": responseMessage
    }

    r = requests.post("https://webexapis.com/v1/messages",
                      data=json.dumps(PostData),
                      headers=HTTPHeaders)

    if r.status_code != 200:
        print("Error posting message:", r.text)
