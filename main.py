# FORECAST GEN V2 #

import asyncio
import nwshandler
import SpeechHandler
import requests as r
import coloredlogs, logging
import json as j

settings = j.load(open('settings.json', 'r'))
logger = logging.getLogger(__name__)
coloredlogs.install(settings['loglevel'], logger=logger)    # I'd recommend keeping this at DEBUG


async def main():
    logger.info('Starting Forecast Gen V2..')
    output = ""
    outfile = open('output.txt', "w+")

    # TODO: Use async to run getActiveAlerts every now and then and check for new alerts
    for z in settings['ForecastGenSettings']['Zones']:
        logger.debug(f'OBTAIN ZONE FORECAST FOR ZONE {z}')
        output += nwshandler.forecast(z=z)
        output += str(nwshandler.getActiveAlerts(z=z))

    outfile.write(output)
    outfile.close()
    logger.info("Wrote text file in /forecastgen-v2/output.txt")

    # TTS
    TTSoptions = settings["TTS"]
    if TTSoptions["enabled"]:
        logger.warning("Text-to-speech is not yet implemented.")



if __name__ == '__main__':
    noaa = r.get('https://api.weather.gov')
    # github = r.get('https://api.github.com/repos/Zeexel/forecastgen-v2/releases/latest').json()

    # Code below should be commented until the first release of forecastgen-v2
    # Github release check
    """
    ver = settings['version']
    if github['name'] != ver:
        logger.warning("You are not using the latest version of forecastgen! Latest version: {github['name']}")
    else:
        logger.info("Using the latest build of forecastgen!")
        """

    # Check NOAA status
    if noaa.ok:
        logger.info("NWS Api is up!")
        asyncio.run(main())
    else:
        logger.critical("Couldn't get a 200 from NWS! Check to see if you're connected to the internet.")
