#!/usr/bin/env python3
import requests
import argparse
import json
import time
import datetime
import re
import sys
import csv
from collections import namedtuple,Counter

def dateformat(utc):
    return str(datetime.datetime.utcfromtimestamp(utc).date())

def keywordclean(str):
    return str.replace('r+','').replace('+','').replace('%','+')

def process_comment(c,keywords):
    matches = []
    for keyword in keywords:
        if re.search('[^%r]\+',keyword) is not None:
            if re.search('r\+',keyword) is not None:
                if re.search('[ /\n,\.]' + keywordclean(keyword) + '[ /\n,\.]',c.subreddit.lower()) is not None:
                    matches.append(keyword)
            else:
                if re.search('[ /\n,\.]' + keywordclean(keyword) + '[ /\n,\.]',c.body.lower()) is not None:
                    matches.append(keyword)
        else:
            if re.search('r+',keyword) is not None:
                if re.search(keywordclean(keyword),c.subreddit.lower()) is not None:
                    matches.append(keyword)
            else:
                if re.search(keywordclean(keyword),c.body.lower()) is not None:
                    matches.append(keyword)
    return matches

def tally_matches(matches,keywords):
    sort = []
    for day in matches:
        tmp = {}
        for kw in keywords:
            try:
                tmp[kw] = Counter(matches[day])[kw]
            except:
                tmp[kw] = 0
        sort.append({**{"Time":day}, **tmp})
    return sort

def mean(numbers):
    return float(sum(numbers))/max(len(numbers),1.)

def parse_date(date):
    return datetime.datetime.strptime(date,"%Y-%m-%d")

def pad_days(sort):
    lst = []
    empty = {}
    for kw in sort[0]:
        if kw is "Time":
            continue
        empty[kw] = 0
    lasttime = parse_date(sort[0]["Time"])-datetime.timedelta(days=1)
    lst.append(sort[0])
    for i in range(1,len(sort)):
        time = parse_date(sort[i]["Time"])
        lst.append(sort[i])
        if((time-lasttime).days > 1):
            #print(i,(time-lasttime).days)
            for day in range(0,(time-lasttime).days):
                lst.append({**{"Time":(lasttime+datetime.timedelta(days=day)).date()},**empty})
        lasttime = time
    return lst

def add_averages(sort,period):
    for day in range(int(period/2),len(sort)-(int(period/2))):
        day2 = {**sort[day]}
        for kw in sort[day]:
            if kw is "Time":
                continue
            lst = []
            for d in sort[day-int(period/2):day+int(period/2)]:
                lst.append(d[kw])
            day2 = {**day2,**{kw + " (" + str(period) + ") day average":mean(lst)}}
        sort[day] = day2
    return sort


def scrape(username,keywords,limit):
    processed_comments = 0
    lastdate = int(time.time())
    matches = {}
    while processed_comments < limit:
        data = requests.get("https://api.pushshift.io/reddit/search/comment/?size=" + str(min(limit,1000)) + "&author=" + username + "&before=" + str(lastdate)).text
        x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        for c in x.data:
            if matches.get(dateformat(c.created_utc),None) is None:
                matches[dateformat(c.created_utc)] = []
            matches[dateformat(c.created_utc)] += process_comment(c,keywords)
        if len(x.data) is 0:
            break
        processed_comments += len(x.data)
        lastdate = int(x.data[-1].created_utc)
    return matches

def main(args):
    if(args.limit is not None):
        limit = args.limit
    else:
        limit = 100000
    matches = scrape(args.user,args.keywords,limit)
    sort = tally_matches(matches,args.keywords)
    sort = pad_days(sort)
    if(args.average is not None):
        sort = add_averages(sort,args.average)
    fields=list(sort[(max(int(args.average/2),0))].keys())
    writer = csv.DictWriter(sys.stdout,dialect="unix",fieldnames=fields)
    writer.writeheader();
    for row in sort:
        writer.writerow(row)

parser = argparse.ArgumentParser(description='Analyze trends in reddit usage',epilog="Keywords: use +word to match strictly for that word, use r+word to match for subreddit name, use +r+word for both, use %+ for '+'. Percent signs not supported.")
parser.add_argument('user',help='User to analyze. Do not use u/ before it."')
parser.add_argument('keywords',help='Keywords to search for',nargs='+')
parser.add_argument('-l','--limit',help='Max. comments to pull from reddit. Default value is "None"',type=int)
parser.add_argument('-a','--average',help='Period of day average for comment analysis. Default value is "None" (no averaging done). Unaveraged data still output.',type=int)
args = parser.parse_args()

main(args)
