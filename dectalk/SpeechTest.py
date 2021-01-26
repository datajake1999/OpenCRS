from os import path
import subprocess
import coloredlogs, logging
import json
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)
promptFile = json.load(open('prompts.json', 'r'))

logger.info("This script will run through some prompts to demonstrate DECTalk working.")
logger.info("If you're using Linux or Mac, you may need to install WINE for DECTalk to work properly.")


def dectalkSelfTest():
    prompts = promptFile['prompts']

    logger.debug("Begin Selftest.")
    for p in prompts:
        subprocess.run(f"say.exe [:rate 250] {p}")
        logger.debug("Going to next prompt..")

    logger.debug("Self-test complete!")


# Check if say.exe exists.
if path.exists('say.exe'):
    logger.info("Successfully found say.exe")
    dectalkSelfTest()
else:
    logger.critical("Missing say.exe! Stopping benchmark.")
