import sys
import requests

base_url = "https://api.stackexchange.com/"
changed_files = sys.argv
article_files = []
for i in changed_files:
    if i.endswith('.md'):
        article_files.append(i)
articles = {}
for i in article_files:
    f = open(i, 'r')
    articles['d'] = {"title" : "", "body" : "", "article_type" : ""}
title = ""
body = ""
article_type = ""
tags = []
key = ""
access_token = ""

payload = {"title" : title, "body" : body, "article_type" : article_type, "tags" : tags, "key" : key, "access_token" : access_token}

r = requests.get(base_url + "2.3/articles?pagesize=2&order=desc&sort=activity&site=stackoverflow")

print(r.text, r.url)