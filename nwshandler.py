import requests
import logging
import coloredlogs

l = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=l)

"""
So, just a quick note, it seems like NOAA and the NWS have actually improved their API quite a bit since fgen-v1
was first released. Now, we can prioritize alerts based on their severity, BLOCKCHANNELS, etc.

They also provide a lot of the EAS stuff used for their own broadcasting, so it's really easy to just straight up
pass a lot of that onto a open sourced EAS/SAME Encoder like OpenENDEC or similar.

Honestly, it seems like the only issue now is a thing where they can't keep their entire fucking API up for more than a
literal fucking day.

Thanks NOAA.

Zeexel @ 0:13 MST - Jan. 27 2021
"""


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
            l.debug(f"ALERT FOUND - {alert['id']}")
            id = requests.get(alert['id']).json()   # Get the full alert details from the alert's ID in the API

            headline = id['properties']['parameters']['NWSheadline'][0]
            desc = id['properties']['description']  # Alert details
            severity = id['properties']['severity']
            blockchannel = id['properties']['parameters']['BLOCKCHANNEL']

            product += f"{headline}\n"
            product += f"{desc}\n"
            product += "---------------------------\n"  # Add seperator

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
        nws_headline = id['properties']['parameters']['NWSheadline'][0]     # Why is this a table?
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
    stationData = requests.get(s).json()