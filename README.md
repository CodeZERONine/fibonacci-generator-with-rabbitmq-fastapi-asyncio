## **Fibonacci numbers generator**
Application is build with two main services. 
First one is generating fibonacci number and pushing them to Rabbit MQ.
Second one is consuming messages from RabbitMQ and inserting numbers to database.

#### Fibonacci numbers generator developed with:
- FastAPI
- RabbitQM
- Asyncio
- Docker
- Docker-compose
- SQLAlchemy
- Databases
- AIORMQ

#### To start services user run:
```
docker-compose up -d 
```

#### To stop services and remove containers run:
```
docker-compose stop
docker-compose rm -f
```

#### To run tests use:
```
docker exec -it app bash
pytest
```

#### To generate numbers visit:
http://localhost:8000/fibonacci

#### To check swagger docs visit:
http://localhost:8000/docs