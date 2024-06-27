import requests
import os
import json


path = "./productData/"
# get all files
files = os.listdir(path)
files = files[::-1]
count = 0
for dataFile in files:
    data = json.load(open(path + dataFile))
    for i in range(len(data)):
        try:
            print(count, data[i]["attributes"]["name"])
            compared_CKSID = data[i]["attributes"]["compared_CKSID"]
            url = "https://cashkaro.com/_next/data/rczn7kLVXRmrxCYWQ8QmM/tiger/"+compared_CKSID+".json"

            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            newData = response.json()["pageProps"]["data"]
            data[i]["relationships"] = newData["relationships"]
            data[i]["attributes"]["facets"] = newData["attributes"]["facets"]
            data[i]["attributes"]["key_features"] = newData["attributes"]["key_features"]
            with open(path + dataFile, "w") as file:
                json.dump(data, file)
        except:
            pass
        count += 1
    print(dataFile + " Done!")
