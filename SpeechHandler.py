import coloredlogs
import logging
from os import path
from os import system
from sys import platform

l = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=l)

"""
General speech handling for DECTalk and possibly other speech options in the future.
If you're using a non-windows OS, you may need to use WINE.
https://www.winehq.org/
"""


def dectalk(r=230, v='np', text='No input was given.'):
    """
    A general speech handler for say.exe in the /dectalk/ directory
    r = The rate at which the program speaks (default 230)
    v = Voice that the applications should use
    """

    if path.exists('dectalk/say.exe'):
        l.debug("Say.exe exists in the current directory")
        l.debug(f"System platform is {platform}")
        # Run say.exe through WINE if the platform isn't on Windows.
        if platform != 'win32':
            system(f"cd dectalk && wine say.exe [:rate {r}] [:{v}] {input}")
        else: system(f"cd dectalk && say.exe [:rate {r}] [:{v}] {input}")
    else:
        l.critical("say.exe does not exist in the dectalk directory!")


def balcon(voice, volume, rate, filelocation):
    if path.exists('balcon/balcon.exe'):
        l.debug("Balcon.exe exists in the current directory.")
        l.debug(f"System platform is {platform}")

        # TODO: Fix bug where balcon can't read .txt files
        if platform != 'win32':
            system(f'cd balcon && wine balcon.exe -n "{voice}" -d pronunciationfix.dic -s {rate} -v {volume} -f {filelocation}')
        else:
            system(f'cd balcon && balcon.exe -n "{voice}" -d pronunciationfix.dic -s {rate} -v {volume} -f {filelocation}')
