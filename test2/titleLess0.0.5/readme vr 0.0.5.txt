##############################################################
##############################################################
##                                                          ##
##  Mumei v.r. 0.0.5                                        ##
##  SVN: http://code.google.com/p/titleless/                ##
##  URL: http://titleless.blogsome.com/                     ##
##  Date: 12/05/2008                                        ##
##                                                          ##
##############################################################
##############################################################

Index.

1. Introduction
2. Description
3. Changes
4. What's next
5. Custom the map
6. Disclaimer

1. Introduction

This is the windows executable of Mumei, this is a strategy game in an isometric world, by now there's no
story, only one dungeon and one character =).

2. Description

This is a strategy game, it's written in python with the pyGame module. The graphical part is all in pixelArt.

3. Changes

- Added better transparencies
- Restrict going up or down two or more tiles

4. What's next

- Improve transparencies algorithm

5. Custom the map

You can create your own map, you only need to change the newDungeon.txt file which is in ./data/maps

Look in the tiles.txt file which is in the same folder of newDungeon.txt and play with the maps.

Each tile is represented in the file as [1:G], the tile level is the first part of the token, and can not be greatter than 9 or you will
see an ugly crash, the second part is the tile graphic, you can define tile graphics in the file tiles.txt that is in the same folder.

You can tell the script the non walkable tiles in nwTiles.txt file.

So, what are you waiting, erase a complete line from that file and run the game to see what happened. Give it a try!

6. Disclaimer

This is an open source project, which means that you can distribute it, sell it, play it, buy it, copy it, but you MUST do all  
that providing the proper documentation (like this file for example).