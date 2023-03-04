# Dora Bora

A dofus 1.29 emulator, written in Python for fun.

## Datamodel

Three layers of data are needed for DoraBora to work: the database layer, the shared memory layer and the client memory layer.
The database layer consists of everything that lives longer a client's session: Accounts, Characters, Maps, Items ...
The shared memory layer owns everything that different characters must be aware, such as other players in game, or on a map. Ongoing fights and overworld creatures. The data is mostly references to database objects, for example a hash with Map ids as keys and a list of character ids on this map as values. Every clients can read and modify this layer.
Finaly the client memory layer owns what lives for a single client session, it's mostly a representation in python of database objects or states regarding these objects.

