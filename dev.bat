docker build -t py-markets-monitor .

start chrome --new-window "http://localhost:8889"

docker run -it -p 8889:8889 -v "%cd%":/home/ --name=monitor_dev --rm py-markets-monitor bash /home/nb-start.sh