# Airflow pollen project
This project is a showcase of how Airflow can be used to
orchestrate a simple ingestion of data into postgres. And
then to notify a user via telegram on certain events. 

A heads up is that I created the same kind of project for
dagster, so this is mainly a refactor to check the
differences between the two.

Specifically it will fetch data on pollen () levels in
Stockholm. It will save the data each day and construct an
SCD2 table containing the valid from and valid to dates of
each status.

If there is a change in the pollen status, a message will be
sent out to the user via telegram, using a bot and a token +
chat id.

The project runs in docker, since my goal was to a) run this
on my raspberry pi b) make it simple to run on other
computers in general and c) to make it into a nice scaffold
for future automations that i might want to run. An added
bonus is that it is very simple to setup a postgres instance
which can have persistent data in between runs.

I use uv to manage the packages. But you don't need it
installed as you are only using docker. You will need to
have docker on your machine though to be running this
project. Docker engine should suffice which is open source.

## How to run
In the root of the project first fill in a .env file since
that will not be part of the repo. You need to fill in
certain values for PG and others for Telegram:

### Postgres .env values
As long as you simply want to try it out these values should
be fine, but you are of course welcome to change db, user or
password. Host and port can be a bit trickier.
```
POSTGRES_DB=mydb  
POSTGRES_USER=myuser  
POSTGRES_PASSWORD=mypass  
POSTGRES_HOST=postgres  
POSTGRES_PORT=5432  
```

### Telegram .env values
For telegram you need to create an account and message
@BotFather to create a new bot. This will give you a token.
Then you can message your bot to start the conversation, you
need to write the first message before a bot can contact
you. You can then save the message id of your conversation
with your bot. Once you have done this you can fill in the 
following values in the .env file  
```
TELEGRAM_BOT_TOKEN  
TELEGRAM_CHAT_ID  
```

### Running docker compose
Once the .env file is filled in with those values in the
root of the project, it is as simple as running the
following command in the terminal  
`docker compose build && docker compose up`

### Checking in on runs
This docker file runs with airflow standalone which means
that you will get an admin user called admin and a password
in the logs when you run it. You can use this to log into
localhost:8080 to view your dags and run history and trigger
runs automatically. For now I have not activated the
schedule which means that you need to trigger it manually to
run. If you trigger the schedule it will run at 7 utc each
morning.

## Repo structure
```
.
├── airflow_pollen                  -- Contains all code for airflow to run
│   ├── __init__.py
│   ├── common                      -- Contains functions meant to be reused across dags
│   │   ├── __init__.py
│   │   ├── connections             -- Contains connections that can be reused such as connections to db
│   │   │   ├── __init__.py
│   │   │   ├── postgres.py         -- Connection to pg
│   │   │   └── telegram.py         -- Connection to telegram
│   │   └── tasks                   -- Contains smaller building blocks (tasks) that make up DAGs 
│   │       ├── __init__.py
│   │       └── pollen_tasks.py     -- Contains tasks specifically for the pollen dag.
│   └── dags                        -- Contains Dags (jobs) in this instance only one of them
│       └── pollen_dag.py           -- Describes how and when to run the pollen dag
├── compose.yaml                    -- Boots the docker image defined in dockerfile, as well as pg and pgadmin
├── Dockerfile                      -- Defines dockerfile which downloads uv and runs airflow
├── entrypoint.sh                   -- Defines start script simply uv run airflow standalone, but nice to have if there is a need for several commands from the start.
├── pyproject.toml                  -- UV description of dependencies etc
├── README.md                       -- Describes purpose of repo and how to run
└── uv.lock                         
```
