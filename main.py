# FORECAST GEN V2 #

import asyncio
import nwshandler
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

    # TODO: Add check for latest version from GitHub    -- can probably start on this soon
    # TODO: Use async to run getActiveAlerts every now and then and check for new alerts
    # print(nwshandler.getActiveAlerts('CAZ071'))
    for z in settings['Zones']:
        logger.debug(f'OBTAIN ZONE FORECAST FOR ZONE {z}')
        print(nwshandler.forecast(z))


if __name__ == '__main__':
    noaa = r.get('https://api.weather.gov')

    if noaa.ok:
        logger.info("NWS Api is up!")
        asyncio.run(main())
    else:
        logger.critical("Couldn't get a 200 from NWS! Check to see if you're connected to the internet.")