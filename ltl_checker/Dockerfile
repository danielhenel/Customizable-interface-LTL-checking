FROM ubuntu:22.04

WORKDIR /app

# copy requirements
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
python3.10 \
python3-pip


RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# configure the container to run in an executed manner
ENTRYPOINT [ "python3" ]

CMD ["main.py" ]