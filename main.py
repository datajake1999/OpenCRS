# FORECAST GEN V2 #

import nwshandler
import requests as r
import coloredlogs, logging
import json as j

logger = logging.getLogger(__name__)
logger.info("Loaded Logger!")
coloredlogs.install('DEBUG', logger=logger)
settings = j.load(open('settings.json', 'r'))


def main():
    logger.info('Starting ForeCast Gen V2..')

    # TODO: Add check for latest version from GitHub

    for z in settings['Zones']:
        logger.debug(f'OBTAIN ZONE FORECAST FOR ZONE {z}')
        print(nwshandler.forecast(z))


if __name__ == '__main__':
    noaa = r.get('https://api.weather.gov')

    if noaa.ok:
        logger.info("NWS Api is up!")
        main()
    else:
        logger.critical("Couldn't get a 200 from NWS! Check to see if you're connected to the internet.")