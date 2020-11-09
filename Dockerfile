FROM python:3.6

# install chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
RUN apt-get install -y xvfb

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app


RUN pip install --no-cache-dir pipenv
COPY ./Pipfile /usr/src/app
COPY ./Pipfile.lock /usr/src/app

RUN pipenv install -d

COPY . /usr/src/app

CMD ["pipenv", "run", "python",  "main.py"]
