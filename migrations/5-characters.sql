CREATE TABLE characters
(
    id                  integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    server_id           integer NOT NULL,
    account_id          integer NOT NULL,
    map_id              integer NOT NULL,
    class_              integer NOT NULL,
    name                text NOT NULL,
    gender              integer NOT NULL,
    colors              integer[3] NOT NULL DEFAULT '{-1,-1,-1}',
    level               integer NOT NULL DEFAULT 1,
    kamas               integer NOT NULL DEFAULT 0,
    spell_points        integer NOT NULL DEFAULT 0,
    stat_points         integer NOT NULL DEFAULT 0,
    energy              integer NOT NULL DEFAULT 0,
    experience          integer NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    CONSTRAINT character_name UNIQUE (name),
    CONSTRAINT character_map FOREIGN KEY (map_id)
        REFERENCES maps (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT character_server FOREIGN KEY (server_id)
        REFERENCES servers (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT character_account FOREIGN KEY (account_id)
        REFERENCES accounts (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID
);

INSERT INTO characters (server_id, account_id, map_id, name, class_, gender)
VALUES (
    (SELECT id FROM servers LIMIT 1),
    (SELECT id FROM accounts LIMIT 1),
    (SELECT id FROM maps WHERE position[1] = 0 AND position[2] = 0 LIMIT 1),
    'Ya-Boy',
    1,
    1
)