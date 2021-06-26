# GitCrawl

This is a project, that allows you to download all the repositories on the given topic from GitHub

## How it works
- We have a database with the files that fit the description (for this project we only have repositories dedicated to `nlp` and having `python` as their main language)
- We send them to a remote message queue
- We use message queues to distribute files between several workers to download them faster
- The files' content is stored in an easily accessible database

YOU can help us download the files!

## How To Use
**0. Prerequisites**

Clone this repo and install all the dependencies:
```
git clone https://github.com/evtaktasheva/gitcrawl
cd gitcrawl
sh install_tools.sh 
```

For the code to run you will need to create a `conf.py` file with several parameters:
- `DB_LOGIN`, `DB_PASSWORD`: login and password for a remote database you use
- `SERVER_LOGIN`, `SERVER_PASSWORD`: login and password for a RabbitMQ message queue
- `GITHUB_LOGIN`, `GITHUB_TOKEN`: your github login and API token

**1. Message Queue**

The first step in downloading the files is setting up a queue. To do this you will require to
- **Get the list of files to download**: use `repo_crawl.py` to create a database and crawl GitHub for the links to files. Remember to define the files you want to download (check [`GitHub REST API`](https://docs.github.com/en/rest) and [`PyGithub`](https://github.com/PyGithub/PyGithub) documentations for details)
- **Setup a RabbitMQ message queue**: read [`RabbitMQ`](https://www.rabbitmq.com/documentation.html) documentation to find out how
- **Send files to queue**: use `main.py` 

**2. Downloading**

To download the files, run `worker.py`

- Remember to change the database and queue information if you want to download your own collection of files.
- If you want to help us download the files, ask for the `DB_LOGIN`, `DB_PASSWORD`, `SERVER_LOGIN` and`SERVER_PASSWORD` credentials
