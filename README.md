# GitHubETL library

GitHubETL is a Python library that use the [PyGithub library](https://github.com/PyGithub/PyGithub/) to consume the [Github API v3](http://developer.github.com/v3)
to extrac the data from any [Github](http://github.com) repository, transform and load the data into a SqlLite database (we use the [SQLite3 Python library](https://docs.python.org/3/library/sqlite3.html) to manipulate our database).

## Table of contents

- [Installation](#installation)
    * [Download](#download)
    * [Install Dependencies](#install-dependencies) 
- [Usage](#usage)
    * [Get the GitHub Access Token](#get-the-gitHub-access-token)
    * [Usage by Command Line](#usage-by-command-line)
    * [Usage as Library](#usage-as-library)

## Installation

This program is written in Python 3.x. There is no backward compatibility with 2.x, since 3.x is the future.

### Download

Open your desired terminal (or GithBash in windows), move to your desired directory where you want to donwload the library. Clone the repository and navigate to the donwloaded directory.
```bash
$ git clone https://github.com/luisjba/pygithub-etl.git
$ cd pygithub-etl

```

### Install Dependencies

All the library dependencies requiered for the project are located in the [requirements.txt](requirements.txt) file.  We can use  `pip` to install the required libreries runing the command:
```python
pip install -r requirements.txt
```

## Usage

Usage is strightforward, all the options can be used by  the `main.py`  passing the coresponding options or by importing the library in you own project.

As the program consume the [Github API v3](http://developer.github.com/v3), we need the acces token to properly connect and consume the API.

### Get the GitHub Access Token

The PyGithub library require a GitHub personal token that you must [generate here](https://github.com/settings/tokens). Follow the page instructions and save the token in a secure location. Do not share you token with anyone, because you are allowing to perform actions on your behalf.

Once you have your token you can use them to comunicate your own Github repositories or any other public. 


### Usage by Command Line

To show the available options, you can pass the `--help` option to the `main.py` file to get the help and detailed options.
```bash
$ python main.py --help
GithubETL Library

Usage:
  main.py help
  main.py version
  main.py sync TOKEN REPO [--db=<database>] [--sdir=<schemadirectory>]
  main.py analize [--db=<database>]

Arguments:
  TOKEN        The GitHub Token
  REPO         The fullname of a GitHub repository

Options:
    -h, help         Show help
    -v, version      Version
    -f, force_update Force the update of commit and files
    --db=<database>  The SQLlite database file, by default is 'data/data.db'
    --sdir=<schemadirectory> The schema directory to find the corresponding DDL for table creation,by default is 'schemas'.
$
```
#### Basic usage


The `TOKEN` and `REPO` arguments are required for connect to the Github API and retrive the desired repository data. Basic example to get the current repository data information usync the sync command:

```bash
$ python main.py sync XXXXXXXXXXXXXX  luisjba/pygithub-etl
```

By default, the database is created in `data/data.db` if not exists and will be use it to connect and dump all the data into it.

#### Custom database

We can set our desired location for the database, for example, if we want the output in out home directory in a `Project` directory with  `my_repo.db` as database file. Do not forget to pass the token ofter the sync command (replace the 'XXX' by your token).

```bash
$ python main.py sync XXXXXXXXXXXXXX  my_user/my_repo --db ~/Project/my_repo.db
```

### Usage as Library

To use as library, wirte your implementation in the current clonned project or copy the `etl` and `schemas` into your desired project. We jave to import the  `GithubETL` class.
```python
from etl import GithubETL
```

To instantiate the `GithubETL`, the constructor requires the Github access token ( go to [Get the GitHub Access Token](#Get-the-GitHub-Access-Token) for more details ) and the full name of the repository.

```pyton
token = "XXXXXXXXX"
repo_fullname = "luisjba/pygithub-etl"
getl = GithubETL(token, repo_fullname)
```

On the instantiation process, the library internally perform the connection to the GitHub API, try the connection to the database and create a blank one of not exists. If any error ocurrs, a message error is displayed and the applications exits.

If all is ok (the token is valid and the database connection was successfull), you will have available the following functions to call as your convenience:

* `sync_repo()` : Fetch the repo information , extract the data, transform and load it into the `repo` table in the database.
* `sync_branches()`: Fetach the related brances, extract the data, transform and load it into the `branch` table in the  database.
* `sync_commits(force_update=False)`: Fetach all the commits of the repo, extract the data, transform and load it into the `commits` table in the database. Each commits contains the related modified files, each related file is stored inot the `commit_file` table in the database.


#### All toguether

```python
from etl import GithubETL

token = "XXXXXXXXX"
repo_fullname = "luisjba/pygithub-etl"
getl = GithubETL(token, repo_fullname)

# Sincronize repo
getl.sync_repo()

# Sincronize branches
getl.sync_branches()

# Sincronize commits and files
getl.sync_commits()

# we can force to update the commits if already exists with
# the 'force_update' parameter in 'sync_commits' function
getl.sync_commits(true)
```

## Schemas



