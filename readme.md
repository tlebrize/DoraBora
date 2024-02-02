# DoraBora

A python dofus server.


## TODO

### Fights

- check la validité du combat
- rendre indisponible le groupe de mobs
- enregistrer la position dans overworld du perso
- créer le Fight
- GAME_SEND_MAP_FIGHT_COUNT_TO_MAP
- Fight:166


### Datamodel

all in memory ?
	-> fast
Lobby model or fight state ?
why is map coppied ?
timings ?
fight server for synchronisation ?
	socket ?

spell cooldowns ?
	-> buffs ? if yes rename them ? no

positions on map -> need to use a proper map position system

```yaml
Fighter:
	origin_id : int
	origin_type : ['Monster' | 'Character' | 'Summon']
	team: ['A', 'B']
	fight: FK Fight
	controller: FK Character? Account? client_id? # Null means AI ?
	x: int
	y: int
	# z ? is_carried_by ? buff ?
	summoner : FK Fighter

	temporary stats ? remove them from monster class and source them from template instead ?
	or just hold them in memory ?
```

```yaml
FightEntities: # traps, glyphs
	fight: FK Fight
	template_id : ?
	???
```

```yaml
Fight:
	map: FK Map
	initiative: json {value: fighter_id}
	state: Lobby|Fight|Finished
```

```yaml
Buff:
	target: FK Fighter
	origin: FK Fighter
	template_id: Fk BuffTemplate
	value: int ?
	turns_left: int
	trigger: ['start_turn', 'pa_spent', 'end_turn']
```