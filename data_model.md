# Tables

## Server

`id` PK
`name` String
`host` String
`port` Int
`state` Enum (0: Offline, 1: Online, 2: Maintenance)
`subscriber_only` Bool

## Account

`id` PK
`username` String
`password` String
`nickname` String
`state` Enum (0: Offline, 1:InLogin, 2:InGame, 3:Banned)
`subscribed_time_remaining` Long
`is_game_master` Bool
`security_question` String

## Characters

`id` PK
`server_id` FK Server
`account_id` FK Account
