FROM alpine:latest

# Install required packages
RUN apk add --update --no-cache git python3 py3-pip

# Clone the repository
RUN git clone https://github.com/ztrby/BBStastic.git

# Install Python dependencies
RUN pip install --no-cache-dir --break-system-packages meshtastic
#RUN pip install --no-cache-dir --break-system-packages pypubsub

# Define config volume
VOLUME /datafiles

# Define working directory
WORKDIR /datafiles

# Define the command to run
#CMD ["sh", "-c", " python3 /BBStastic/server.py"]
