CREATE TABLE IF NOT EXISTS commit_file(
    id integer PRIMARY KEY,
    commit_id INTEGER NOT NULL,
    repo_id INTEGER NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    addtions INTEGER NOT NULL,
    deletions INTEGER NOT NULL,
    changes INTEGER NOT NULL,
    status VARCHAR(255) NOT NULL,
    FOREIGN KEY (commit_id) REFERENCES commits (id),
    FOREIGN KEY (repo_id) REFERENCES repo (id)
);