FROM ubuntu:20.04

WORKDIR /code

# copy requirements.txt to root
COPY requirements.txt requirements.txt

# install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# copy all files into the working directory
COPY . /code/

# command to run on container start
CMD [ "python", "main.py"]