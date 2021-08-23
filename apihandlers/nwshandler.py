import requests
import logging
import coloredlogs
from math import floor
import json as j

settings = j.load(open('settings.json',  'r'))
l = logging.getLogger(__name__)
coloredlogs.install(level=settings['loglevel'], logger=l)


def getActiveAlerts(z='DCZ001'):
    """"
    Gets the list of active alerts specified within a specific zone
    If the alert is in the EAS Blockchannel, then the program will attempt to stop current speech in order to
    broadcast the alert efficiently. However, it will not be able to generate SAME Tones.
    """
    active_alerts = requests.get(f'https://api.weather.gov/alerts/active/zone/{z}').json()
    id = ""
    headline = ""
    desc = ""
    severity = ""
    blockchannel = []
    product = ""

    if None in active_alerts['features']:
        l.debug(f'No alerts listed for zone {z}')
        pass
    else:
        for alert in active_alerts['features']:
            id = requests.get(alert['id']).json()   # Get the full alert details from the alert's ID in the API

            headline = id['properties']['parameters']['NWSheadline'][0]
            desc = id['properties']['description']  # Alert details
            severity = id['properties']['severity']
            blockchannel = id['properties']['parameters']['BLOCKCHANNEL']

            product += f"{headline}.\n"
            product += f"{desc}..\n"
            product += "---------------------------\n"  # Add seperator

            l.debug(f"ALERT FOUND\nBLOCKCHANNEL {blockchannel}\nSEVERITY {severity}\n{alert['id']}")

        return product


def forecast(z="DCZ001", t="land"):
    """"
    Obtains zone forecast for the zone given.
    If no zone is given, it will default to giving the zone forecast for Washington D.C. (DCZ001)
    You can also change the type of forecast, in order to get things like marine and fire forecasts.
    Forecast types:
    land, marine, forecast, public, coastal, offshore, fire, county

    UPDATE: I think land, forecast, and public might just give the same output for some reason.
            Marine, fire, and coastal forecasts are pretty cool to look at, though!
    """
    zone_url = f"https://api.weather.gov/zones/forecast/{z}"
    zf_url = f"https://api.weather.gov/zones/{t}/{z}/forecast"
    activeAlerts = requests.get(f'https://api.weather.gov/alerts/active/zone/{z}').json()
    zfd = requests.get(zf_url).json()
    zd = requests.get(zone_url).json()  # Zone Details
    zf = ""
    ah = None

    # Borrowing code from getActiveAlerts here
    for alert in activeAlerts['features']:
        id = requests.get(alert['id']).json()
        nws_headline = id['properties']['parameters']['NWSheadline'][0]     # Nah, it makes sense that it's a table
        ah = nws_headline

    try:
        zf += f"The zone forecast for {zd['properties']['name']}:\n"

        if ah is not None:
            zf += f"{ah}.\n"

        forecastPeriods = list(zfd['properties']['periods'])

        for i in forecastPeriods:
            zf += f"{i['name']}: {i['detailedForecast']}\n"

        zf += "---------------------------\n"   # Add Separator

        return zf

    except TypeError:
        pass

    except IndexError:
        pass


def getObservation(s):
    """
    Obtains the latest data from the station specified.
    """
    stationData = requests.get(f'https://api.weather.gov/stations/{s}/observations/latest').json()
    stationInfo = requests.get(f'https://api.weather.gov/stations/{s}').json()
    name = stationInfo['properties']['name']
    obs = ""

    # This is gonna require a lot of if statements
    # YandereDev time
    try:
        con = stationData['properties']['textDescription']
        temp = floor(stationData['properties']['temperature']['value'])
        dp = floor(stationData['properties']['dewpoint']['value'])
        rh = floor(stationData['properties']['relativeHumidity']['value'])

        # TODO: Round & floor decimals to prevent trailing decimals when it comes to
        # Temperature + Dewpoint, as well as relative humidity.

        if con != "":
            obs += f"At {name}, it was {con}. "
        else:
            obs += f"At {name}, the conditions were unavailable. "

        if temp != None:
            if settings['OpenCRSsettings']['system'] == 'metric':
                obs += f"Temperature {str(round(temp))} degrees, "
            elif settings['OpenCRSsettings']['system'] == 'imperial':
                temp = (temp * 9 / 5 + 32)  # Convert the temperature from C to F
                obs += f"Temperature {str(round(temp))} degrees, "

        if dp != None:
            if settings['OpenCRSsettings']['system'] == 'metric':
                obs += f"Dewpoint {str(round(dp))}, "
            elif settings['OpenCRSsettings']['system'] == 'imperial':
                dp = (dp * 9 / 5 + 32)
                obs += f"Dewpoint {str(round(dp))}, "

        if rh != None:
            obs += f"relative humidity {rh}%. \n"

    except Exception as e:
        l.error(f"Unable to obtain data for {s}!\n{e}")
        obs += f"At {name}, the observations were unavailable.\n"    
    return obs

def getSynopsis(fo):
    afdProducts = requests.get(f'https://api.weather.gov/products/types/AFD/locations/{fo}').json()
    afd = requests.get(afdProducts['@graph'][0]['@id']).json()  # Grabs the latest AFD product, @id being the URL
    l.debug(f"AFD PRODUCT URL {afdProducts['@graph'][0]['@id']}")

    start = '.SYNOPSIS...'
    end = "&&"  # For some reason this is at the end of each synopsis product
    productText = afd['productText']
    syn = (productText.split(start))[1].split(end)[0]   # Take everything but the synopsis text from the AFD
    
    # TODO: Add SYN product edge case

    return syn
