#
# Import modules
#
import RPi.GPIO as GPIO
import requests
import json
import urllib.parse
import time
import datetime

#
# Weather constants
#
API_KEY = "ce8eaf0e980fc797cc8861d4e83f2514"
HOME_ADDRESS = '43, Cranbourne Drive, Otterbourne, Winchester, Hampshire, South East England, England, SO21 2ES, United Kingdom'
URL_LATLONG = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(HOME_ADDRESS) + '?format=json'
URL_WEATHER = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric"
COLD = 18
WARM = 19
HOT = 20
LED_RED = 5
LED_GREEN = 6
LED_YELLOW = 13
LOOP = 100
#
# Get the Longitude and Latitude for the long form address
#
latlong_response = requests.get(URL_LATLONG).json()
latitude = latlong_response[0]["lat"]
longitude = latlong_response[0]["lon"]
#
# Get the temperature using the Latitude and Longitude from open weather
#
URL_WEATHER = URL_WEATHER % (latitude, longitude, API_KEY)
weather_response = requests.get(URL_WEATHER).json()
#
# Get the temperature and see if cold, warm or hot twt
#
def temp():
    current_temperature = weather_response["current"]["temp"]
    print("Temperature in Winchester =", current_temperature, "Celsius")
    if current_temperature <= COLD:
        temp_range = "Cold = Blue LED"
        led_color = LED_YELLOW
    elif current_temperature >= HOT:
        temp_range = "Hot Red LED"
        led_color = LED_RED
    else:
        temp_range = "warm - yellow LED"
        led_color = LED_GREEN
    print("temperature = ", temp_range)
    return led_color
#
# Initialise the GPIO bus
#
def led_initialise():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LED_RED, GPIO.OUT)
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.setup(LED_YELLOW, GPIO.OUT)
    return
#
# switch on the LED color passed to the function
#
def led_on(led_color):
    GPIO.output(led_color, GPIO.HIGH)
    time.sleep(5)
    return
#
#
#
class Test:
    def __str__(self):
        return("I am an amazing object")

    print("Class caller")
#
# Loop for 100 iterations. Reset GPIO and display appropriate LED
#
x = 0
y = Test()
while x < LOOP:
    print(y)
    now = datetime.datetime.now()
    print("iteration = ", x, "time = ", now.strftime("%d-%m-%Y %H:%M:%S"))
    led_initialise()
    led_on(temp())
    time.sleep(360)
    x += 1
