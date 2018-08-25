import requests
import configparser
import sys

def getdata(url):
    try:
        ans = requests.get("https://www.thebluealliance.com/api/v3/" + url,
                           "accept=application%2Fjson&X-TBA-Auth-Key=ZjJzrR9KQ3X1kg5jsfUn8cKs42N5B0pDNyeuLXXLBLZRIQiUFWbk81ISY9E36J4V").json()
        if ans is not None:
            return ans
        else:
            print("oops null " + url)
            getdata(url)
    except:
        print("oops " + url)
        getdata(url)

config = configparser.ConfigParser()
config.read("../config.ini")
event = config["DEFAULT"]["EventKey"]

matches = getdata("event/"+event+"/matches/simple")
if matches is None or len(matches) == 0:
    print("Data not loaded.")
    sys.exit(0)

with open(config["DEFAULT"]["TBA_Data_File"], "w+") as file:
    file.write(event + "\nMatch,R1,R2,R3,L1,L2,L3\n")
    for match in matches:
        if match["comp_level"] == "qm":
            file.write(str(match["match_number"]) + "," + ",".join(match["alliances"]["red"]["team_keys"] + match["alliances"]["blue"]["team_keys"]) + "\n")

print("Match data loaded for " + event + ".")