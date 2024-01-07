# DoraBora

A python dofus server.


## Architecture

DoraBora is made of multiple services:

- client : an async python server, handling socket connection for the game and login servers.
	- login : a sub-service handling login and gameserver selection.
	- game : the main game.
- management : a django server, handling the database state and exposing an admin interface.
- db : a postgres database.
- redis : a redis instance acting as a shared memory and pub/sub.
- static : an nginx server serving static files for the client. (langs, maps ...)

## DataModel

Three types of data are needed for DoraBora to work: the persistent layer, the shared memory layer and the user memory layer.

The persistent layer consists of everything that lives longer a user's session: Accounts, Characters, Maps, Items ...
The database contents and schema are managed by the management service but access directly by the client service.

The shared memory layer owns everything that multiple users need to access at once, such as other players in game, or on a map. Ongoing fights and overworld creatures. The data is mostly references to database objects, for example a hash with Map ids as keys and a list of character ids on this map as values. Every user can read and modify this layer.

Finaly the user memory layer owns what lives for a single user session, it's mostly a representation in python of database objects or states regarding these objects.


