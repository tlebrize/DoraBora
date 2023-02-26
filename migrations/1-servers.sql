CREATE TYPE server_state
    AS ENUM ('offline', 'online', 'maintenance');

CREATE TABLE servers
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    name text NOT NULL,
    host text NOT NULL,
    port integer NOT NULL,
    state server_state NOT NULL DEFAULT 'offline',
    subscriber_only boolean NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT servers_name UNIQUE (name)
);

INSERT INTO
    servers (name, host, port, state, subscriber_only)
VALUES
    ('DoraBora', '127.0.0.1', 4446, 'offline', false);
