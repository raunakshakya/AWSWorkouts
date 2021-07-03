import datetime

for i in range(10):
    ct = datetime.datetime.now()
    ts = round(ct.timestamp() + i)
    print(ts)
