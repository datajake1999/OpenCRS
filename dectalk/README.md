# OpenCRS DECtalk settings & usage guide.
 
As mentioned in the README for OpenCRS, here's that more comprehensive DECTalk guide.

The DECTalk version included in OpenCRS is ``BETA 5.0``

## Voices

The voices for DECtalk are as follows:

Paul (Default) - ``[:np]``
Harry/igor - ``[:nh]``
Frank - ``[:nf]``
Dennis - ``[:nd]``
Betty - ``[:nb]``
Ursula - ``[:nu]``
Wendy - ``[:nw]``
Rita - ``[:nr]``
Kit - ``[:nk]``
Variable Val - ``[:nv]``

Any of these voices can be used by changing the ``"voice"`` variable in settings.json with any of their two-letter identifiers. By default, OpenCRS uses the Paul voice.

## Phonemes 

We won't go fully into phonemes, but their main purpose in DECTalk is so that the voices can sing. You can enable them with ``say.exe`` by using ``[:phoneme on]``, or if you're using it with OpenCRS, setting ``"phonemes"`` to ``true``.

## Speech Variables

Variables for speech are very few, surprisingly, and only a few are implemented into OpenCRS.

### Implemented Speech Variables
``[:rate]`` - The rate at which DECTalk speaks. The max is 600, and the minimum is 75.

### Unimplemented Speech Variables
``[:volume up DD]`` - Increases the volume by DD (1-99) units.
``[:volume down DD]`` - Decreases the volume by DD (1-99) units.
``[:pron alternate]`` - Uses the alternate pronunciation for the word that it's next to.
``[:pron primary]`` - Uses the primary pronunciation for the word that it's next to.
``[:comma DD]`` - Length for pauses between commas.
``[:period DD]`` - Length for pauses between periods.

More of these speech variables will be eventually implemented into OpenCRS's settings for DECTalk.

