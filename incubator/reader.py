import time, requests
from datetime import datetime

while True:
    time.sleep(300)
    try:
        r = requests.post("http://localhost:5000/readsensor", timeout=10)
    except:
        print("{}: readsensor failed".format(datetime.now()))
        continue
    if r.status_code != 200:
        print("{}: readsensor failed status: ".format(
            datetime.now(), r.status_code))
        continue
        
    print (r.text)
