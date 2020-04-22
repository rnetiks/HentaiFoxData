import json
import os

for file in os.listdir("./data/"):
    tag = str(file)[:-5]
    with open(f"data/{tag}.json","r") as g:
        gals = json.load(g)
        ammount = len(gals["galleries"])
    with open("possible_tags.json","r") as f:
        data = json.load(f)
        data[tag] = ammount
    with open("possible_tags.json","w") as f:
        json.dump(data,f,indent=4)
    with open("Tags.txt","a+") as t:
        t.write(f"\n{tag}: {ammount}")
    print(f"{tag}: {ammount}")
