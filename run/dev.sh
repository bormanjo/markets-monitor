#!/usr/bin/env bash

docker build -t py-markets-monitor .

open http://localhost:8889

docker run -it -p 8889:8889 -v $(pwd):/home/ --name=monitor_dev --rm py-markets-monitor bash /home/nb-start.sh