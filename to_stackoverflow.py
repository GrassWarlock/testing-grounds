import sys
import requests

base_url = "https://api.stackexchange.com/"
target_file = sys.argv[1]

if target_file.endswith('.md'):
    operation = sys.argv[2]
    lines = open(target_file, 'r').readlines()


    for line in lines:
        if line.startswith("#"):
            title = line.replace("#", "", 1)
            lines.remove(line)
            break
    body = "".join(lines)
    article_type = "knowledge-article"
    tags = [x.split(".")[0] for x in target_file.split("/") if len(x) > 1]
    key = sys.argv[3]
    access_token = sys.argv[4]

    payload = {"title" : title, "body" : body, "article_type" : article_type, "tags" : tags, "key" : key, "access_token" : access_token}
    print(payload)
    if operation == "add":
        print("opadd")
    if operation == "opmodify":
        print("modify")
    if operation == "remove":
        print("opremove")
    r = requests.get(base_url + "2.3/articles?pagesize=2&order=desc&sort=activity&site=stackoverflow")

    print(r.text, r.url)