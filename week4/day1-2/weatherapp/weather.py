import pyowm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pytz

owm = pyowm.OWM('7cc1a8a4a406c973956d30af1f84747a')
mgr = owm.weather_manager()


def get_weather_info(location):
    observation = mgr.weather_at_place(location)
    weather = observation.weather
    temperature = weather.temperature('celsius')['temp']
    wind = weather.wind()
    sunrise = weather.sunrise_time('iso')
    sunset = weather.sunset_time('iso')

    print(f"\n--- Current Weather for {location} ---")
    print(f"Temperature : {temperature}°C")
    print(f"Wind        : {wind['speed']} m/s, direction {wind['deg']}°")
    print(f"Sunrise     : {sunrise}")
    print(f"Sunset      : {sunset}")


def get_city_id(location):
    observation = mgr.weather_at_place(location)
    return observation.location.id


def get_forecast_info(location):
    city_id = get_city_id(location)
    forecast = mgr.forecast_at_id(city_id, '3h')
    snapshots = forecast.forecast.weathers

    print(f"\n--- 5-Day Forecast for {location} (every 3h) ---")
    for weather in snapshots[:16]:
        time = weather.reference_time('iso')
        temperature = weather.temperature('celsius')['temp']
        humidity = weather.humidity
        wind_speed = weather.wind().get('speed', 0)
        print(f"{time}  |  {temperature}°C  |  Humidity: {humidity}%  |  Wind: {wind_speed} m/s")
    print(f"Showing {min(16, len(snapshots))} of {len(snapshots)} snapshots.")


def get_air_pollution(location):
    observation = mgr.weather_at_place(location)
    lat = observation.location.lat
    lon = observation.location.lon

    air_mgr = owm.airpollution_manager()
    air = air_mgr.air_quality_at_coords(lat, lon)
    aqi = air.aqi
    aqi_labels = {1: 'Good', 2: 'Fair', 3: 'Moderate', 4: 'Poor', 5: 'Very Poor'}

    print(f"\n--- Air Pollution for {location} ---")
    print(f"AQI: {aqi} ({aqi_labels.get(aqi, 'Unknown')})")


# --- Bonus GUI: 3-day humidity bar chart ---

def init_plot():
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_ylabel('Humidity (%)')
    ax.set_title(f'3-Day Humidity Forecast')
    ax.set_ylim(0, 110)
    return fig, ax


def plot_temperatures(ax, location):
    city_id = get_city_id(location)
    forecast = mgr.forecast_at_id(city_id, '3h')
    snapshots = forecast.forecast.weathers[:24]  # 3 days × 8 per day

    times = [datetime.fromtimestamp(w.reference_time(), tz=pytz.utc) for w in snapshots]
    humidities = [w.humidity for w in snapshots]

    bars = ax.bar(times, humidities, width=0.1, color='steelblue', edgecolor='white')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b\n%H:%M'))
    plt.xticks(rotation=45)
    return bars, humidities


def write_humidity_on_bar_chart(ax, bars, humidities):
    for bar, humidity in zip(bars, humidities):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f'{humidity}%',
            ha='center', va='bottom', fontsize=8
        )


def show_humidity_chart(location):
    fig, ax = init_plot()
    ax.set_title(f'3-Day Humidity Forecast — {location}')
    bars, humidities = plot_temperatures(ax, location)
    write_humidity_on_bar_chart(ax, bars, humidities)
    plt.tight_layout()
    plt.show()


# --- Main ---
location = input("Enter a city name to get the weather information: ")
get_weather_info(location)
get_forecast_info(location)
get_air_pollution(location)
show_humidity_chart(location)
