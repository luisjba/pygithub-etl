# GitHub repo ETL into SQLite database

With this library you can dump a github repository related data into a SqlLite database using PyGithub to consume the Github API V3 and SQLLite3 library to manage our target database.


## Table of contents

- [Installation](#installation)


### Installation
This project use the [PyGithub](https://github.com/PyGithub/PyGithub) library to connect and consume the GitHub API. PyGithub is a Python library to use the [Github API v3](http://developer.github.com/v3>) With it, you can manage your [Github](http://github.com) resources (repositories, user profiles, organizations, etc.) from Python scripts.

The [SQLite3 Python library](https://docs.python.org/3/library/sqlite3.html) is a SQL Interface tha provides ligthweight disk-based database that will be use in this project to store our  estrated data from a GitHub repository.

All the library dependencies requiered for the project are located in the [requirements.txt](requirements.txt) file, and we can use `pip` to install the required libreries runing the command:
```python
pip install -r requirements.txt
```

## Get the GitHub Access Token

The PyGithub library require a GitHub personal token that you must [generate here](https://github.com/settings/tokens). Follow the page instructions and save the token in a secure location. Do not share you token with anyone, because you are allowing to perform actions on your behalf.


