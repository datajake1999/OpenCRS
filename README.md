# OpenCRS
The successor to the [original Forecast-Gen](https://github.com/Zeexel/forecast-gen), which is now heavily outdated as the U.S. National Weather Service has since done a ton of reworking to their API.

The goal of OpenCRS is to update the stability, performance of the original project, as well as create something akin to the National Weather Service's [Console Replacement System (CRS)](https://www.weather.gov/nwr/automatevoice) whilst still being simple to set up, install, and run constantly on something such as a server running an internet radio stream.

In the future, there is likely to be more support for seperate APIs so that people outside of the United States can use it. This will likely include support for languages such as Spanish, French, and Japanese, as well as many others. As of Feburary 2021, the program currently only supports users in the United States and its territories, with English being the only current language.

The program is currently in early development, but releases can be found [here.](https://github.com/Zeexel/forecastgen-v2/releases)

# TTS Support
OpenCRS better supports Text-to-speech use with the output of the python scripts. By default, DECTalk is included with the software, and is easily used cross-platform using WINE.

As opposed to the previous iteration of ["Basic TTS support"](https://github.com/Zeexel/forecast-gen/commit/661d80aef6c1d966ac3b0229d939db314f8034ee) (which was awful in the last iteration), V2 introduces a basic JSON file that configures not only the zones, stations, as well as the priority zones for emergency alerts & warnings, configures text-to-speech. 

In order to enable TTS, simple go into ``settings.json`` and scroll down to ``"TTS"``. You can then enable TTS by setting the ``"enable"`` variable to true.

### DECTalk
[DECTalk](https://en.wikipedia.org/wiki/DECtalk) comes pre-included with the software, and is the default option for the ``"engine"`` variable. 

This should be the base DECTalk settings in an unedited settings file:

```json
    "dectalk": {
      "voice": "np",
      "rate": 250,
      "phonemes": false
    },
```

I will soon make a more comprehensive guide once full support for DECTalk is added, but here are the basics:

* ``"voice"`` is the voice that the engine will use when reading the ``output.txt`` file.
* ``"rate"`` is the speed at which the voice reads the text given to it.
* ``"phonemes"`` is currently unused in the source code, but will enable the engine to use phonemes, which can allow it to sing.

### Balcon
Balcon is the CLI variant for [Balabolka](http://www.cross-plus-a.com/balabolka.htm), a freeware TTS reader. It's not included in the source code due to the licensing, but it is supported out of the box once installed, and the ``balcon`` folder is put into the same directory as OpenCRS

Once installed, it's recommended to use the ``pronunciationfix.dic`` file in the ``extras`` directory, as some things can be read incorrectly by a lot of TTS voices.

If you need voices, I would personally recommend trying out the voices from the Microsoft Text to Speech Pack, which can be downloaded [here.](https://archive.org/details/Sam_mike_and_mary) This pack includes Microsoft Sam, Mike, and Mary, and will work perfectly fine with Balcon, even on non-windows environments that have to use WINE.

This should be the base Balcon settings in an unedited settings file:
```json
    "balcon": {
      "download_here": "http://www.cross-plus-a.com/bconsole.htm",
      "voice": "ATT Mike16",
      "dictionary-path": "pronunciationfix.dic",
      "volume": 25,
      "speed": 100
    }
```

Unlike DECTalk, balcon is quite simple, so I don't need to make a more in-depth guide for it, so here's what everything does:

* ``"voice"`` is the voice that Balcon will use when reading the output.txt file. 
  It's very important that the voice given to Balcon is the same voice that your computer uses when trying to use it itself. If you're not sure what the full name of your voice is, you can do ``.\balcon.exe -l`` or ``wine balcon.exe -l`` to get a list of the voices installed on your system.

* ``"dictionary-path"`` is the directory to a custom dictionary file.
* ``"volume"`` is how loud the audio is (I'd recommend keeping this at 25, personally)
* ``"speed"`` is just the speed at which the voice reads everything. Some TTS voices don't support this, however.
