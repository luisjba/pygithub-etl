CREATE TABLE IF NOT EXISTS repo(
    id integer PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    owner VARCHAR(255) NOT NULL,
    fullname VARCHAR(511) NOT NULL,
    description TEXT NOT NULL,
    url VARCHAR(511) NOT NULL,
    pushed_date INTEGER NOT NULL,
    created_date INTEGER NOT NULL,
    updated_date INTEGER NOT NULL,
    size INTEGER NOT NULL,
    stars INTEGER NOT NULL,
    forks INTEGER NOT NULL,
    watchers INTEGER NOT NULL,
    language VARCHAR(255) NOT NULL,
    topics TEXT NOT NULL
);