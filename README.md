# GitHubETL Library

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
import etl
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
import etl
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

A ER model (Entity-relationship model) was desingned to store all the related data of a Github repository. We have 4 schemas:

### Repo Schema

The repo schema is used to fit the data that the GitHub API provide as response for a requested repository.

```json
{'id': 408675469,
 'node_id': 'R_kgDOGFvkjQ',
 'name': 'pygithub-etl',
 'full_name': 'luisjba/pygithub-etl',
 'private': False,
 'owner': {'login': 'luisjba',
  'id': 1441722,
  'node_id': 'MDQ6VXNlcjE0NDE3MjI=',
  'avatar_url': 'https://avatars.githubusercontent.com/u/1441722?v=4',
  'gravatar_id': '',
  'url': 'https://api.github.com/users/luisjba',
  'html_url': 'https://github.com/luisjba',
  'followers_url': 'https://api.github.com/users/luisjba/followers',
  'following_url': 'https://api.github.com/users/luisjba/following{/other_user}',
  'gists_url': 'https://api.github.com/users/luisjba/gists{/gist_id}',
  'starred_url': 'https://api.github.com/users/luisjba/starred{/owner}{/repo}',
  'subscriptions_url': 'https://api.github.com/users/luisjba/subscriptions',
  'organizations_url': 'https://api.github.com/users/luisjba/orgs',
  'repos_url': 'https://api.github.com/users/luisjba/repos',
  'events_url': 'https://api.github.com/users/luisjba/events{/privacy}',
  'received_events_url': 'https://api.github.com/users/luisjba/received_events',
  'type': 'User',
  'site_admin': False},
 'html_url': 'https://github.com/luisjba/pygithub-etl',
 'description': 'Python library that uses PyGithub library to consume GitHub API authenticated by  token, to Extract Transform and Load the related data into a SQLite database to analyze it.',
 'fork': False,
 'url': 'https://api.github.com/repos/luisjba/pygithub-etl',
 'forks_url': 'https://api.github.com/repos/luisjba/pygithub-etl/forks',
 'keys_url': 'https://api.github.com/repos/luisjba/pygithub-etl/keys{/key_id}',
 'collaborators_url': 'https://api.github.com/repos/luisjba/pygithub-etl/collaborators{/collaborator}',
 'teams_url': 'https://api.github.com/repos/luisjba/pygithub-etl/teams',
 'hooks_url': 'https://api.github.com/repos/luisjba/pygithub-etl/hooks',
 'issue_events_url': 'https://api.github.com/repos/luisjba/pygithub-etl/issues/events{/number}',
 'events_url': 'https://api.github.com/repos/luisjba/pygithub-etl/events',
 'assignees_url': 'https://api.github.com/repos/luisjba/pygithub-etl/assignees{/user}',
 'branches_url': 'https://api.github.com/repos/luisjba/pygithub-etl/branches{/branch}',
 'tags_url': 'https://api.github.com/repos/luisjba/pygithub-etl/tags',
 'blobs_url': 'https://api.github.com/repos/luisjba/pygithub-etl/git/blobs{/sha}',
 'git_tags_url': 'https://api.github.com/repos/luisjba/pygithub-etl/git/tags{/sha}',
 'git_refs_url': 'https://api.github.com/repos/luisjba/pygithub-etl/git/refs{/sha}',
 'trees_url': 'https://api.github.com/repos/luisjba/pygithub-etl/git/trees{/sha}',
 'statuses_url': 'https://api.github.com/repos/luisjba/pygithub-etl/statuses/{sha}',
 'languages_url': 'https://api.github.com/repos/luisjba/pygithub-etl/languages',
 'stargazers_url': 'https://api.github.com/repos/luisjba/pygithub-etl/stargazers',
 'contributors_url': 'https://api.github.com/repos/luisjba/pygithub-etl/contributors',
 'subscribers_url': 'https://api.github.com/repos/luisjba/pygithub-etl/subscribers',
 'subscription_url': 'https://api.github.com/repos/luisjba/pygithub-etl/subscription',
 'commits_url': 'https://api.github.com/repos/luisjba/pygithub-etl/commits{/sha}',
 'git_commits_url': 'https://api.github.com/repos/luisjba/pygithub-etl/git/commits{/sha}',
 'comments_url': 'https://api.github.com/repos/luisjba/pygithub-etl/comments{/number}',
 'issue_comment_url': 'https://api.github.com/repos/luisjba/pygithub-etl/issues/comments{/number}',
 'contents_url': 'https://api.github.com/repos/luisjba/pygithub-etl/contents/{+path}',
 'compare_url': 'https://api.github.com/repos/luisjba/pygithub-etl/compare/{base}...{head}',
 'merges_url': 'https://api.github.com/repos/luisjba/pygithub-etl/merges',
 'archive_url': 'https://api.github.com/repos/luisjba/pygithub-etl/{archive_format}{/ref}',
 'downloads_url': 'https://api.github.com/repos/luisjba/pygithub-etl/downloads',
 'issues_url': 'https://api.github.com/repos/luisjba/pygithub-etl/issues{/number}',
 'pulls_url': 'https://api.github.com/repos/luisjba/pygithub-etl/pulls{/number}',
 'milestones_url': 'https://api.github.com/repos/luisjba/pygithub-etl/milestones{/number}',
 'notifications_url': 'https://api.github.com/repos/luisjba/pygithub-etl/notifications{?since,all,participating}',
 'labels_url': 'https://api.github.com/repos/luisjba/pygithub-etl/labels{/name}',
 'releases_url': 'https://api.github.com/repos/luisjba/pygithub-etl/releases{/id}',
 'deployments_url': 'https://api.github.com/repos/luisjba/pygithub-etl/deployments',
 'created_at': '2021-09-21T03:28:01Z',
 'updated_at': '2021-09-21T06:48:00Z',
 'pushed_at': '2021-09-21T06:47:57Z',
 'git_url': 'git://github.com/luisjba/pygithub-etl.git',
 'ssh_url': 'git@github.com:luisjba/pygithub-etl.git',
 'clone_url': 'https://github.com/luisjba/pygithub-etl.git',
 'svn_url': 'https://github.com/luisjba/pygithub-etl',
 'homepage': None,
 'size': 18,
 'stargazers_count': 0,
 'watchers_count': 0,
 'language': 'Python',
 'has_issues': True,
 'has_projects': True,
 'has_downloads': True,
 'has_wiki': True,
 'has_pages': False,
 'forks_count': 0,
 'mirror_url': None,
 'archived': False,
 'disabled': False,
 'open_issues_count': 0,
 'license': None,
 'allow_forking': True,
 'forks': 0,
 'open_issues': 0,
 'watchers': 0,
 'default_branch': 'master',
 'permissions': {'admin': True,
  'maintain': True,
  'push': True,
  'triage': True,
  'pull': True},
 'temp_clone_token': '',
 'network_count': 0,
 'subscribers_count': 1}
```

