import pyowm
owm = pyowm.OWM('7cc1a8a4a406c973956d30af1f84747a')
mgr = owm.weather_manager()
def get_weather_info(location):
    observation = mgr.weather_at_place(location)
    weather = observation.weather
    temperature = weather.temperature('celsius')['temp']
    wind = weather.wind()
    sunrise = weather.sunrise_time('iso')
    sunset = weather.sunset_time('iso')
    
    print(f"Weather information for {location}:")
    print(f"Temperature: {temperature}°C")
    print(f"Wind Speed: {wind['speed']} m/s, Wind Direction: {wind['deg']}°")
    print(f"Sunrise: {sunrise}")
    print(f"Sunset: {sunset}")
'''Use input() to ask for a city name
Look up the city ID using the registry:
python

   reg = owm.city_id_registry()
   locations = reg.locations_for('Paris', country='FR')
   city_id = locations[0].id
   
Use mgr.weather_at_id(city_id) instead of weather_at_place()'''
location = input("Enter a city name to get the weather information: ")
get_weather_info(location)
