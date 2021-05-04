from fastapi import FastAPI
from fastapi.testclient import TestClient

import asyncio
import aiormq
from schemas import RabbitBody

import os

app = FastAPI()

queueName = os.environ.get("QUEUE_NAME")
rabbitmqHost = os.environ.get("RABBITMQ_HOST")
rabbitmqUser = os.environ.get("RABBITMQ_USER")
rabbitmqPassword = os.environ.get("RABBITMQ_PASSWORD")

async def push_to_rabbit(number: int):
    request = RabbitBody(number)
    connection = await aiormq.connect("amqp://{}:{}@{}/".format(rabbitmqUser, rabbitmqPassword, rabbitmqHost))
    channel = await connection.channel()
    await channel.basic_publish(request.encode(), routing_key=queueName)

async def fibonacci(delay: int):
    a, b = 0, 1
    while True:
        await asyncio.sleep(delay)
        await push_to_rabbit(a)
        yield a
        a, b = b, a + b

fibo = fibonacci(1)

@app.get("/fibonacci/")
async def get_fibonacci_number():
    return await fibo.__anext__()