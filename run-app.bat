docker build -t py-markets-monitor .
docker run -it -p 8050:8050 -v "%cd%":/home/Github/markets-monitor py-markets-monitor 

start chrome --new-window "http://localhost:8050"
