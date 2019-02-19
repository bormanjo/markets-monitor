FROM python:3.6

# Jupyter Setup

WORKDIR /jup

# Install Node:
RUN apt-get install curl -y
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash
RUN apt-get install --yes nodejs
RUN node -v
RUN npm -v
RUN npm i -g nodemon
RUN nodemon -v

# Install Jupyter
RUN pip install jupyter -U && pip install jupyterlab "ipywidgets>=7.2"

# Jupyter widgets extension
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager@0.38 --no-build

# FigureWidget support
RUN jupyter labextension install plotlywidget@0.6.0 --no-build

# offline iplot support
RUN jupyter labextension install @jupyterlab/plotly-extension@0.18.1 --no-build

# Build extensions (must be done to activate extensions since --no-build is used above)
RUN jupyter lab build

# Python package setup

# Install required packages
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

# Change working directory back to home
WORKDIR /home

# Jupyter Lab Port
EXPOSE 8889

# Dash(board) Port
EXPOSE 8050 

CMD ["/bin/bash"]