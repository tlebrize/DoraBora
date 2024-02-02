from asgiref.sync import sync_to_async

from Game.fight import create_monster_fight
from Game.game_actions import GameActions


async def handle_move_acknowledge(s, success, action_data, payload):
    assert s.character
    assert s.map

    if success:
        s.character.cell_id = action_data["destination"]
    else:
        s.character.cell_id = int(payload[0])

    if door := s.map.doors.get(str(action_data["destination"])):
        new_map, new_cell = await s.character.teleport(door[0], door[1])
        await s.write(f"GA;2;{s.character.id};")
        await s.exchange.broadcast_character_left_map(s.character.id, s.map.id)
        s.exchange.character_left_map(s.character, s.map)
        s.map = new_map
        s.exchange.character_joined_map(s.character, s.map)
        await s.write(s.map.format_GDM())
    else:
        await s.character.asave()

    await s.write("BN")

    group_id = await sync_to_async(s.map.get_aggressing_group)(s.character)
    if group_id:
        s.fight = await create_monster_fight(s, group_id)
        await s.exchange.fight_started(s.fight)
        await s.exchange.broadcast_fight_count(s.map.id)
        await s.write(s.fight.format_gjk())

        gdf_packet = await s.fight.format_gdf()
        if gdf_packet:
            await s.write()

        # TODO timer ??

        await s.write(await s.fight.format_gp(team=0))


async def handle_game_action_acknowledges(s, data):
    success = data[0] == "K"
    id_, *payload = data[1:].split("|")
    action_data = s.exchange.pop_action(int(id_))

    print(f"* GK : {action_data}")

    if action_data["kind"] == GameActions.MOVE:
        await handle_move_acknowledge(s, success, action_data, payload)
    else:
        raise Exception("Unknown action : " + action_data)
