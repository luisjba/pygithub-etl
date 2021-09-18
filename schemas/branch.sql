CREATE TABLE IF NOT EXISTS branch(
    id integer PRIMARY KEY,
    repo_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    commit_sha VARCHAR(255) NOT NULL,
    protected  INTEGER NOT NULL,
    FOREIGN KEY (repo_id) REFERENCES repo (id)
);