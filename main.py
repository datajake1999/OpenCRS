# FORECAST GEN V2 #

import asyncio
import nwshandler
import SpeechHandler as SpeechHandler
import requests as r
import coloredlogs, logging
import json as j

logger = logging.getLogger(__name__)
logger.info("Loaded Logger!")
coloredlogs.install('DEBUG', logger=logger)
settings = j.load(open('settings.json', 'r'))


# TODO: Learn async.. Whoops.
async def main():
    logger.info('Starting Forecast Gen V2..')
    output = ""
    outfile = open('output.txt', "w+")

    # TODO: Add check for latest version from GitHub    -- can probably start on this soon
    # TODO: Use async to run getActiveAlerts every now and then and check for new alerts
    for z in settings['Zones']:
        logger.debug(f'OBTAIN ZONE FORECAST FOR ZONE {z}')
        output += nwshandler.forecast(z=z)
        output += str(nwshandler.getActiveAlerts(z=z))

    outfile.write(output)
    # SpeechHandler.balcon(volume=25, rate=250, text='-f ..\\output.txt')
    # SpeechHandler.dectalk()


if __name__ == '__main__':
    noaa = r.get('https://api.weather.gov')

    if noaa.ok:
        logger.info("NWS Api is up!")
        asyncio.run(main())
    else:
        logger.critical("Couldn't get a 200 from NWS! Check to see if you're connected to the internet.")