from Game.ank_encodings import ank_decode_cell, ank_encode_cell
from Game.game_actions import GameActions


async def handle_move_action(s, data):
    destination = ank_decode_cell(data[-2:])
    game_action_id = await s.exchange.ga_move(s.character, destination)

    current_cell_code = ank_encode_cell(s.character.map_cell_id)

    path = current_cell_code + data  # check pathfinding?
    await s.exchange.broadcast_move_action(game_action_id, s.character.id, s.map.id, path)


async def handle_game_action(s, data):
    action_id = int(data[:3])
    if action_id == GameActions.MOVE:
        await handle_move_action(s, data[3:])
    else:
        raise Exception(f"Unknown action : {data}.")
