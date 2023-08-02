FROM python:3.11

# First, install dependencies
RUN pip3 install cmake
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY scripts/install-coap-client.sh /usr/src/app/scripts/install-coap-client.sh
RUN mkdir -p /usr/src/build
RUN cd /usr/src/build
RUN chmod +x /usr/src/app/scripts/install-coap-client.sh
RUN /usr/src/app/scripts/install-coap-client.sh

COPY . /usr/src/app

WORKDIR /usr/src/app
# Run the python script brain.py when the container launches
CMD ["python3", "brain.py"]