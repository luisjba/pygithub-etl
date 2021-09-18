#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitDump class definition 
@datecreated: 2021-09-16
@lastupdated: 2021-09-17
@author: Jose Luis Bracamonte Amavizca
"""
# Meta informations.
__author__ = 'Jose Luis Bracamonte Amavizca'
__version__ = '0.0.1'
__maintainer__ = 'Jose Luis Bracamonte Amavizca'
__email__ = 'me@luisjba.com'
__status__ = 'Development'

import os, sys
from posixpath import join
from github import Github, GithubException
from github.Repository import Repository
from .db import Connection
from .utils import print_fail, print_okgreen

class GitDump():
    def __init__(self, token: str, repo_fullname: str, db_file: str = "data/data.db", base_path: str = "", schemas_dir="schemas") -> None:
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
        schemas:list = ['repo']
        schame_dict = {schema:"{}/{}.sql".format(schemas_dir, schema) for schema in schemas}
        if self.db_conn is not None and len(schame_dict) > 0:
            for t,t_file  in schame_dict.items():
                if not os.path.isfile(t_file):
                    print_fail("Schema file '{}' does not exists".format(t_file))
                    continue
                result = self.db_conn.execute_query_fetch('sqlite_master',['name'],{'type':'table', 'name':t})
                if len(result) > 0 : # The table already axists in the database
                    continue 
                with open(t_file, 'r') as file:
                    if self.db_conn.create_table(file.read()):
                        print_okgreen("Created the table {} into SQLite db: '{}'".format(t, self.db_conn.db_file))

    

