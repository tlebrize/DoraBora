CREATE TABLE maps
(
    id                  integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    dofus_id           integer NOT NULL,
    date                text NOT NULL,
    width               integer DEFAULT NULL,
    height              integer DEFAULT NULL,
    key_                text NOT NULL,
    position            integer[3] NOT NULL DEFAULT '{0,0,0}',
    PRIMARY KEY (id)
    -- places              text,
    -- mapData             text NOT NULL,
    -- background_id       integer NOT NULL,
    -- music_id            integer NOT NULL,
    -- ambiente_id         integer NOT NULL,
    -- song                integer NOT NULL DEFAULT 0
    -- monsters
    -- numgroup
    -- minSize
    -- fixSize
    -- maxSize
    -- forbidden
    -- sniffed
    -- minRespawnTime
    -- maxRespawnTime
    -- outdoor
    -- capabilities
);
