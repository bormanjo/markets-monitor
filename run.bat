docker build -t py-markets-monitor .
docker run -it -p 8888:8888 -v "%cd%":/home/Github/markets-monitor py-markets-monitor &
start chrome --new-window "http://localhost:8888"