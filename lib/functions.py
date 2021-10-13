import json
import re
import os
import os.path as op

PATH_BLACKLIST = op.join(op.dirname(__file__), './blacklist.json')
blacklist_kw = {}
with open(PATH_BLACKLIST, 'r') as f:
    blacklist_kw = json.loads(f.read())

regex_blackist_kw = re.compile(
    f"(^|(?<=\\s))({'|'.join(blacklist_kw)})(\\s+|$)",
    re.I
)


def filter_chat_content(msg):
    msg = re.sub(regex_blackist_kw, r'\1 *** \3', msg, 0)

    # censor phonenum
    msg = re.sub(r'\b([0-9]{4,7})', '***', msg, 0)

    # censor link href
    msg = re.sub(
        r"\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))",
        '***', msg, 0
    )

    # remove multi ***
    msg = re.sub(r'(\s*\*{3}\s*)+', ' *** ', msg, 0)

    return msg
