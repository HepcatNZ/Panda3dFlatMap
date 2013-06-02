Panda3dFlatMap
==============

Some experimentation with using a plane rather than a heightmap

Controls:
==============

- WASD: Movement
- Space: Create new message (in top left)
- +: Zoom In
- -: Zoom Out
- Alt+F4: Quit

On using the Tools:
==============

1. Place your custom texture.jpg and associated regions.png in the maps folder.
2. Run ImageToMap.py which will generate a map_output.xml file of your texture.jpg and regions.png
3. Run MapEditor.py
4. The left window is for your map details and the right is to view the map while you edit it
5. Choose your map from the drop down box
6. Now name your provinces. You can pick them from the list or by clicking on their colour in the right window.
7. Click save, it will be saved as map_output.xml and is ready to put into the game.

Notes:
- Renaming texture and regions images needs to be manually added to the xml file
- Images need to be added manually under <image></image>
- The regions.png is what determines the map size, sizes of texture and regions do NOT need to match. The texture will be scaled to whatever size regions is.