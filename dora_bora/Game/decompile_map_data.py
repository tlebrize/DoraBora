from Game.ank_encodings import ank_decode_int

data = "bhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhaaeaaaaaHhaaeaaaaaHhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhaaeaaaaaHhaaeaaaaaHhaaeaaaaaHhaaej0aaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhaaeaaaaaHhaaej1aaaHhbgej2aaaHhbgej2aaaHhaaej0iaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhaaeaaaaaHhaaej0aaaGhbgeaaaqiHhbgeaaajeHhHgeaDaaaHhbgej0iaabhbgeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhaaeaaaaaHhaaej0aaaHhbgeqkeqjHhbgeaDiqjHhHgeaaaaaHhbgeaaajeHhHgeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhaaej0aaaHhaaej1aaaHhHgeqkGaaHhHgeqkqaaHhHgeaaaaaHhHgeaaaaaHhHgeaaaaaHhbgejhiaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhaaeaaaaaHhaaej0aaaHhiaej2d1MHhHgej4aaaHhHgeaaaaaHhHgeaaaaaHhHgeaaaaaHhHgeaaaaaHhHgeaaaaaHhaaej0iaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhaaeaaaaaHhiaej0d1MHhHgeaaaaaHhHggaaaaaHhHggaaaaaHhHggqkaaaHhHgeaaaaaHhHgeaaaaaHhHgeaaaaaHhHgeaaaaaHhaaej0iaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhaaej0aaaHhiaej0d1MHhHgeaaaaaHhHgeaaaaaHhHgeaaaaaHhHggaaaaaHhHggaaaaaHhHgeaaaaaHhHgeaaaaaHhHgeaaaaaHhHgeaaaaaHhaaeaaaaabhaaeaaaaabhaaeaaaaaHhiaej0d1MHhaaej2aaaHhHggaaaaaHhHggaaaaaHhHggqkaaaGhbggaaaqiHhHgeaaaaaHhHggqkWaaHhHgeqkaaaHhHgeaaaaaHhbgeaTajeHhaaeaaej0bhaaeaaaaabhaaeaaaaaHhaaej0aaaHhHgeaaaaaHhHgeaTaaaHhHgeaaaaaHhHggaaaaaHhbggaaeqjHhHgeqkiaaHhHgeaaaaaHhHgeqkaaaHhHgeqkGaaHhHgeaaaaaHhHgeaaaaabhaaeaaaaabhaaeaaaaaHhaaej0aaaHhHgeaDaaaHhHgeaaaaaHhHgeaaaaaHhHggaaaaaHhHgeaaaaaHhHggaaaaaHhHgeaaaaaHhHgeqkaaaHhHggqkWaaHhHgeaaaaaHhHgeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhHggaaaaaHhHgeaaaaaHhHgeaaaaaHhHggaaaaaHhHggaaaaaHhHggaaaaaHhHggaaaaaHhHgem2aaaHhHggaaaaaHhHggaaaaaHhHgeaaaaaHhHgeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhHgeaaaaaHhHggaaaaaHhHgeaaaaaHhHggaaaaaHhHgeaaaaaHhHggm2aaaHhHgeaaaaaHhHggaaaaaHhHggaaaaaHhHgeaaaaaHhHgeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhHggaaaaaHhHgeaaaaaHhbgeaaaqjHhHggaaaaaHhHgeaaaaaHhHgeaaaaaGhbggaaeqiHhHgeaaaaaHhHggaaaaaHhHggaaaaaHhHgeaaaaaHhHgeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhHgeaaaaaHhHgeqkaaaHhHggaaaaaHhHgeaaaaaHhHggaaaaaHhbggaaeqjHhbggaaaqjGhbggaaaqiHhHgem2aaaGhbggaaaqiHhHgeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhHgeaaaaaHhHgeaaaaaHhHgeaaaaaHhHggqkqaaHhHgeaaaaaHhHggaaaaaHhHgeqkaaaHhbgeaaaqjHhHgeqkiaaHhHggaaaaaHhHgeaaaaaHhHgeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhHggaaaaaHhHggaaaaaHhHgeaaaaaHhHggaaaaaHhHgeaaaaaHhHgeaaaaaHhHggaaaaaHhHggqkGaaHhHgeaaaaaHhbggaaaqjHhHggaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhHggaaaaaHhHgeaaaaaHhHgeaaaaaHhHggaaaaaHhHgeaaaaaHhHgeaaaaaHhHggaaaaaHhHggaaaaaHhHgeaaaaaHhHgeaaaaaHhHgeaaaaaHhHgeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhHgeaaaaaHhHggaaaaaHhHgeaaaaaHhHggaaaaaHhHggaaaaaHhHgeaaaaaHhHgeaaaaaHhHggaaaaaHhHgeaaaaaHhHggaaaaaHhHgeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhHggm2aaaHhHggaaaaaHhHgeaaaaaHhHggaaaaaHhHgeqkGaaHhHggaaaaaHhbgeaaeqjHhHgeaaaaaHhHggaaaaaHhHgeaaaaaHhHgeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhHggctiaaHhHggaaaaaHhHggaaaaaHhHggaaaaaHhHggaaaaaHhHgeaaaaaGhbgeaaeqiHhHggaaaaaHhHggaaaaaHhHggaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhHgeaaaaaHhHggm1aaaHhHggaaaaaHhHggaaaaaHhHgeaaaaaHhHgeaaaaaHhHggaaaaaHhHgeaaaaaHhHgeaaaaaHhHggaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHhGaOaaaaaHhHgecsaaaHhHggm2aaaHhHggaaaaaHhHgeaaaaaHhHggaaaaaHhbgeaaaqjHhHggaaaaaHhHggaaaaaHhHgeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHiGaOaaaaaHhGaOaaaaaahaaeaaaaaHhHggctaaaHhHggaaaaaHhHgeaaaaaHhHgeaaaaaHhHggaaaaaHhHggaaaaaHhHggaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHjiaeaaaaaHiGaOaaaaabhaaeaaaaaahaaeaaaaaHhHgeaaaaaHhHggaaaaaHhHggaaaaaHhHggaaaaaHhHggaaaaaHhHgeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaaHjiaeh3aqgbhaaeaaaaabhaaeaaaaaahaaeaaaaaHhHggaaaaaHhHgeaaaaaHhHgeaaaaaHhHggaaaaaHhHggaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaabhaaeaaaaa"


# public List<GameCase> decompileMapData(GameMap map, String data, byte sniffed) {
def decompile_map_data(map_data):
    # List<GameCase> cells = new ArrayList<>();
    # List<Short> losCells = new ArrayList<>();
    cells = []
    los_cells = []

    # if(mapCrypted(data) && !map.getKey().isEmpty()) {
    #     try {
    #         data = this.decryptMapData(data, map.getKey());
    #     } catch (Exception e) {
    #         System.err.println("Erreur decypher map data : " + map.getId());
    #         e.printStackTrace();
    #     }
    # }

    # TODO ??
    # if(PathFinding.outForbiddenCells.get(map.getW() + "_" + map.getH()) == null)
    #     PathFinding.outForbiddenCells.put(map.getW() + "_" + map.getH(), cellWalkable(map));

    # short cellId = 0
    cell_id = 0

    # for (; cellId < data.length()/10; cellId ++ ){
    while cell_id < len(map_data) // 10:
        # String cellData = data.substring(cellId*10, (cellId+1)*10);
        cell_data = map_data[cell_id * 10 : (1 + cell_id) * 10]
        # byte[] array = new byte[10];
        array = []

        # for (int i = 0; i < cellData.length(); i++)
        #     array[i] = (byte) getIntByHashedValue(cellData.charAt(i));
        for char in cell_data:
            array.append(ank_decode_int(char))

        # walkable = (((array[2] & 56 ) >> 3) != 0 && !cellData.equalsIgnoreCase("bhGaeaaaaa") && !cellData.equalsIgnoreCase("Hhaaeaaaaa"));
        walkable = ((array[2] & 56) >> 3) != 0 and not (cell_data.lower() in ["bhgaeaaaaa", "hhaaeaaaaa"])

        # if((array[0] & 1) == 0)
        #     los = false;
        # if(los) losCells.add(cellId);
        if (array[0] & 1) == 0:
            los = False
        else:
            los = True
            los_cells.append(cell_id)

        # unused
        # short tmp = (short) ((array[4] & 60) >> 2);
        # if (tmp != 1) groundSlope = tmp;
        # tmp = (short) (array[1] & 15);
        # if (tmp != 0) groundLevel = tmp;

        # int layerObject2 = ((array[0] & 2) << 12) + ((array[7] & 1) << 12) + (array[8] << 6) + array[9];
        # boolean layerObject2Interactive = ((array[7] & 2) >> 1) != 0;
        # int obj = (layerObject2Interactive ? layerObject2 : -1);
        layer_2_object = ((array[0] & 2) << 12) + ((array[7] & 1) << 12) + (array[8] << 6) + array[9]
        layer_2_object_interactive = ((array[7] & 2) >> 1) != 0
        obj = layer_2_object if layer_2_object_interactive else None

        # cells.add(new GameCase(map, cellId, walkable, los, obj));
        cells.append({"cell_id": cell_id, "walkable": walkable, "los": los, "obj": obj})
        cell_id += 1

    return cells


print(decompile_map_data(data))
