"""
Function based on PyDictionary library with added bugfixes as pull requests
in the original library are not merged.
"""

import re

import requests
from bs4 import BeautifulSoup


def _get_soup_object(url, parser="html.parser"):
    return BeautifulSoup(requests.get(url).text, parser)


def get_definition(word, disable_errors=False):
    if len(word.split()) > 1:
        print("Error: A Term must be only a single word")
    else:
        try:
            html = _get_soup_object("http://wordnetweb.princeton.edu/perl/webwn?s={0}".format(
                word))
            types = html.findAll("h3")
            # length = len(types)
            lists = html.findAll("ul")
            out = {}
            for a in types:
                reg = str(lists[types.index(a)])
                meanings = []
                for x in re.findall(r'\(((?:[^()]*|\([^()]*\))*)\)', reg):
                    if 'often followed by' in x:
                        pass
                    elif len(x) > 5 or ' ' in str(x):
                        meanings.append(x)
                name = a.text
                out[name] = meanings
            return out
        except IndexError:
            print(f"No definition found for word \"{word}\"")
        except Exception as e:
            if not disable_errors:
                print(f"Error: The Following Error occurred: {e}")
