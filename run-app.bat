docker build -t py-markets-monitor .

docker run -d -p 8050:8050 -v "%cd%":/home/Github/markets-monitor --name=markets_monitor_app --rm  py-markets-monitor bash /home/Github/markets-monitor/app-start.sh

start chrome --new-window "http://localhost:8050"
