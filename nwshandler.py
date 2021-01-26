import json
import requests


def forecast(z="DCZ001", t="land"):
    """"
    Obtains zone forecast for the zone given.
    If no zone is given, it will default to giving the zone forecast for Washington D.C. (DCZ001)
    You can also change the type of forecast, in order to get things like marine and fire forecasts.
    Forecast types:
    land, marine, forecast, public, coastal, offshore, fire, county
    """
    zone_url = f"https://api.weather.gov/zones/forecast/{z}"
    zf_url = f"https://api.weather.gov/zones/{t}/{z}/forecast"
    zfd = requests.get(zf_url).json()
    zd = requests.get(zone_url).json()  # Zone Details
    zf = """"""
    ah = None

    try:
        zf += f"""The zone forecast for {zd['properties']['name']}:\n"""

        if ah != None:
            zf += f"{ah}\n"

        for i in range(0,8):
            zf += f"""{zfd['properties']['periods'][i]['name']}: {zfd['properties']['periods'][i]['detailedForecast']}\n"""

        zf += """---------------------------"""     # Add Separator

        return zf

    except TypeError:
        pass

    except IndexError:
        pass

