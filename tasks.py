from crontab import CronTab


empty_cron = CronTab
my_user_cron = CronTab(user=True)
## TODO:  github to my machine, and update this with admin username.
users_cron = CronTab(user='username')

# the example given
# job  = cron.new(command='/usr/bin/echo', comment='IDnum')

job  = cron.new(command='/tasks/api.py', comment='CAISO api initiated')

job.minute.every(10)

