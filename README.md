# elba_autoreg
##Installation
* Clone  script and html-email from repository;
* Create cron-task to run this script periodically
```sh
crontab -e
```
```sh
*/2 * * * * /usr/bin/python /home/autoreg/autoreg_new.py
```
