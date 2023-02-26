CREATE TYPE account_state
    AS ENUM ('offline', 'in_login', 'in_game', 'banned');

CREATE TABLE accounts
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    username text NOT NULL,
    nickname text NOT NULL,
    password text NOT NULL,
    state account_state NOT NULL DEFAULT 'offline',
    subscribed_seconds integer DEFAULT null,
    is_game_master boolean NOT NULL DEFAULT false,
    security_question text NOT NULL,
    community integer NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT accounts_username UNIQUE (username),
    CONSTRAINT accounts_nickname UNIQUE (nickname)
);

INSERT INTO
    accounts (username, nickname, password, state, subscribed_seconds,
        is_game_master, security_question, community)
VALUES
    ('qwe', 'TestQwe', 'password', 'offline', 1000000,
        false, 'isitqwe?', 2);

