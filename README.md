# 3D Tile Processing Tools
Tools developed for manipulating 3DTile datasets


## b3dm2glb
If you need to manipulate the data inside `.b3dm` files, you first need to convert them to `.glb`, this tool does that.  
Also the [1.1 spec for 3D Tiles](https://github.com/CesiumGS/3d-tiles/tree/1.1) now uses glb as the default format, so going forward you should be using glb anyways.

This tool will convert an entire tileset from `.b3dm` to `.glb`.

You may be wondering why this tool even exists considering that this functionality already exists in the [CesiumGS 3d tiles tools](https://github.com/CesiumGS/3d-tiles-tools). 

The reason is performance.
Using the [Cesium nodeJS tool](https://github.com/CesiumGS/3d-tiles-tools#b3dmtoglb) takes about 1 minute to convert 279 `.b3dm` files to `.glb`     
The python tool provided will process over 50,000 `.b3dm` files in just over 11 seconds.

**Usage**   
`python b3dm2glb-tileset_convert.py folder_containing_tileset.json`

**How it works**  
The code will scan the folder you specified recursively looking for .b3dm files and .json files.   
- When it finds a `.b3dm` file, it will convert it to `.glb`
- When it finds a `.json` file, it will do a find/replace for all references of `.b3dm` and replace them with `.glb`
