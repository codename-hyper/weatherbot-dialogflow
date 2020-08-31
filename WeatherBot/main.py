from flask import Flask, request, make_response
import json
import pyowm
from flask_cors import CORS, cross_origin

weather = Flask(__name__)

owmapikey = 'api_key_from_openweather_website'
owm = pyowm.OWM(owmapikey)


def ProcessRequest(req):
    query = req.get('queryResult')
    parameters = query.get('parameters')
    city = parameters.get('city')
    City = str(city)
    manager = owm.weather_manager()
    observation = manager.weather_at_place(City)
    weather = observation.weather


    wind = weather.wind()
    wind_speed = str(wind['speed'])

    humidity = str(weather.humidity)

    celsius = weather.temperature('celsius')
    temp_min = str(celsius['temp_min'])
    temp_max = str(celsius['temp_max'])

    # latlon = weather.get_location()
    # lat = str(latlon.get_lat())
    # lon = str(latlon.get_lon())

    result = "Today's weather in " + City + "is: \n" + "Humidity: " + humidity + "\n Wind speed: " + wind_speed + "\n Min. Temperature: " + temp_min + "\n Max. Temperature: " + temp_max

    return {
        'fulfillmentText': str(result)
    }


@weather.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    req = request.get_json()
    result = ProcessRequest(req)
    result_json = json.dumps(result)
    result_response = make_response(result_json)
    result_response.headers['Content-Type'] = 'application/json'
    return result_response


if __name__ == '__main__':
    weather.run(debug=True)
