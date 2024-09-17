## Usage

After installation, the application can be run.

Depending on the method of installation, the way to run it is different.

All commands are performed in a command line terminal opened in the root directory unless stated otherwise.
[See how to open a terminal in a directory.](https://www.lifewire.com/open-command-prompt-in-a-folder-5185505)

When the application starts it will open at http://127.0.0.1:8000

### Docker

Run:
``docker compose up --build``

Close:
Press `Ctrl + C` in the terminal


### Manually

When running manually you will need to start up multiple processes.

 - RabbitMQ
    RabbitMQ is used from the RabbitMQ Command Prompt (sbin dir), which should be found when searching through for it
    by pressing the start key. Finding it might differ based on your operating system.
    After opening it you should run
    ``rabbitmq-server``
    
    This should start the server.
    It is possible that an error is shown, if the error says that rabbitmq is already running on the port, that means it has been previously started, or has started on startup of the device. This should be okay.

 - Celery
    After RabbitMQ has been started you can startup Celery. The order does not matter, but Celery requires RabbitMQ to have been started to function.

    You will need to open a terminal and run the following commands in order:
    
    1.
    ``venv\scripts\activate``
    2.
    Unix:
    ``celery -A BlastBuddyClub worker -l INFO``
    Windows:
    ``celery -A BlastBuddyClub worker -l INFO -P gevent``

 - The app
    To run the app, you will need to open a terminal and run the following commands in order:
    1.
    ``venv\scripts\activate``
    2.
    ``py manage.py runserver``

    This will now run the app.