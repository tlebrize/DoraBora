async def list_characters_on_map(s, map_id):
    return await s.redis.smembers(f"server.{s.server_id}.map.{map_id}")


async def add_character_to_map(s, map_id, character_id):
    await s.redis.sadd(f"server.{s.server_id}.map.{map_id}", character_id)


async def remove_character_from_map(s, map_id, character_id):
    await s.redis.srem(f"server.{s.server_id}.map.{map_id}", character_id)
