-- Tabelul pentru utilizatori
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- Tabelul pentru seriale, cu asociere la utilizatori
CREATE TABLE infoseries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    imdb_link TEXT NOT NULL,
    last_episode TEXT NOT NULL,
    last_viewed_date DATE,
    score INTEGER NOT NULL,
    snoozed BOOLEAN DEFAULT FALSE
)