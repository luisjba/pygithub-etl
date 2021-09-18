#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLite Database layer  
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

from genericpath import isdir
import sqlite3
from sqlite3 import Error, Row
import os, sys
from .utils import print_fail, print_okgreen, print_warning

class Connection():
    def __init__(self, base_path:str, db_file:str):
        super().__init__()
        self.base_path:str = base_path
        self.db_file = os.path.join(self.base_path, db_file) if not db_file[0] == "/" else db_file
        if not os.path.isfile(self.db_file):
            make_dir = os.path.split(self.db_file)[0]
            os.makedirs(make_dir, exist_ok=True)
            print_okgreen("Created the directory for SQLlite database: {}".format(make_dir))
        try:
           self.db_conn:sqlite3.Connection = sqlite3.connect(self.db_file)
        except Error as e:
            self.db_conn:sqlite3.Connection = None
            print_fail("Error Connecting to SQLLite DB: {}".format(self.db_file))
            sys.exit(1)

    def execute_query_nr(self, query:str) -> bool:
        """Execute a query statement into the db
        :param query: the string query statement
        :return: true if no error occurs
        """
        try:
            self.db_conn.cursor().execute(query)
        except Error as e:
            print_fail("SQLite Exucute Error:{}".format(e))
            return False
        return True

    def execute_query_insert(self,table:str, values_dict:dict, columns_timestamp=["date_created", "last_updated"]) -> int:
        """Insert into deb
        :param table: the table name
        :param columns: the list of column names
        :param values: the list of values to insert
        :return: retiurn the las row id inserted
        """
        columns = list(values_dict.keys())
        values_stmt = ["?"]*len(columns) + ["strftime('%s', 'now')"]*len(columns_timestamp)
        query = '''INSERT INTO {table}({columns})
            VALUES({values});'''.format(
                table=table, 
                columns=",".join(columns + columns_timestamp), 
                values=",".join(values_stmt)
            )
        values = [values_dict[k] for k in columns]
        try:
            # print_warning(query)
            # print_warning(values)
            cursor:sqlite3.Cursor = self.db_conn.cursor().execute(query, values)
            self.db_conn.commit()
            return cursor.lastrowid
        except Error as e:
            print_fail("SQLite Execute Insert Error:{}".format(e))
        return 0

    def execute_query_update(self,table:str, row:Row, keys:list=["id"], columns_timestamp:list=["last_updated"]) -> int:
        """Insert into deb
        :param table: the table name
        :param columns: the list of column names
        :param values: the list of values to update
        :return: true if updated
        """
        exluded_cols = keys + columns_timestamp + ["date_created"]
        columns = [k for k,v in row.items() if k not in exluded_cols]
        values_stmt = ["{} = ?".format(v) for v in columns] \
            + ["{} = strftime('%s', 'now')".format(c) for c in columns_timestamp]
        query = '''UPDATE {table} SET {values}
            WHERE {condition};'''.format(
                table=table, 
                values=",".join(values_stmt),
                condition=" AND ".join(["{} = ?".format(k) for k in keys])
            )
        values = [row[k] for k in (columns + keys)]
        try:
            self.db_conn.cursor().execute(query, values)
            self.db_conn.commit()
            return True
        except Error as e:
            print_fail("SQLite Execute Update Error:{} Query:{}".format(e, query))
        return False
    
    def execute_query_delete(self, table:str, condition_dict:dict={}) -> int:
        """Delete data from db table"""
        if condition_dict is None or type(condition_dict) is not dict or len(condition_dict) == 0:
            return 0
        condition_columns = list(condition_dict.keys())
        query = '''DELETE FROM {table} WHERE {condition};'''.format(
                table=table,
                condition=" AND ".join(["{} = ?".format(c) for c in condition_columns])
            )
        values = [condition_dict[k] for k in condition_columns]
        try:
            cursor:sqlite3.Cursor = self.db_conn.cursor()
            cursor.row_factory = Row
            return int(cursor.execute(query, values).rowcount)
        except Error as e:
            print_fail("SQLite Execute Update Error:{}".format(e))
        return 0

    def execute_query_fetch(self, table:str, columns:list=['*'], condition_dict:dict={}, order:dict={}) -> list:
        """Query data form the DB
        :param table: the table name
        :param columns: the list of column names
        :param condition_dict: dictionaty with column and value 
        :return: list of result rows
        """
        if len(condition_dict) == 0:
            condition_dict[1] = 1
        condition_columns = list(condition_dict.keys())
        order_by = ""
        if len(order) > 0:
            order_by = "ORDER BY {}".format(",".join(["{} {}".format(k, "ASC" if order[k].lower().startswith("asc") else "DESC") for k in order.keys()]))
        query = '''SELECT {columns} FROM {table} WHERE {condition} {order_by};'''.format(
                table=table, 
                columns=",".join(columns),
                condition=" AND ".join(["{} = ?".format(c) for c in condition_columns]),
                order_by = order_by
            )
        values = [condition_dict[k] for k in condition_columns]
        try:
            cursor:sqlite3.Cursor = self.db_conn.cursor()
            cursor.row_factory = Row
            cursor.execute(query, values)
            return cursor.fetchall()
        except Error as e:
            print_fail("SQLite Execute Select Error:{} Query:{}".format(e, query))
        return []

    def add_tables(self, ddl_schemas:dict):
        """Create the table based on the ddl_schemas parameter. The
        key of each item correspond to the table name and its value is the table definition.
        A suggested table definition is:   
        'CREATE TABLE IF NOT EXISTS {table_name}
        ( 
            {col_name} {type} [{constrains}]
            .
            . 
            
        );'
        :paramd ddl_schemas: A dictionary with table name and table definition.
        """
        for t,dd_table  in ddl_schemas.items():
                if self.create_table(dd_table):
                    print("Created the DB {}".format(t))

    def create_table(self, create_table_statement:str) -> bool:
        """Create a table from a statement
        :param create_table_statement: The string create statement
        :return: true if no error occurs
        """
        return self.execute_query_nr(create_table_statement)

    def get_repo(self, fullname:str, pk_column:str="fullname"):
        """Get the repository by fullname"""
        repos = self.execute_query_fetch("repo", condition_dict={pk_column:fullname})
        return repos[0] if len(repos) > 0 else None

    def add_repo(self, repo_data:dict) -> Row:
        """Store  new repo into the DB"""
        self.execute_query_insert("repo",repo_data, columns_timestamp=[])
        return self.get_repo(repo_data["fullname"])
    
    def get_or_create_repo(self, repo_data:dict) -> Row:
        """Try to find the repo or create if not exists"""
        repo = self.get_repo(repo_data["fullname"])
        if repo is None:
            return self.add_repo(repo_data)
        return repo

    def update_repo(self, repo_data:Row) -> Row:
        """Update the repo information and retrive the updated value from the DB"""
        self.execute_query_update("repo", repo_data, keys=["id"], columns_timestamp=[])
        return self.get_repo(repo_data["id"], pk_column="id")