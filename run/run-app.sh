#!/usr/bin/env bash

docker build -t py-markets-monitor .

open http://localhost:8050

docker run -p 8050:8050 -v $(pwd):/home/ --name=markets_monitor_app --rm  py-markets-monitor bash /home/app-start.sh
