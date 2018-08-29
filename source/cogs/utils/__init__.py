"""
Utils package for Robo-CLaymore
intended for internal use
could probably be used in other bots with a bit of work
"""

from .zalgo import zalgo
from .checks import is_admin, can_kick, can_ban, manage_messages, manage_nicknames
from .retro import make_retro
from .sankaku import skkcomplex_request
from .facial_detection import replace_eyes
from .van import overlay_van
from .networking import (
	tinyurl, hastebin, hastebin_error,
	exists, url_request, json_request,
	request_async, get_bytes, get_image
)
from .shortcuts import (
	try_file, quick_embed, embedable,
	emoji, only_mentions_bot
)
from .memegen import make_meme
from .converters import bytes_to_cv2, image_to_bytes, bytes_to_image
from .expanding_brain import make_expanding_brain
from .images import (
	do_choice, do_button, do_note,
	do_kick, do_words, do_prison,
	do_retard, do_shout, do_tweet,
	do_villan_image, do_rtx, do_wack
)
