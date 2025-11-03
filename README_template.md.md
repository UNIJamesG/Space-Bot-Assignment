# 🚀 Space Bot API Investigation Sheet

**Total Marks: 30**  
**Part 1: Collect Required API Documentation**

This investigation sheet helps you gather key technical information from the three APIs required for the Space Bot project: **Webex Messaging API**, **ISS Current Location API**, and a **Geocoding API** (LocationIQ or Mapbox or other), plus the Python time module.

---

## ✅ Section 1: Webex Messaging API (7 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `https://webexapis.com/v1` |
| Authentication Method | `Bearer Token` |
| Endpoint to list rooms | `/rooms` |
| Endpoint to get messages | `/messages` |
| Endpoint to send message | `/messages` |
| Required headers | `{"Authorization": "Bearer {token}", "Content-Type": "application/json"}` |
| Sample full GET or POST request | `GET https://webexapis.com/v1/rooms
POST https://webexapis.com/v1/messages
Headers: {"Authorization": "Bearer Y2MxMzU5MTAtYmVlMS00MmIyLWE0ZTItNDE1ZTExYTlmOGY4Njg4ZTgwM2MtOWIw_PE93_d68b3fe9-4c07-4dad-8882-3b3fd6afb92d", "Content-Type": "application/json"}
Body: {"roomId": "room_id", "text": "Hello"}` |

---

## 🛰️ Section 2: ISS Current Location API (3 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `http://api.open-notify.org` |
| Endpoint for current ISS location | `/iss-now.json` |
| Sample response format (example JSON) |  
```
{
  "message": "success",
  "timestamp": 1645826400,
  "iss_position": {
    "latitude": "51.6587",
    "longitude": "-0.2859"
  }
}
```
|

---

## 🗺️ Section 3: Geocoding API (LocationIQ or Mapbox or other) (6 marks)

| Criteria | Details |
|---------|---------|
| Provider used (circle one) | **OpenWeatherMapAPI** |
| API Base URL | `https://api.openweathermap.org/data/2.5` |
| Endpoint for reverse geocoding | `/weather` |
| Authentication method | `API Key (appid parameter)` |
| Required query parameters | `lat, lon, appid` |
| Sample request with latitude/longitude | `https://api.openweathermap.org/data/2.5/weather?lat=51.5074&lon=-0.1278&appid=23b3179ed699a6446e1c10664a3ef5da` |
| Sample JSON response (formatted example) |  
```
{
  "coord": {"lon": -0.13, "lat": 51.51},
  "weather": [{"id": 300, "main": "Drizzle", "description": "light intensity drizzle", "icon": "09d"}],
  "base": "stations",
  "main": {"temp": 280.32, "pressure": 1012, "humidity": 81, "temp_min": 279.15, "temp_max": 281.15},
  "visibility": 10000,
  "wind": {"speed": 4.1, "deg": 80},
  "clouds": {"all": 90},
  "dt": 1485789600,
  "sys": {"type": 1, "id": 5091, "message": 0.0103, "country": "GB", "sunrise": 1485762037, "sunset": 1485794875},
  "id": 2643743,
  "name": "London",
  "cod": 200
}
```
|

---

## ⏰ Section 4: Epoch to Human Time Conversion (Python time module) (2 marks)

| Criteria | Details |
|---------|---------|
| Library used | `time` |
| Function used to convert epoch | `time.ctime()` |
| Sample code to convert timestamp |  
```
import time
timestamp = 1645826400
timeString = time.ctime(timestamp)
print(timeString)
```
|
| Output (human-readable time) | `Mon Feb 28 11:00:00 2022` |

---

## 🧩 Section 5: Web Architecture & MVC Design Pattern (12 marks)

### 🌐 Web Architecture – Client-Server Model
Client (User) → HTTP Request → Server (API) → HTTP Response → Client (User)
    ↓                                      ↓
Webex App                           Webex API Server
    ↓                                      ↓
Python Script                      ISS Location API
    ↓                                      ↓
                   Geocoding API

### 🔁 RESTful API Usage

- HTTTP Method (Get,POST)
- Returns data in the JSON format
- Communicates between the client and the server

### 🧠 MVC Pattern in Space Bot

| Component   | Description |
|------------|-------------|
| **Model**  |ISS Location data, Geocoding Data and information about the room  |
| **View**   |Formatted messages sent to Webex rooms  |
| **Controller** | Coordinates between API's, Processes Commands and Manages Flow of Outputs |


#### Example:
- Model: json_data["iss_position"], json_data_weather["name"]
- View: responseMessage
- Controller: /seconds

---

### 📝 Notes

- Use official documentation for accuracy (e.g. developer.webex.com, locationiq.com or Mapbox, open-notify.org or other ISS API).
- Be prepared to explain your findings to your instructor or demo how you retrieved them using tools like Postman, Curl, or Python scripts.

---

### ✅ Total: /30
