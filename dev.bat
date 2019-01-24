docker build -t py-markets-monitor .

start chrome --new-window "http://localhost:8888"

docker run -it -p 8888:8888 -v "%cd%":/home/ --name=monitor_dev --rm py-markets-monitor bash /home/nb-start.sh