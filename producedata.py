import random
from time import sleep, time
from json import dumps
import numpy as np
from kafka import KafkaProducer

my_producer = KafkaProducer(
    bootstrap_servers = ['localhost:9092'],
    value_serializer = lambda x:dumps(x).encode('utf-8')
    )

while True:
    heartbeat = round(random.uniform(65, 100),2)
    pressure = random.randint(5, 15)
    volume = random.randint(150, 200)
    flow = random.randint(50, 150)
    oxygen = round(random.uniform(0.20, 1),2)
    data={}
    data["pressure"]=pressure
    data["volume"]=volume
    data["flow"]=flow
    data["oxygen"]=oxygen
    data["heartbeat"]=heartbeat
    data2 = {}
    data2["pressure"] = pressure
    data2["volume"] = volume
    data2["flow"] = flow
    data2["oxygen"] = oxygen
    data2["heartbeat"] = heartbeat
    my_data = {'Patient1': data,
               'Patient2':data2}
    print(my_data)
    my_producer.send('heartbeat', value=my_data)
    sleep(2)
