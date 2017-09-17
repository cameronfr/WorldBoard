FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN pip3 install http://download.pytorch.org/whl/cu75/torch-0.2.0.post3-cp36-cp36m-manylinux1_x86_64.whl
RUN pip3 install torchvision
RUN pip3 install pandas
RUN pip3 install -U spacy
RUN pip3 install satori
RUN python -m spacy download en
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -yq nodejs
RUN pip3 install Flask-Shelve
RUN pip3 install newspaper3k

COPY ./app /app
WORKDIR /app
RUN npm install --save-dev webpack-dev-server webpack
RUN npm install --save-dev react-hot-loader
RUN npm install --save-dev babel-core babel-loader babel-preset-env babel-preset-react
RUN npm install --save react react-dom
RUN npm install --save golden-layout jquery
RUN npm install --save highcharts
