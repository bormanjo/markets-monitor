cd ..

docker build -t py-markets-monitor .

start chrome --new-window "http://localhost:8050"

docker run -p 8050:8050 -v "%cd%":/home/ --name=markets_monitor_app --rm  py-markets-monitor bash /home/app-start.sh
