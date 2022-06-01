# Alternatives, Inspiration and Comparisons

## Introduction

FastAPI is not Python API framework that I approached at begin.

I try many framework, micro-framework such as [Flask](https://flask.palletsprojects.com/en/2.1.x/), [Django](https://www.djangoproject.com/), [Pyramid](https://trypyramid.com/). So, each framework left an impression on me.

As I said at the beginning, my inspiration is [Cookiecutter Django](https://github.com/cookiecutter/cookiecutter-django). Inspiration includes:

- Code structure.
- Mindset break settings for environments.
- Mindset integration third-party, cloud service.
- Thinking of setting up code for easy deployment.
- ...

But why do I use FastAPI to build the codebase? Have reasons:

- FastAPI very fast. It impressed me. You know that, Python is pretty slow compared to [Go](https://go.dev/), [Nodejs](https://nodejs.org/en/). After working with FastAPI, I had to change my mind.
- FastAPI support validation in core. If you use Flask, Django Pure, you need install third-party package like [marshmallow](https://marshmallow.readthedocs.io/en/stable/).I don't like it. Other solution, you can use [Django REST framework](https://www.django-rest-framework.org/) with [Serializers](https://www.django-rest-framework.org/api-guide/serializers/).  
- FastAPI is very easy to use and learn. Easy to integration with other library. This I find similar to Flask.
- ...

Personal opinion about my codebase:

- My codebase can be not good for all project.
- MRLSR architecture can be not good for you. MVC pure or [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) may be is better.
- Base is not Base - This codebase contains my ideas and experiences in projects. So, you don't have to hesitate and improve it. Try to personalize it so that the codebase is truly yours.
- ...

Finally, here is a comparison when you need to build the API codebase with Python.

## Comparisons

### Web framework

|   | Django Rest framework| Flask | FastAPI | |
|---|---|---|---|---|
|Repository| [https://github.com/encode/django-rest-framework](https://github.com/encode/django-rest-framework) | [https://github.com/pallets/flask](https://github.com/pallets/flask) | [https://github.com/tiangolo/fastapi](https://github.com/tiangolo/fastapi) | |
|Full framework| Yes | No | No | |
|Design pattern | MVC | No | No | |
|Easy to study| No | Yes | Yes  | for newbie|
|Contributing| 23.4k stars | 59.1k stars | 45.4k stars | Github stars |
|Authors| [Tom Christie](https://fund.django-rest-framework.org/topics/funding/) | [Armin Ronacher](https://en.wikipedia.org/wiki/Flask_(web_framework)#:~:text=Flask%20was%20created%20by%20Armin,make%20into%20a%20serious%20application.) | [Sebastián Ramírez](https://github.com/tiangolo) | Github stars |
|License| BSD License | BSD License | MIT license | |

### Object-Relational Mapping (ORM) and Database driver engine

In my codebase, I used SQLAlchemy. With example CRUD, I used the PostgreSQL with `psycopg2` driver. Some alternatives `psycopg2`:

- [pg8000](https://github.com/tlocke/pg8000)
- [asyncpg](https://magicstack.github.io/asyncpg/current/)
- ...

My codebase support config database by URI. Example with PostgreSQL:

```bash
export DATABASE_URI=postgresql+asyncpg://user:password@host:port/dbname[?key=value&key=value...]
```

So, it's very flexible to use SQL database engine and driver engine. You can also add option to DATABASE_URI. Other example:

```bash
export DATABASE_URI=mysql+pymysql://user:pass@some_mariadb/dbname?charset=utf8mb4
```

SQLAlchemy DBAPI Support:

- [MySQL](https://docs.sqlalchemy.org/en/14/dialects/mysql.html#dialect-mysql)
- [PostgreSQL](https://docs.sqlalchemy.org/en/14/dialects/postgresql.html)
- [SQLite](https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#dialect-sqlite)
- [Oracle](https://docs.sqlalchemy.org/en/14/dialects/oracle.html#dialect-oracle)
- [Microsoft SQL Server](https://docs.sqlalchemy.org/en/14/dialects/mssql.html#dialect-mssql)

With driver engine, if you take care about performance, you should choose asynchronous driver like `asyncpg`, `asyncmy`, `aiomysql`. If you take care about stability,easy and official, the driver like `pg8000`, `psycopg2` or `mysqlclient` is your solution.

#### Asynchronous task

Asynchronous task or Worker is an integral part of the modern system. We may be 2 solutions:

- Use [BackgroundTasks](https://fastapi.tiangolo.com/sq/tutorial/background-tasks/?h=backgroundtasks#background-tasks) of FastAPI
- Use [Celery](https://docs.celeryq.dev/) framework

**Docs quote: "Background Tasks"**
> If you need to perform heavy background computation and you don't necessarily need it to be run by the same process (for example, you don't need to share memory, variables, etc), you might benefit from using other bigger tools like Celery.

> They tend to require more complex configurations, a message/job queue manager, like RabbitMQ or Redis, but they allow you to run background tasks in multiple processes, and especially, in multiple servers.

From the docs [fastapi.tiangolo.com](https://fastapi.tiangolo.com/tutorial/background-tasks/#caveat)

In my codebase, we use `RabbitMQ` to message broker and `Redis` to backend. The reasons:

**Docs quote: "Choosing a Broker"**
> RabbitMQ is feature-complete, stable, durable and easy to install. It’s an excellent choice for a production environment.
>
> Redis is also feature-complete, but is more susceptible to data loss in the event of abrupt termination or power failures.

From the docs [docs.celeryq.dev](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#choosing-a-broker)

#### Logging

Logging package built-in on Python before version Alpha 5 is pretty bad with newbie. So, I use to [loguru](https://github.com/Delgan/loguru). `loguru` very easy to config and understand.
But, if you want to use [Python Alpha 5](https://realpython.com/python-news-february-2022), you should use `logging` package built-in.

Loguru example:

![Loguru](images/loguru3.png "Loguru")

Logging in Python Alpha 5 example:

```bash
$ python3.10 test.py
Traceback (most recent call last):
  File "/home/realpython/test.py", line 2, in <module>
    w = x / y / z
ZeroDivisionError: float division by zero

$ python3.11a5 test.py
  File "/home/realpython/test.py", line 2, in <module>
    w = x / y / z
        ~~~~~~^~~
ZeroDivisionError: float division by zero
```

#### Docs API

[OpenAPI](https://swagger.io/blog/api-design/openapi-3-0-specification-training/) is built and enabled into FastAPI by default. It's very simple to use. But, if you wanna to use other tool, you can disable by setting:

```py
app = FastAPI(
    docs_url=None,
)
```
