def GM(character, cellid):
    """Informations about a character on a map."""
    return ";".join(
        map(
            str,
            [
                f"GM|+{cellid}",  # cellid
                1,  # orientation
                0,  # ? level ?
                character.id,
                character.name,
                character.class_,
                f"{character.get_gfxid()}^100x100",  # gfxid^size
                character.gender,
                f"",  # -1,0,0,0
                # alignement,?,wings,grade
                *character.get_colors(),
                ",,,,",  # equipment
                "",  # Emote
                "",  # Emote Timer
                "",  # Guild Name
                "",  # Guild Emblem
                "",  # ?
                8,  # Speed
                "",  # Close
            ],
        )
    )
