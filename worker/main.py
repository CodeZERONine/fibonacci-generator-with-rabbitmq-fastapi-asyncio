import asyncio
import aiormq

from aiormq.abc import DeliveredMessage
from schemas import RabbitBody

import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer
from databases import Database

exchange_name = os.environ.get("EXCHANGE_NAME")
rabbitmq_host = os.environ.get("RABBITMQ_HOST")
rabbitmq_user = os.environ.get("RABBITMQ_USER")
rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD")

postgres_host = os.environ.get("POSTGRES_HOST")
postgres_port = os.environ.get("POSTGRES_PORT")
postgres_database = os.environ.get("POSTGRES_DB")
postgres_user = os.environ.get("POSTGRES_USER")
postgres_password = os.environ.get("POSTGRES_PASSWORD")

DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(postgres_user, postgres_password, postgres_host, postgres_port, postgres_database)

engine = create_engine(DATABASE_URL)
database = Database(DATABASE_URL)
metadata = MetaData()

fibonacci = Table(
    'fibonacci', metadata,
    Column('id', Integer, primary_key=True),
    Column('number', Integer)
)

metadata.create_all(engine)

async def insertFibo(message: DeliveredMessage):
    response = RabbitBody.decode(message.body)
    query = fibonacci.insert().values(number=response.fibo)
    await database.connect()
    await database.execute(query=query)
    await database.disconnect()

    await message.channel.basic_ack(
        message.delivery.delivery_tag
    )

async def consume():
    connection = await aiormq.connect("amqp://{}:{}@{}/".format(rabbitmq_user, rabbitmq_password, rabbitmq_host))
    channel = await connection.channel()
    
    await channel.basic_qos(prefetch_count=1)

    await channel.exchange_declare(
        exchange=exchange_name, exchange_type='direct'
    )
    
    declare = await channel.queue_declare(durable=True, auto_delete=True)
    await channel.queue_bind(declare.queue, exchange_name, routing_key='fibonacci')

    await channel.basic_consume(declare.queue, insertFibo)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())
    loop.run_forever()