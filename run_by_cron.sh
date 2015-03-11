#! /bin/bash
cd /Users/wiedld/Hackbright/HB_project
echo "line 3 reached"
source env/bin/activate
echo "line 5 reached"
python tasks/CAISO_daily_data_scraper.py