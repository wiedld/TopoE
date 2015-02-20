import datetime

# This file should include the api call to CAISO, cron every 10 minute.  Collects realtime data which updates every 10 minutes.


current = datetime.datetime.now()
cur_str = str(current)

f = open('log_file.txt','a')
f.write(cur_str)
f.close