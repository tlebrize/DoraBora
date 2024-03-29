import string

BASE64 = string.ascii_letters + string.digits + "-_"


def ank_decode_cell(encoded):
    code = [0, 0]
    for index, value in enumerate(BASE64):  # index of
        if value == encoded[0]:
            code[0] = index * 64
        if value == encoded[1]:
            code[1] = index

    return sum(code)


def ank_encode_cell(decoded):
    return BASE64[decoded // 64] + BASE64[decoded % 64]


def ank_decode_int(c):
    for i in range(len(BASE64)):
        if BASE64[i] == c:
            return i
    return -1


def ank_decode_map_data(map_data):
    cells = []
    los_cells = []
    cell_id = 0

    while cell_id < len(map_data) // 10:
        cell_data = map_data[cell_id * 10 : (1 + cell_id) * 10]
        array = []

        for char in cell_data:
            array.append(ank_decode_int(char))

        walkable = ((array[2] & 56) >> 3) != 0 and cell_data.lower() not in ["bhgaeaaaaa", "hhaaeaaaaa"]

        if (array[0] & 1) == 0:
            los = False
        else:
            los = True
            los_cells.append(cell_id)

        layer_2_object = ((array[0] & 2) << 12) + ((array[7] & 1) << 12) + (array[8] << 6) + array[9]
        layer_2_object_interactive = ((array[7] & 2) >> 1) != 0
        obj = layer_2_object if layer_2_object_interactive else None

        cells.append({"cell_id": cell_id, "walkable": walkable, "los": los, "obj": obj})
        cell_id += 1

    return cells
