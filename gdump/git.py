#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GithubETL class definition 
@datecreated: 2021-09-16
@lastupdated: 2021-09-20
@author: Jose Luis Bracamonte Amavizca
"""
# Meta informations.
__author__ = 'Jose Luis Bracamonte Amavizca'
__version__ = '0.1.2'
__maintainer__ = 'Jose Luis Bracamonte Amavizca'
__email__ = 'me@luisjba.com'
__status__ = 'Development'

import os, sys
from sqlite3.dbapi2 import Row
from datetime import datetime
from posixpath import join
from github import Github, GithubException, Commit
from github.NamedUser import NamedUser
from github.Repository import Repository
from .db import Connection
from .utils import print_fail, print_okgreen, print_okblue, print_warning

class GithubETL():
    def __init__(self, token: str, repo_fullname: str, db_file: str = "data/data.db", base_path: str = "", schemas_dir="schemas") -> None:
        self._date_format:str = "%Y/%m/%d %H:%M:%S"
        self.g: Github = Github(token)
        try:
            self.repo:Repository = self.g.get_repo(repo_fullname)
        except GithubException as e:
            if e.status == 401:
                print_fail("The token is invalid, please privide a new valid token")
            elif e.status == 404:
                print_fail("The repository '{}' was not found, try with with a diferent repository name.".format(repo_fullname))
            else:
                print_fail("GitHub error: {}".format(e))
            sys.exit(1)
        self.db_file:str = db_file
        self.base_path:str = base_path
        self.db_conn:Connection = Connection(self.base_path, db_file)
        print_okgreen("SQLite connected to:{}".format(self.db_conn.db_file))
        self._init_db(schemas_dir)

    def _init_db(self, schemas_dir="schemas"):
        """Checks the db connection and initialize the database"""
        schemas_dir = os.path.join(self.base_path, schemas_dir) if not schemas_dir[0] == "/" else schemas_dir
        if not os.path.isdir(schemas_dir):
            print_fail("'{}' is an invalid directory. Provide a valid directory to find the schemas for SQLite tables".format(schemas_dir))
            sys.exit(1)
        schemas:list = ['repo', 'branch', 'commits', 'commit_file']
        schame_dict = {schema:"{}/{}.sql".format(schemas_dir, schema) for schema in schemas}
        if self.db_conn is not None and len(schame_dict) > 0:
            for t,t_file  in schame_dict.items():
                if not os.path.isfile(t_file):
                    print_fail("Schema file '{}' does not exists".format(t_file))
                    sys.exit(1)
                    continue
                result = self.db_conn.execute_query_fetch('sqlite_master',['name'],{'type':'table', 'name':t})
                if len(result) > 0 : # The table already axists in the database
                    continue 
                with open(t_file, 'r') as file:
                    if self.db_conn.create_table(file.read()):
                        print_okgreen("Created the table {} into SQLite db: '{}'".format(t, self.db_conn.db_file))

    def sync_repo(self):
        """This function perform the repo syncronization into the SQLite db"""
        repo_data = {
            "name": self.repo.name,
            "owner": self.repo.owner.login,
            "fullname": self.repo.full_name,
            "description": self.repo.description,
            "url": self.repo.url,
            "pushed_date": int(self.repo.pushed_at.timestamp()),
            "created_date": int(self.repo.created_at.timestamp()),
            "updated_date": int(self.repo.updated_at.timestamp()),
            "size": self.repo.size,
            "stars": self.repo.stargazers_count,
            "forks": self.repo.forks_count,
            "watchers": self.repo.watchers_count,
            "language": self.repo.language,
            "topics": ",".join(self.repo.get_topics()),
        }
        db_repo = self.db_conn.get_repo(self.repo.full_name)
        if db_repo is None:
            db_repo = self.db_conn.add_repo(repo_data)
            if db_repo is None:
                print_fail("Failed insert the new repository '{}' into SQLite db".format(self.repo.full_name))
                sys.exit(1)
            else:
                print_okgreen("Respository '{}'  succesfully inserted into SQLite db".format(self.repo.full_name))
        else:
            repo_data["id"] = db_repo["id"]
            if db_repo["pushed_date"] < repo_data["pushed_date"]:
                print_okblue("Trying to update repo '{}' from {} to {} ".format(
                    self.repo.full_name,
                    datetime.fromtimestamp(db_repo["pushed_date"]).strftime(self._date_format),
                    datetime.fromtimestamp(repo_data["pushed_date"]).strftime(self._date_format)
                ))
                db_repo = self.db_conn.update_repo(repo_data)
                print_okgreen("Respository '{}' succesfully sincronized into SQLite db.".format(self.repo.full_name))
            else:
                print_okblue("Respository '{}' is up to date.".format(self.repo.full_name))

    def sync_branches(self):
        """Syncornize the Branches of the repository"""
        db_repo = self.db_conn.get_repo(self.repo.full_name)
        if db_repo is None:
            print_fail("The repository '{}' dos not exists in the SQLite db. Try first 'sync_repo' function".format(self.repo.full_name))
            sys.exit(1)
        for branch in self.repo.get_branches():
            branch_data = {
                "repo_id": db_repo["id"],
                "name": branch.name,
                "commit_sha": branch.commit.sha,
                "protected": 1 if branch.protected else 0,
            }
            db_branch = self.db_conn.get_branch(db_repo["id"], branch.name)
            if db_branch is None:
                db_branch = self.db_conn.add_branch(db_repo["id"], branch_data)
                if db_branch is None:
                    print_fail("Failed insert the branch '{}:{}' into SQLite db".format(self.repo.full_name, branch.name))
                else:
                    print_okgreen("Branch '{}:{}' succesfully inserted into SQLite db".format(self.repo.full_name, branch.name))
            else:
                branch_data["id"] = db_branch["id"]
                if not (db_branch["commit_sha"] == branch_data["commit_sha"] ) :
                    print_okblue("Trying to update branch '{}:{}' from commit  {} to {} ".format(
                            self.repo.full_name, branch.name, db_branch["commit_sha"], branch_data["commit_sha"]
                        ))
                    db_branch = self.db_conn.update_branch(branch_data)
                    print_okgreen("Branch '{}:{}' succesfully sincronized into SQLite db.".format(self.repo.full_name, branch.name))
                else:
                    print_okblue("Branch '{}:{}' is up to date.".format(self.repo.full_name, branch.name))

    def _get_commit_data(self,repo_id:int, commit:Commit.Commit ) -> dict:
        """Extract the data form a Commit Object"""
        try:
            data =  {
                "repo_id": repo_id,
                "commit_sha": commit.sha,
                "commit_message": commit.commit.message,
                "commit_author_name": commit.commit.author.name,
                "commit_author_email": commit.commit.author.email,
                "commit_author_date": int(commit.commit.author.date.timestamp()),
                "commit_committer_name": commit.commit.committer.name,
                "commit_committer_email": commit.commit.committer.email,
                "commit_committer_date": int(commit.commit.committer.date.timestamp()),
                "stats_addtions": commit.stats.additions,
                "stats_deletions": commit.stats.deletions,
                "stats_total": commit.stats.total
            }
            self._append_user_data(data, commit.author, "author")
            self._append_user_data(data, commit.committer, "committer")
            return data
        except GithubException as e:
             print_fail("GitHub error: {}".format(e))
        except AttributeError as e:
            print_fail("Attribute error: {}".format(e))
        print_warning("Commit data:".format(commit.raw_data))
        return None

    def _append_user_data(self, data:dict, user:NamedUser, prefix_key:str):
        """Append the user dara to a data dict"""
        if user is not None:
            data["{}_id".format(prefix_key)] = user.id
            data["{}_login".format(prefix_key)] = user.login
            data["{}_avatar_url".format(prefix_key)] = user.avatar_url
            data["{}_type".format(prefix_key)] = user.type

    def sync_commits(self, force_update=False):
        """Syncornize the Commits of a repository"""
        db_repo = self.db_conn.get_repo(self.repo.full_name)
        if db_repo is None:
            print_fail("The repository '{}' dos not exists in the SQLite db. Try first 'sync_repo' function".format(self.repo.full_name))
            sys.exit(1)
        for commit in self.repo.get_commits():
            commit_data = self._get_commit_data(db_repo["id"], commit)
            if commit_data is None:
                print_fail("Something went worng tryin t0 fetch/parse '{}:{}'".format(self.repo.full_name, commit.sha))
                continue
            db_commit = self.db_conn.get_commit(db_repo["id"], commit.sha)
            if db_commit is None:
                db_commit = self.db_conn.add_commit(db_repo["id"], commit_data)
                if db_commit is None:
                    print_fail("Failed insert the commit '{}:{}' into SQLite db".format(self.repo.full_name, commit.sha))
                else:
                    print_okgreen("Commit '{}:{}' succesfully inserted into SQLite db".format(self.repo.full_name, commit.sha))
            if db_commit is not None:
                if force_update:
                    print_okblue("Trying to update commit '{}:{}'".format(
                            self.repo.full_name, commit.sha, db_commit["commit_sha"], commit_data["commit_sha"]
                        ))
                    db_commit = self.db_conn.update_commit(commit_data)
                    print_okgreen("Commit '{}:{}' succesfully sincronized into SQLite db.".format(self.repo.full_name, commit.sha))
                self._sync_commit_files(commit, db_commit)

    def _sync_commit_files(self, commit:Commit.Commit, db_commit:Row):
        """Syncronize the files related with the commit"""
        for file in commit.files:
            commit_file_data = {
                "commit_id": db_commit["id"],
                "repo_id": db_commit["repo_id"],
                "file_name": file.filename,
                "addtions": file.additions,
                "deletions": file.deletions,
                "changes": file.changes,
                "status": file.status
            }
            db_commit_file = self.db_conn.get_commit_file(db_commit["id"], file.filename)
            if db_commit_file is None:
                db_commit_file = self.db_conn.add_commit_file(db_commit["id"], commit_file_data)
                if db_commit_file is None:
                    print_fail("\tFailed insert the commit_file '{}:{} {}' into SQLite db".format(self.repo.full_name, commit.sha, file.filename))
                else:
                    print_okgreen("\tFile '{}:{} {}' succesfully inserted into SQLite db".format(self.repo.full_name, commit.sha, file.filename))

    

