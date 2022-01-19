#IMPORTS
import sys
from textwrap import indent
import requests
import json

base_url = "https://api.stackexchange.com/"
print(base_url)

file_path = sys.argv[1]
file_name = sys.argv[1].split("/")[-1]

if file_path.endswith('.md'):
    #READ ALL SCRIPT ARGUMENTS (PROVIDED IN THE .YML FILE)
    operation = sys.argv[2]
    key = sys.argv[3]
    access_token = sys.argv[4]
    #READ ARTICLE IDs INDEX FILE (EXIT IF FAILED)
    try:
        index_file = open("articles_index.json", 'r+')
        j = json.load(index_file)
    except:
        print("index file not found or failed to load.")
        exit()

    #SCENARIO1: THE .MD FILE WAS DELETED
    if operation == "remove":
        print("Removing and unindexing ", file_name, " 's StackOverflow article...")
        for name, id in j.items():
            if name == file_name:
                article_id = j[name]
                j.pop(name, None)
                index_file.seek(0)
                json.dump(j, index_file, indent=4, sort_keys=True)
                break
        if article_id == None:
            print("The file ", file_name, " is not indexed. please remove from StackOverflow manually.")
            exit()
        r = requests.post(base_url + "2.3/articles/{}/delete?key={}&access_token={}".format(article_id, key, access_token))
        print("success")
        exit()

    #URL ARGUMENTS FOR ADDING/EDITING ARTICLES
    lines = open(file_path, 'r').readlines()
    for line in lines:
        if line.startswith("#"):
            title = line.replace("#", "", 1)
            lines.remove(line)
            break
    body = "".join(lines)
    article_type = "knowledge-article"
    tags = [x.split(".")[0] for x in file_path.split("/") if len(x) > 1]
    payload = {"title" : title, "body" : body, "article_type" : article_type, "tags" : tags, "key" : key, "access_token" : access_token}
    print(payload)

    #SCENARIO2: THE .MD FILE WAS ADDED
    if operation == "add":
        print("Adding and indexing ", file_name, " as a StackOverflow article...")
        r = requests.post(base_url + "2.3/articles/add?", data = payload)
        j[file_name] = json.load(r.text)["items"][0]["article_id"]
        index_file.seek(0)
        json.dump(j, index_file, indent=4, sort_keys=True)
        print("success")
        exit()

    #SCENARIO3: THE .MD FILE WAS EDITED
    if operation == "modify":
        print("Editing ", file_name, "'s StackOverflow article...")
        for name, id in j.items():
            if name == file_name:
                article_id = j[name]
                break
        if article_id == None:
            print("The file ", file_name, " is not indexed. please edit manually then add it to index.")
            exit()
        r = requests.post(base_url + "2.3/articles/{}/edit?key={}".format(article_id), data = payload)
        print("success")
        exit()