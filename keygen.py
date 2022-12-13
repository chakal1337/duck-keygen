import sys
import requests
import argparse
import threading
import time
import urllib.parse
from bs4 import BeautifulSoup
import json

words_collected = []
max_depth = 1
max_threads = 25

parser = argparse.ArgumentParser()
parser.add_argument('keyword')
parser.add_argument("-d", "--depth")
parser.add_argument('-t', '--max-threads')
args = parser.parse_args()

if args.depth:
 max_depth = int(args.depth)

if args.max_threads:
 max_threads = int(args.max_threads)

keywords = [args.keyword]
try:
 with open(args.keyword, "rb") as file:
  keywords = file.read().decode().splitlines()
except:
 pass

tlock = threading.Lock()

def gkey(queryword, depth=1):
 try:
  global words_collected
  s = requests.Session()
  querywordq = urllib.parse.quote_plus(queryword)
  url = f"https://duckduckgo.com/ac/?q={querywordq}+&kl=wt-wt"
  r = s.get(url=url)
  words = json.loads(r.text)
  for word in words:
   word = word["phrase"]
   with tlock:
    if not word in words_collected:
     words_collected.append(word)
     print(word)
    else:
     continue
   if depth < max_depth:
    while threading.active_count() > max_threads: time.sleep(0.1)
    t=threading.Thread(target=gkey, args=(word, depth+1))
    t.start()
 except Exception as error:
  if debug == 1: print(error)

def main():
 for keyword in keywords:
  while threading.active_count() > max_threads: time.sleep(0.1)
  gkey(keyword, 1)

if __name__ == "__main__":
 main()
