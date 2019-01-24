docker build -t py-markets-monitor .
start chrome --new-window "http://localhost:8888"
docker run --name=monitor_dev -it -p 8888:8888 -v "%cd%":/home/Github/markets-monitor py-markets-monitor
docker exec -it monitor_dev nb-start.sh