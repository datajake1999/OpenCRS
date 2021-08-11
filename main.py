import asyncio
import SpeechHandler
import generators
import requests as r
import coloredlogs, logging
import json as j

settings = j.load(open('settings.json', 'r'))
logger = logging.getLogger(__name__)
coloredlogs.install(settings['loglevel'], logger=logger)    # I'd recommend keeping this at DEBUG


async def main():
    logger.info('Starting OpenCRS..')

    # Use different generators based on the current
    if (settings['OpenCRSsettings']['apihandler'] == "noaa"):
        logger.debug("Generating output.txt using NOAA's API..")
        generators.genNWS()
    elif (settings['OpenCRSsettings']['apihandler'] == "ibm"):
        logger.debug("Generating output.txt using IBM's API..")
        generators.genIBM()


    # TODO: Make radio loop

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
    ver = '0.2-GIT'     # OpenCRS version
    noaa = r.get('https://api.weather.gov')

    #Github release check
    try:
        github = r.get('https://api.github.com/repos/Zeexel/OpenCRS/releases/latest').json()
        if github['name'] != ver:
            logger.warning(f"Version {github['name']} is currently out! You're using version {ver}.")
        else:
            logger.info("Using the latest build of OpenCRS!")
    except Exception as e:
        logger.error("Could not obtain the latest version of OpenCRS!")
        logger.debug(f"FAILED TO OBTAIN OPENCRS VERSION\n{e}")

    # Check NOAA status
    if noaa.ok:
        logger.info("NWS Api is up!")
        asyncio.get_event_loop().run_until_complete(main())
    else:
        logger.critical("Couldn't get a 200 from NWS! Check to see if you're connected to the internet.")
