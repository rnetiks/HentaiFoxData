import json
import os

things = {}

types = ["parodies","characters","tags","artists","groups","categories"]
for type in types:
    things[type] = {}
    for file in os.listdir(f"./{type}/"):
        abc = str(file)[:-5]
        try:
            with open(f"{type}/{abc}.json","r") as g:
                gals = json.load(g)
            things[type][abc] = len(gals["galleries"])
            print(f"{type}/{abc}.json is fine")
        except:
            print(f"\n{type}/{abc}.json is broke\n")
            os.system("pause")

with open("data.json","w") as f:
    json.dump(things,f,indent=4)
