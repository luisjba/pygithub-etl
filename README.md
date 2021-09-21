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

- id : integer value used as primary key for each repository.
- name: string value to store the repository name.
- owner: string value to store the owner name.
- fullname: string value to store the repository full name.
- description: string value to store the repository description.
- url : string value to store the url location of the repository.
- pushed_date: int value to store the timestamp of the pushed date of the repository.
- created_date: int value to store the timestamp of the created date of the repository.
- updated_date: int value to store the timestamp of the las updated date of the repository.
- size: int value to store the size of the repository.
- stars: int value to store the number of stars that the repository had.
- forks: int value to store the number of forks ththata the repository had.
- watchers: int value to store the number of wtchers that the repository had.
- language: string value to store the programming language for the repository.
- topics: string to store the list of topics that the repository had.

Go to the [repo table DDL](schemas/repo.sql) file for more detailed information about the table definition.

<details>
<summary>
API JSON response for repository
</summary>

```json
{
   "id":408675469,
   "node_id":"R_kgDOGFvkjQ",
   "name":"pygithub-etl",
   "full_name":"luisjba/pygithub-etl",
   "private":false,
   "owner":{
      "login":"luisjba",
      "id":1441722,
      "node_id":"MDQ6VXNlcjE0NDE3MjI=",
      "avatar_url":"https://avatars.githubusercontent.com/u/1441722?v=4",
      "gravatar_id":"",
      "url":"https://api.github.com/users/luisjba",
      "html_url":"https://github.com/luisjba",
      "followers_url":"https://api.github.com/users/luisjba/followers",
      "following_url":"https://api.github.com/users/luisjba/following{/other_user}",
      "gists_url":"https://api.github.com/users/luisjba/gists{/gist_id}",
      "starred_url":"https://api.github.com/users/luisjba/starred{/owner}{/repo}",
      "subscriptions_url":"https://api.github.com/users/luisjba/subscriptions",
      "organizations_url":"https://api.github.com/users/luisjba/orgs",
      "repos_url":"https://api.github.com/users/luisjba/repos",
      "events_url":"https://api.github.com/users/luisjba/events{/privacy}",
      "received_events_url":"https://api.github.com/users/luisjba/received_events",
      "type":"User",
      "site_admin":false
   },
   "html_url":"https://github.com/luisjba/pygithub-etl",
   "description":"Python library that uses PyGithub library to consume GitHub API authenticated by  token, to Extract Transform and Load the related data into a SQLite database to analyze it.",
   "fork":false,
   "url":"https://api.github.com/repos/luisjba/pygithub-etl",
   "forks_url":"https://api.github.com/repos/luisjba/pygithub-etl/forks",
   "keys_url":"https://api.github.com/repos/luisjba/pygithub-etl/keys{/key_id}",
   "collaborators_url":"https://api.github.com/repos/luisjba/pygithub-etl/collaborators{/collaborator}",
   "teams_url":"https://api.github.com/repos/luisjba/pygithub-etl/teams",
   "hooks_url":"https://api.github.com/repos/luisjba/pygithub-etl/hooks",
   "issue_events_url":"https://api.github.com/repos/luisjba/pygithub-etl/issues/events{/number}",
   "events_url":"https://api.github.com/repos/luisjba/pygithub-etl/events",
   "assignees_url":"https://api.github.com/repos/luisjba/pygithub-etl/assignees{/user}",
   "branches_url":"https://api.github.com/repos/luisjba/pygithub-etl/branches{/branch}",
   "tags_url":"https://api.github.com/repos/luisjba/pygithub-etl/tags",
   "blobs_url":"https://api.github.com/repos/luisjba/pygithub-etl/git/blobs{/sha}",
   "git_tags_url":"https://api.github.com/repos/luisjba/pygithub-etl/git/tags{/sha}",
   "git_refs_url":"https://api.github.com/repos/luisjba/pygithub-etl/git/refs{/sha}",
   "trees_url":"https://api.github.com/repos/luisjba/pygithub-etl/git/trees{/sha}",
   "statuses_url":"https://api.github.com/repos/luisjba/pygithub-etl/statuses/{sha}",
   "languages_url":"https://api.github.com/repos/luisjba/pygithub-etl/languages",
   "stargazers_url":"https://api.github.com/repos/luisjba/pygithub-etl/stargazers",
   "contributors_url":"https://api.github.com/repos/luisjba/pygithub-etl/contributors",
   "subscribers_url":"https://api.github.com/repos/luisjba/pygithub-etl/subscribers",
   "subscription_url":"https://api.github.com/repos/luisjba/pygithub-etl/subscription",
   "commits_url":"https://api.github.com/repos/luisjba/pygithub-etl/commits{/sha}",
   "git_commits_url":"https://api.github.com/repos/luisjba/pygithub-etl/git/commits{/sha}",
   "comments_url":"https://api.github.com/repos/luisjba/pygithub-etl/comments{/number}",
   "issue_comment_url":"https://api.github.com/repos/luisjba/pygithub-etl/issues/comments{/number}",
   "contents_url":"https://api.github.com/repos/luisjba/pygithub-etl/contents/{+path}",
   "compare_url":"https://api.github.com/repos/luisjba/pygithub-etl/compare/{base}...{head}",
   "merges_url":"https://api.github.com/repos/luisjba/pygithub-etl/merges",
   "archive_url":"https://api.github.com/repos/luisjba/pygithub-etl/{archive_format}{/ref}",
   "downloads_url":"https://api.github.com/repos/luisjba/pygithub-etl/downloads",
   "issues_url":"https://api.github.com/repos/luisjba/pygithub-etl/issues{/number}",
   "pulls_url":"https://api.github.com/repos/luisjba/pygithub-etl/pulls{/number}",
   "milestones_url":"https://api.github.com/repos/luisjba/pygithub-etl/milestones{/number}",
   "notifications_url":"https://api.github.com/repos/luisjba/pygithub-etl/notifications{?since,all,participating}",
   "labels_url":"https://api.github.com/repos/luisjba/pygithub-etl/labels{/name}",
   "releases_url":"https://api.github.com/repos/luisjba/pygithub-etl/releases{/id}",
   "deployments_url":"https://api.github.com/repos/luisjba/pygithub-etl/deployments",
   "created_at":"2021-09-21T03:28:01Z",
   "updated_at":"2021-09-21T06:48:00Z",
   "pushed_at":"2021-09-21T06:47:57Z",
   "git_url":"git://github.com/luisjba/pygithub-etl.git",
   "ssh_url":"git@github.com:luisjba/pygithub-etl.git",
   "clone_url":"https://github.com/luisjba/pygithub-etl.git",
   "svn_url":"https://github.com/luisjba/pygithub-etl",
   "homepage":null,
   "size":18,
   "stargazers_count":0,
   "watchers_count":0,
   "language":"Python",
   "has_issues":true,
   "has_projects":true,
   "has_downloads":true,
   "has_wiki":true,
   "has_pages":false,
   "forks_count":0,
   "mirror_url":null,
   "archived":false,
   "disabled":false,
   "open_issues_count":0,
   "license":null,
   "allow_forking":true,
   "forks":0,
   "open_issues":0,
   "watchers":0,
   "default_branch":"master",
   "permissions":{
      "admin":true,
      "maintain":true,
      "push":true,
      "triage":true,
      "pull":true
   },
   "temp_clone_token":"",
   "network_count":0,
   "subscribers_count":1
}
```
</details>

### Branch Schema

Available values:

- id: int value used as primary key for ech branch
- repo_id: int value used as foreing key to the `repo` table.
- name: string value to store the branch name.
- commit_sha: string value to store the sha value.
- pretected: integer value . Value of 0 means unprotected.

<details> 
<summary>
API JSON response for branch
</summary>

```json
{
    "name": "master", 
    "commit": {
        "sha": "4aa88ed5bf3fac036fef0b92f04959311bf4ec0b", 
        "url": "https://api.github.com/repos/luisjba/pygithub-etl/commits/4aa88ed5bf3fac036fef0b92f04959311bf4ec0b"
    }, 
    "protected": false
}
```
</details>

### Commits Schema

Available values:
- id: int value used as primary key for each commit.
- repo_id: int value used as foreing key to the `repo` table.
- commit_sha: string value to store the sha value of the commit.
- commit_message: string value to store the message of the commit.
- commit_author_name: string value to store the author's name of the commit.
- commit_author_email: string value to store the author's email of the commit.
- commit_author_date: int value to store the timestamp of the commit.
- commit_committer_name: string value to store the committer's name of the commit.
- commit_committer_email: string value to store the committer's email of the commit.
- commit_committer_date: int value to store the timestamp of the committer's date.
- author_login: string to store the author's login if author user available.
- author_id: string to store the author's id if author user available.
- author_avatar_url: string to store the author's url if author user available.
- author_type: string to store the author's type if author user available.
- committer_login: string to store the committer's login if committer user available.
- committer_id: string to store the committer's id if autcommitterhor user available.
- committer_avatar_url: string to store the committer's url if committer user available.
- committer_type: string to store the committer's type if committer user available.
- stats_addtions: int value to store the total additions in the commit.
- stats_deletions: int value to store the total deletions in the commit.
- stats_total: int value to store the total additions and deletions in the commit.

<details> 
<summary>
API JSON response for commit
</summary>

```json
{
   "sha":"4aa88ed5bf3fac036fef0b92f04959311bf4ec0b",
   "node_id":"C_kwDOGFvkjdoAKDRhYTg4ZWQ1YmYzZmFjMDM2ZmVmMGI5MmYwNDk1OTMxMWJmNGVjMGI",
   "commit":{
      "author":{
         "name":"Jose Luis Bracamonte Amavizca",
         "email":"luisjba@gmail.com",
         "date":"2021-09-21T07:08:47Z"
      },
      "committer":{
         "name":"Jose Luis Bracamonte Amavizca",
         "email":"luisjba@gmail.com",
         "date":"2021-09-21T07:08:47Z"
      },
      "message":"Repo raw data",
      "tree":{
         "sha":"196fb10515424d389d906dbd6cbb7f86abcc90b2",
         "url":"https://api.github.com/repos/luisjba/pygithub-etl/git/trees/196fb10515424d389d906dbd6cbb7f86abcc90b2"
      },
      "url":"https://api.github.com/repos/luisjba/pygithub-etl/git/commits/4aa88ed5bf3fac036fef0b92f04959311bf4ec0b",
      "comment_count":0,
      "verification":{
         "verified":false,
         "reason":"unsigned",
         "signature":null,
         "payload":null
      }
   },
   "url":"https://api.github.com/repos/luisjba/pygithub-etl/commits/4aa88ed5bf3fac036fef0b92f04959311bf4ec0b",
   "html_url":"https://github.com/luisjba/pygithub-etl/commit/4aa88ed5bf3fac036fef0b92f04959311bf4ec0b",
   "comments_url":"https://api.github.com/repos/luisjba/pygithub-etl/commits/4aa88ed5bf3fac036fef0b92f04959311bf4ec0b/comments",
   "author":null,
   "committer":null,
   "parents":[
      {
         "sha":"34215d1a6a53cec3ae4b6d003df9fbe53e1f696f",
         "url":"https://api.github.com/repos/luisjba/pygithub-etl/commits/34215d1a6a53cec3ae4b6d003df9fbe53e1f696f",
         "html_url":"https://github.com/luisjba/pygithub-etl/commit/34215d1a6a53cec3ae4b6d003df9fbe53e1f696f"
      }
   ],
   "stats":{
      "total":112,
      "additions":110,
      "deletions":2
   },
   "files":[
      {
         "sha":"293ac52f690693f268026fa0256cb870b233dfff",
         "filename":"README.md",
         "status":"modified",
         "additions":110,
         "deletions":2,
         "changes":112,
         "blob_url":"https://github.com/luisjba/pygithub-etl/blob/4aa88ed5bf3fac036fef0b92f04959311bf4ec0b/README.md",
         "raw_url":"https://github.com/luisjba/pygithub-etl/raw/4aa88ed5bf3fac036fef0b92f04959311bf4ec0b/README.md",
         "contents_url":"https://api.github.com/repos/luisjba/pygithub-etl/contents/README.md?ref=4aa88ed5bf3fac036fef0b92f04959311bf4ec0b",
         "patch":"@@ -1,4 +1,4 @@\n-# GitHubETL library\n+# GitHubETL Library\n \n GitHubETL is a Python library that use the [PyGithub library](https://github.com/PyGithub/PyGithub/) to consume the [Github API v3](http://developer.github.com/v3)\n to extrac the data from any [Github](http://github.com) repository, transform and load the data into a SqlLite database (we use the [SQLite3 Python library](https://docs.python.org/3/library/sqlite3.html) to manipulate our database).\n@@ -94,6 +94,7 @@ $ python main.py sync XXXXXXXXXXXXXX  my_user/my_repo --db ~/Project/my_repo.db\n \n To use as library, wirte your implementation in the current clonned project or copy the `etl` and `schemas` into your desired project. We jave to import the  `GithubETL` class.\n ```python\n+import etl\n from etl import GithubETL\n ```\n \n@@ -117,6 +118,7 @@ If all is ok (the token is valid and the database connection was successfull), y\n #### All toguether\n \n ```python\n+import etl\n from etl import GithubETL\n \n token = \"XXXXXXXXX\"\n@@ -139,5 +141,111 @@ getl.sync_commits(true)\n \n ## Schemas\n \n-\n+A ER model (Entity-relationship model) was desingned to store all the related data of a Github repository. We have 4 schemas:\n+\n+### Repo Schema\n+\n+The repo schema is used to fit the data that the GitHub API provide as response for a requested repository.\n+\n+```json\n+{'id': 408675469,\n+ 'node_id': 'R_kgDOGFvkjQ',\n+ 'name': 'pygithub-etl',\n+ 'full_name': 'luisjba/pygithub-etl',\n+ 'private': False,\n+ 'owner': {'login': 'luisjba',\n+  'id': 1441722,\n+  'node_id': 'MDQ6VXNlcjE0NDE3MjI=',\n+  'avatar_url': 'https://avatars.githubusercontent.com/u/1441722?v=4',\n+  'gravatar_id': '',\n+  'url': 'https://api.github.com/users/luisjba',\n+  'html_url': 'https://github.com/luisjba',\n+  'followers_url': 'https://api.github.com/users/luisjba/followers',\n+  'following_url': 'https://api.github.com/users/luisjba/following{/other_user}',\n+  'gists_url': 'https://api.github.com/users/luisjba/gists{/gist_id}',\n+  'starred_url': 'https://api.github.com/users/luisjba/starred{/owner}{/repo}',\n+  'subscriptions_url': 'https://api.github.com/users/luisjba/subscriptions',\n+  'organizations_url': 'https://api.github.com/users/luisjba/orgs',\n+  'repos_url': 'https://api.github.com/users/luisjba/repos',\n+  'events_url': 'https://api.github.com/users/luisjba/events{/privacy}',\n+  'received_events_url': 'https://api.github.com/users/luisjba/received_events',\n+  'type': 'User',\n+  'site_admin': False},\n+ 'html_url': 'https://github.com/luisjba/pygithub-etl',\n+ 'description': 'Python library that uses PyGithub library to consume GitHub API authenticated by  token, to Extract Transform and Load the related data into a SQLite database to analyze it.',\n+ 'fork': False,\n+ 'url': 'https://api.github.com/repos/luisjba/pygithub-etl',\n+ 'forks_url': 'https://api.github.com/repos/luisjba/pygithub-etl/forks',\n+ 'keys_url': 'https://api.github.com/repos/luisjba/pygithub-etl/keys{/key_id}',\n+ 'collaborators_url': 'https://api.github.com/repos/luisjba/pygithub-etl/collaborators{/collaborator}',\n+ 'teams_url': 'https://api.github.com/repos/luisjba/pygithub-etl/teams',\n+ 'hooks_url': 'https://api.github.com/repos/luisjba/pygithub-etl/hooks',\n+ 'issue_events_url': 'https://api.github.com/repos/luisjba/pygithub-etl/issues/events{/number}',\n+ 'events_url': 'https://api.github.com/repos/luisjba/pygithub-etl/events',\n+ 'assignees_url': 'https://api.github.com/repos/luisjba/pygithub-etl/assignees{/user}',\n+ 'branches_url': 'https://api.github.com/repos/luisjba/pygithub-etl/branches{/branch}',\n+ 'tags_url': 'https://api.github.com/repos/luisjba/pygithub-etl/tags',\n+ 'blobs_url': 'https://api.github.com/repos/luisjba/pygithub-etl/git/blobs{/sha}',\n+ 'git_tags_url': 'https://api.github.com/repos/luisjba/pygithub-etl/git/tags{/sha}',\n+ 'git_refs_url': 'https://api.github.com/repos/luisjba/pygithub-etl/git/refs{/sha}',\n+ 'trees_url': 'https://api.github.com/repos/luisjba/pygithub-etl/git/trees{/sha}',\n+ 'statuses_url': 'https://api.github.com/repos/luisjba/pygithub-etl/statuses/{sha}',\n+ 'languages_url': 'https://api.github.com/repos/luisjba/pygithub-etl/languages',\n+ 'stargazers_url': 'https://api.github.com/repos/luisjba/pygithub-etl/stargazers',\n+ 'contributors_url': 'https://api.github.com/repos/luisjba/pygithub-etl/contributors',\n+ 'subscribers_url': 'https://api.github.com/repos/luisjba/pygithub-etl/subscribers',\n+ 'subscription_url': 'https://api.github.com/repos/luisjba/pygithub-etl/subscription',\n+ 'commits_url': 'https://api.github.com/repos/luisjba/pygithub-etl/commits{/sha}',\n+ 'git_commits_url': 'https://api.github.com/repos/luisjba/pygithub-etl/git/commits{/sha}',\n+ 'comments_url': 'https://api.github.com/repos/luisjba/pygithub-etl/comments{/number}',\n+ 'issue_comment_url': 'https://api.github.com/repos/luisjba/pygithub-etl/issues/comments{/number}',\n+ 'contents_url': 'https://api.github.com/repos/luisjba/pygithub-etl/contents/{+path}',\n+ 'compare_url': 'https://api.github.com/repos/luisjba/pygithub-etl/compare/{base}...{head}',\n+ 'merges_url': 'https://api.github.com/repos/luisjba/pygithub-etl/merges',\n+ 'archive_url': 'https://api.github.com/repos/luisjba/pygithub-etl/{archive_format}{/ref}',\n+ 'downloads_url': 'https://api.github.com/repos/luisjba/pygithub-etl/downloads',\n+ 'issues_url': 'https://api.github.com/repos/luisjba/pygithub-etl/issues{/number}',\n+ 'pulls_url': 'https://api.github.com/repos/luisjba/pygithub-etl/pulls{/number}',\n+ 'milestones_url': 'https://api.github.com/repos/luisjba/pygithub-etl/milestones{/number}',\n+ 'notifications_url': 'https://api.github.com/repos/luisjba/pygithub-etl/notifications{?since,all,participating}',\n+ 'labels_url': 'https://api.github.com/repos/luisjba/pygithub-etl/labels{/name}',\n+ 'releases_url': 'https://api.github.com/repos/luisjba/pygithub-etl/releases{/id}',\n+ 'deployments_url': 'https://api.github.com/repos/luisjba/pygithub-etl/deployments',\n+ 'created_at': '2021-09-21T03:28:01Z',\n+ 'updated_at': '2021-09-21T06:48:00Z',\n+ 'pushed_at': '2021-09-21T06:47:57Z',\n+ 'git_url': 'git://github.com/luisjba/pygithub-etl.git',\n+ 'ssh_url': 'git@github.com:luisjba/pygithub-etl.git',\n+ 'clone_url': 'https://github.com/luisjba/pygithub-etl.git',\n+ 'svn_url': 'https://github.com/luisjba/pygithub-etl',\n+ 'homepage': None,\n+ 'size': 18,\n+ 'stargazers_count': 0,\n+ 'watchers_count': 0,\n+ 'language': 'Python',\n+ 'has_issues': True,\n+ 'has_projects': True,\n+ 'has_downloads': True,\n+ 'has_wiki': True,\n+ 'has_pages': False,\n+ 'forks_count': 0,\n+ 'mirror_url': None,\n+ 'archived': False,\n+ 'disabled': False,\n+ 'open_issues_count': 0,\n+ 'license': None,\n+ 'allow_forking': True,\n+ 'forks': 0,\n+ 'open_issues': 0,\n+ 'watchers': 0,\n+ 'default_branch': 'master',\n+ 'permissions': {'admin': True,\n+  'maintain': True,\n+  'push': True,\n+  'triage': True,\n+  'pull': True},\n+ 'temp_clone_token': '',\n+ 'network_count': 0,\n+ 'subscribers_count': 1}\n+```\n "
      }
   ]
}
```
<details> 
<summary>
API JSON response for commit
</summary>

### Commit File Schema

Available values:
- id: int value used as primary key for each commit file.
- commit_id: int value used as foreing key to the `commits` table.
- repo_id: int value used as foreing key to the `repo` table.
- file_name: string value to store the file name in the commit.
- additions: int value to store the number of additions in the file.
- deletions: int value to store the number of deletions in the file.
- changes: int value to store the number of additions and deletions in the file.
- status: string value ti stire the file status.


<details> 
<summary>
API JSON response for files section in the commit
</summary>

```json
{
   "files":[
      {
         "sha":"293ac52f690693f268026fa0256cb870b233dfff",
         "filename":"README.md",
         "status":"modified",
         "additions":110,
         "deletions":2,
         "changes":112,
         "blob_url":"https://github.com/luisjba/pygithub-etl/blob/4aa88ed5bf3fac036fef0b92f04959311bf4ec0b/README.md",
         "raw_url":"https://github.com/luisjba/pygithub-etl/raw/4aa88ed5bf3fac036fef0b92f04959311bf4ec0b/README.md",
         "contents_url":"https://api.github.com/repos/luisjba/pygithub-etl/contents/README.md?ref=4aa88ed5bf3fac036fef0b92f04959311bf4ec0b",
         "patch":"@@ -1,4 +1,4 @@\n-# GitHubETL library\n+# GitHubETL Library\n \n GitHubETL is a Python library that use the [PyGithub library](https://github.com/PyGithub/PyGithub/) to consume the [Github API v3](http://developer.github.com/v3)\n to extrac the data from any [Github](http://github.com) repository, transform and load the data into a SqlLite database (we use the [SQLite3 Python library](https://docs.python.org/3/library/sqlite3.html) to manipulate our database).\n@@ -94,6 +94,7 @@ $ python main.py sync XXXXXXXXXXXXXX  my_user/my_repo --db ~/Project/my_repo.db\n \n To use as library, wirte your implementation in the current clonned project or copy the `etl` and `schemas` into your desired project. We jave to import the  `GithubETL` class.\n ```python\n+import etl\n from etl import GithubETL\n ```\n \n@@ -117,6 +118,7 @@ If all is ok (the token is valid and the database connection was successfull), y\n #### All toguether\n \n ```python\n+import etl\n from etl import GithubETL\n \n token = \"XXXXXXXXX\"\n@@ -139,5 +141,111 @@ getl.sync_commits(true)\n \n ## Schemas\n \n-\n+A ER model (Entity-relationship model) was desingned to store all the related data of a Github repository. We have 4 schemas:\n+\n+### Repo Schema\n+\n+The repo schema is used to fit the data that the GitHub API provide as response for a requested repository.\n+\n+```json\n+{'id': 408675469,\n+ 'node_id': 'R_kgDOGFvkjQ',\n+ 'name': 'pygithub-etl',\n+ 'full_name': 'luisjba/pygithub-etl',\n+ 'private': False,\n+ 'owner': {'login': 'luisjba',\n+  'id': 1441722,\n+  'node_id': 'MDQ6VXNlcjE0NDE3MjI=',\n+  'avatar_url': 'https://avatars.githubusercontent.com/u/1441722?v=4',\n+  'gravatar_id': '',\n+  'url': 'https://api.github.com/users/luisjba',\n+  'html_url': 'https://github.com/luisjba',\n+  'followers_url': 'https://api.github.com/users/luisjba/followers',\n+  'following_url': 'https://api.github.com/users/luisjba/following{/other_user}',\n+  'gists_url': 'https://api.github.com/users/luisjba/gists{/gist_id}',\n+  'starred_url': 'https://api.github.com/users/luisjba/starred{/owner}{/repo}',\n+  'subscriptions_url': 'https://api.github.com/users/luisjba/subscriptions',\n+  'organizations_url': 'https://api.github.com/users/luisjba/orgs',\n+  'repos_url': 'https://api.github.com/users/luisjba/repos',\n+  'events_url': 'https://api.github.com/users/luisjba/events{/privacy}',\n+  'received_events_url': 'https://api.github.com/users/luisjba/received_events',\n+  'type': 'User',\n+  'site_admin': False},\n+ 'html_url': 'https://github.com/luisjba/pygithub-etl',\n+ 'description': 'Python library that uses PyGithub library to consume GitHub API authenticated by  token, to Extract Transform and Load the related data into a SQLite database to analyze it.',\n+ 'fork': False,\n+ 'url': 'https://api.github.com/repos/luisjba/pygithub-etl',\n+ 'forks_url': 'https://api.github.com/repos/luisjba/pygithub-etl/forks',\n+ 'keys_url': 'https://api.github.com/repos/luisjba/pygithub-etl/keys{/key_id}',\n+ 'collaborators_url': 'https://api.github.com/repos/luisjba/pygithub-etl/collaborators{/collaborator}',\n+ 'teams_url': 'https://api.github.com/repos/luisjba/pygithub-etl/teams',\n+ 'hooks_url': 'https://api.github.com/repos/luisjba/pygithub-etl/hooks',\n+ 'issue_events_url': 'https://api.github.com/repos/luisjba/pygithub-etl/issues/events{/number}',\n+ 'events_url': 'https://api.github.com/repos/luisjba/pygithub-etl/events',\n+ 'assignees_url': 'https://api.github.com/repos/luisjba/pygithub-etl/assignees{/user}',\n+ 'branches_url': 'https://api.github.com/repos/luisjba/pygithub-etl/branches{/branch}',\n+ 'tags_url': 'https://api.github.com/repos/luisjba/pygithub-etl/tags',\n+ 'blobs_url': 'https://api.github.com/repos/luisjba/pygithub-etl/git/blobs{/sha}',\n+ 'git_tags_url': 'https://api.github.com/repos/luisjba/pygithub-etl/git/tags{/sha}',\n+ 'git_refs_url': 'https://api.github.com/repos/luisjba/pygithub-etl/git/refs{/sha}',\n+ 'trees_url': 'https://api.github.com/repos/luisjba/pygithub-etl/git/trees{/sha}',\n+ 'statuses_url': 'https://api.github.com/repos/luisjba/pygithub-etl/statuses/{sha}',\n+ 'languages_url': 'https://api.github.com/repos/luisjba/pygithub-etl/languages',\n+ 'stargazers_url': 'https://api.github.com/repos/luisjba/pygithub-etl/stargazers',\n+ 'contributors_url': 'https://api.github.com/repos/luisjba/pygithub-etl/contributors',\n+ 'subscribers_url': 'https://api.github.com/repos/luisjba/pygithub-etl/subscribers',\n+ 'subscription_url': 'https://api.github.com/repos/luisjba/pygithub-etl/subscription',\n+ 'commits_url': 'https://api.github.com/repos/luisjba/pygithub-etl/commits{/sha}',\n+ 'git_commits_url': 'https://api.github.com/repos/luisjba/pygithub-etl/git/commits{/sha}',\n+ 'comments_url': 'https://api.github.com/repos/luisjba/pygithub-etl/comments{/number}',\n+ 'issue_comment_url': 'https://api.github.com/repos/luisjba/pygithub-etl/issues/comments{/number}',\n+ 'contents_url': 'https://api.github.com/repos/luisjba/pygithub-etl/contents/{+path}',\n+ 'compare_url': 'https://api.github.com/repos/luisjba/pygithub-etl/compare/{base}...{head}',\n+ 'merges_url': 'https://api.github.com/repos/luisjba/pygithub-etl/merges',\n+ 'archive_url': 'https://api.github.com/repos/luisjba/pygithub-etl/{archive_format}{/ref}',\n+ 'downloads_url': 'https://api.github.com/repos/luisjba/pygithub-etl/downloads',\n+ 'issues_url': 'https://api.github.com/repos/luisjba/pygithub-etl/issues{/number}',\n+ 'pulls_url': 'https://api.github.com/repos/luisjba/pygithub-etl/pulls{/number}',\n+ 'milestones_url': 'https://api.github.com/repos/luisjba/pygithub-etl/milestones{/number}',\n+ 'notifications_url': 'https://api.github.com/repos/luisjba/pygithub-etl/notifications{?since,all,participating}',\n+ 'labels_url': 'https://api.github.com/repos/luisjba/pygithub-etl/labels{/name}',\n+ 'releases_url': 'https://api.github.com/repos/luisjba/pygithub-etl/releases{/id}',\n+ 'deployments_url': 'https://api.github.com/repos/luisjba/pygithub-etl/deployments',\n+ 'created_at': '2021-09-21T03:28:01Z',\n+ 'updated_at': '2021-09-21T06:48:00Z',\n+ 'pushed_at': '2021-09-21T06:47:57Z',\n+ 'git_url': 'git://github.com/luisjba/pygithub-etl.git',\n+ 'ssh_url': 'git@github.com:luisjba/pygithub-etl.git',\n+ 'clone_url': 'https://github.com/luisjba/pygithub-etl.git',\n+ 'svn_url': 'https://github.com/luisjba/pygithub-etl',\n+ 'homepage': None,\n+ 'size': 18,\n+ 'stargazers_count': 0,\n+ 'watchers_count': 0,\n+ 'language': 'Python',\n+ 'has_issues': True,\n+ 'has_projects': True,\n+ 'has_downloads': True,\n+ 'has_wiki': True,\n+ 'has_pages': False,\n+ 'forks_count': 0,\n+ 'mirror_url': None,\n+ 'archived': False,\n+ 'disabled': False,\n+ 'open_issues_count': 0,\n+ 'license': None,\n+ 'allow_forking': True,\n+ 'forks': 0,\n+ 'open_issues': 0,\n+ 'watchers': 0,\n+ 'default_branch': 'master',\n+ 'permissions': {'admin': True,\n+  'maintain': True,\n+  'push': True,\n+  'triage': True,\n+  'pull': True},\n+ 'temp_clone_token': '',\n+ 'network_count': 0,\n+ 'subscribers_count': 1}\n+```\n "
      }
   ]
}
```

</summary>

