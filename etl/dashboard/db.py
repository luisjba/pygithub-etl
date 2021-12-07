import sqlite3
import click
from flask import Flask, current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    # with current_app.open_resource('schema.sql') as f:
    #     db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app:Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def commits_max_date() -> int:
    return get_db().execute(
        "SELECT MAX(commit_author_date) AS MaxDate FROM commits"
    ).fetchone()['MaxDate']

def repos_modified_series(start:int, end:int) -> list:
    query="""
    SELECT repo.name AS Name
        ,IFNULL(SUM(cm.stats_total), 0)  AS Total
    FROM repo 
    LEFT JOIN (
        SELECT repo_id
            ,stats_total
            ,commit_author_date
        FROM commits
        WHERE commits.commit_author_date BETWEEN ? AND ?
    ) AS cm
    ON (cm.repo_id = repo.id)
    GROUP BY repo.name
	ORDER BY Total DESC
    """
    return get_db().execute(query, [start, end]).fetchall()

def repos_modified_files_series(start, end):
    query="""
    SELECT repo.name AS Name
        ,IFNULL(COUNT(cm.file_id), 0)  AS Total
    FROM repo 
    LEFT JOIN (
        SELECT commits.repo_id
            ,commit_file.id AS file_id
        FROM commits
        INNER JOIN commit_file ON (commit_file.commit_id = commits.id)
        WHERE commits.commit_author_date BETWEEN ? AND ?
    ) AS cm
    ON (cm.repo_id = repo.id)
    GROUP BY repo.name
	ORDER BY Total DESC
    """
    return get_db().execute(query, [start, end]).fetchall()

def repos_modified_by_author_series(start, end):
    query="""
    SELECT repo.name AS Name
        ,IFNULL(COUNT(cm.author), 0)  AS Total
    FROM repo 
    LEFT JOIN (
        SELECT commits.repo_id
            ,commits.commit_author_name AS author
        FROM commits
        WHERE commits.commit_author_date BETWEEN ? AND ?
    ) AS cm
    ON (cm.repo_id = repo.id)
    GROUP BY repo.name
	ORDER BY Total DESC
    """
    return get_db().execute(query, [start, end]).fetchall()

def repos_top_contributors(start, end, limit=10):
    query="""
    SELECT commits.commit_author_name AS name
        ,commits.author_login AS login
		,commits.author_avatar_url as url
        ,IFNULL(SUM(commits.stats_total), 0)  AS contributions
        ,IFNULL(COUNT(DISTINCT commits.repo_id), 0)  AS repos
        ,IFNULL(COUNT(commit_file.id), 0)  AS files
    FROM commits
    INNER JOIN commit_file ON (commit_file.commit_id = commits.id)
    WHERE commits.commit_author_date BETWEEN ? AND ?
    GROUP BY commits.commit_author_name
	ORDER BY contributions DESC
    LIMIT ?
    """
    return get_db().execute(query, [start, end, limit]).fetchall()
