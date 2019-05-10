import re

def format_name(toto):
  titi = re.sub(r"corpus1\/(.*\/.*).txt.*", r"\1", toto)
  return titi
