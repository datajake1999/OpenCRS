# FORECAST GEN V2 #

import asyncio
import nwshandler
import SpeechHandler
import time
import requests as r
import coloredlogs, logging
import json as j


settings = j.load(open('settings.json', 'r'))
logger = logging.getLogger(__name__)
coloredlogs.install(settings['loglevel'], logger=logger)    # I'd recommend keeping this at DEBUG


async def main():
    logger.info('Starting OpenCRS..')
    output = ""
    outfile = open('output.txt', "w+")

    # TODO: Use async to run getActiveAlerts every now and then and check for new alerts
    for z in settings['OpenCRSsettings']['Zones']:
        logger.info(f'Getting forecast data from zone {z}')
        output += nwshandler.forecast(z=z)
        output += nwshandler.getActiveAlerts(z=z)

    output += (f"Here are the current observations, as of {time.strftime('%I:%M %p %Z')}.\n")

    for s in settings['OpenCRSsettings']['ObservationZones']:
        logger.info(f"Getting data from zone {s}")
        output += nwshandler.getObservation(s=s)

    

    outfile.write(output)
    outfile.close()
    logger.info("Wrote output.txt successfully!")

    # TTS
    TTSoptions = settings["TTS"]
    if TTSoptions["enabled"]:
        logger.warning("Note that TTS implementation is very janky! It relies on DECTalk or Balabolka, as well as your own installed TTS voices.")
        logger.warning("Check README for instructions on using Balcon/DECTalk with Forecast-Gen!")

        TTSengine = TTSoptions['engine']
        DTSettings = TTSoptions['dectalk']
        BALSettings = TTSoptions['balcon']

        if TTSengine == "dectalk":
            SpeechHandler.dectalk(r=DTSettings['rate'], v=DTSettings['voice'])
        elif TTSengine == "balcon":
            SpeechHandler.balcon(voice=f"{BALSettings['voice']}", volume=BALSettings['volume'], rate=BALSettings['speed'], filelocation="../output.txt")




if __name__ == '__main__':
    noaa = r.get('https://api.weather.gov')

    #Github release check
    ver = settings['version']
    try:
        github = r.get('https://api.github.com/repos/Zeexel/OpenCRS/releases/latest').json()
        if github['name'] != ver:
            logger.warning("You are not using the latest version of forecastgen! Latest version: {github['name']}")
        else:
            logger.info("Using the latest build of OpenCRS!")
    except Exception:
        logger.error("Could not obtain the latest version of OpenCRS! (Probably cause there isn't a release build yet..)")

    # Check NOAA status
    if noaa.ok:
        logger.info("NWS Api is up!")
        asyncio.get_event_loop().run_until_complete(main())
    else:
        logger.critical("Couldn't get a 200 from NWS! Check to see if you're connected to the internet.")
