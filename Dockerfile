FROM python:3.6

WORKDIR /jup

RUN pip install jupyter -U && pip install jupyterlab

WORKDIR /home/Github/markets-monitor

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

# Jupyter Lab Port
EXPOSE 8888 

# Dash(board) Port
EXPOSE 8050 

ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]