## Installation

There are currently two ways to install the tools required to run the application, it is possible to install it manually or through the use of Docker.

When setting up everything manually, it will take more effort to run everything compared to Docker, and will require you to keep track of more separate processes, however, it will allow you more / easier flexibility in developing the application. It makes it easier to migrate the database, and perform django commands related to manage.py.

Docker is recommended when deploying, or when there is no need to actively develop, such as demoing.


### Clone repository
Regardless of using Docker, it is necessary to clone the repository manually.
There are several ways to clone the repository to get it running on your machine.

 - Git clone
    You can clone the repository, this option will require [git to be installed](https://git-scm.com/).
    If git is not installed, you can simply install git with all the default settings.

    You can then in the command line, in the directory where you want the repository to execute:
    [(This can be done by navigating to a directory, and press the path bar and fill in "cmd" and then pressing enter).](https://www.lifewire.com/open-command-prompt-in-a-folder-5185505)
    ``git clone http://145.97.18.141/bbc-bweb2/bbc-app.git``

    On executing the command it will prompt for your credentials.
    After filling in your credentials it will automatically clone the repository.

    Note: The exact name of the repository is not guaranteed, please see the repository on the webpage to be sure if it's correct.

    It is also possible to clone a repository through IDE's such as Pycharm or VSCode.
    This might not require the separate installation of git.
    Please consult a guide on your respective IDE.

 - Download a zip file of the [repository](http://145.97.18.141/bbc-bweb2/bbc-app/-/tree/main?ref_type=heads).
    This option is only viable when you are unlikely to upgrade to a later version, and are not 
    in a development environment. Otherwise, it is recommended to clone instead.

### Docker
To use Docker, you need to [download Docker](https://www.docker.com/products/docker-desktop/).
After downloading Docker, it is possible that a large amount of RAM is suddenly used up, this can be resolved  [following this guide](https://www.aleksandrhovhannisyan.com/blog/limiting-memory-usage-in-wsl-2/).

Docker is also prone to using up a lot of disc space, we don't have a specific guide to solve this issue, 
however it is good to keep in mind if this might create issues for you.

### Manually

#### Python
It is necessary to install python.
This application is setup and tested using [python 3.11.8](https://www.python.org/downloads/release/python-3118/)
When installing through the installer, it is recommended to select "Add python.exe to PATH".

##### Virtual environment
This section will create a virtual environment through the command line. It is also possible to do this in an IDE.
If you wish to do it through an IDE, you will need to look up your own guide for it.

A virtual environment can be created by opening the command line in the cloned repositories root directory.
In the command line execute the command:

`py -3.11 -m venv venv`

If an error occurs, it might be because you did not install 3.11, or did not add python as PATH variable.
Please check if you have 3.11.x installed, and if not reinstall python.

The previous command will automatically create a directory "venv".
If you created the venv in the right directory, it should be inside of the cloned bbc-app.

You will then need to activate the environment:

On windows:
`venv\scripts\activate`

On Unix / Mac:
`source venv/bin/activate`

After activating the environment the python requirements will need to be installed.
There are different requirements dependent on usage.

dev:
`pip install -r requirements/dev.txt``


#### RabbitMQ
The project has been configured and developed using version 3.13.1 RabbitMQ

RabbitMQ requires Erlang to work, and supports versions from 26.0 to 26.2.x
Erlang will need to be downloaded separately, this project has been tested using [26.2.5](https://www.erlang.org/patches/otp-26.2.5)
Please note that only 1 version of Erlang can be installed at a time for RabbitMQ. If multiple versions of Erlang
need to be installed please refer back to Docker.

The specific version of RabbitMQ can be installed through the [3.13.1 release page](https://github.com/rabbitmq/rabbitmq-server/releases/tag/v3.13.1)
When installing from there "rabbitmq-server-3.13.1.exe" is the easiest to install.

Instead of using the installers, it's also possible to use a package manager, like [Chocolatery](https://chocolatey.org/) or [brew](https://brew.sh/).
For these examples the installation can be done through the command line:
    ``choco install rabbitmq --version 3.13.1``
    or
    ``brew install rabbitmq@3.13.1``
