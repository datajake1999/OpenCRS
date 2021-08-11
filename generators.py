import apihandlers.nwshandler as nwshandler
import logging
import coloredlogs
import json as j
import time

settings = j.load(open('settings.json', 'r'))

logger = logging.getLogger(__name__)
coloredlogs.install(settings['loglevel'], logger=logger) 


def genNWS():
    """Generator for the NOAA/NWS web API"""

    outfile = open('output.txt', "w+")
    txt = ""
    
    for z in settings['OpenCRSsettings']['Zones']:
        logger.info(f'Getting forecast data from zone {z}')
        txt += nwshandler.forecast(z=z)
        txt += nwshandler.getActiveAlerts(z=z)

    txt += (f"Here are the current observations, as of {time.strftime('%I:%M %p %Z')}.\n")

    for s in settings['OpenCRSsettings']['ObservationZones']:
        logger.info(f"Getting data from zone {s}")
        txt += nwshandler.getObservation(s=s)

    # Write then close the output.txt file

    if (txt != None):
        # Someone should make an issue if this doesn't work
        # because it was very in-and-out with working when I orginally
        # implemented this, but now it seems to work 100% of the time,
        # so i dont know whats going on there.
        outfile.write(txt)
        logger.info("Wrote to output.txt successfully!")
        outfile.close()
    else:
        logger.error("The generator failed to provide a text output to write to a file.")
    



def genIBM():
    """Generator for The Weather Company/IBM web API"""
    print("TODO")
