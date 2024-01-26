# DoraBora

A python dofus server.


## TODO

### Mobs

Mob groups on maps:
- fixed : always the same group, fixed position
- dynamic : variable group contents and size

RankedMonster:
	rank: int
	monster: FK Monster

MobGroup:
	map_id: FK Map
	mob_ids: M2M Monster through RankedMonster
	max_size: int
	min_size: int
	is_fixed: bool

	<!-- for fixed only -->
	cell_id: int
	respawn_delay: int

