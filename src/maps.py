#!/bin/python


import pi3d
import math,random		


class forest(object):

  def __init__(self):

    # load shader
    shader = pi3d.Shader("uv_bump")
    shinesh = pi3d.Shader("uv_reflect")
    flatsh = pi3d.Shader("uv_flat")

    bumpimg = pi3d.Texture("../textures/grasstile_n.jpg")
    reflimg = pi3d.Texture("../textures/stars.jpg")
    floorimg = pi3d.Texture("../textures/floor_nm.jpg")

    FOG = ((0.3, 0.3, 0.4, 0.8), 650.0)
    TFOG = ((0.2, 0.24, 0.22, 1.0), 150.0)

    #myecube = pi3d.EnvironmentCube(900.0,"HALFCROSS")
    ectex=pi3d.loadECfiles("../textures/ecubes","sbox")
    self.myecube = pi3d.EnvironmentCube(size=900.0, maptype="FACES", name="cube")
    self.myecube.set_draw_details(flatsh, ectex)
    self.myecube.position(0,0,0)

    # Create elevation map
    mapsize = 1000.0
    mapheight = 60.0
    mountimg1 = pi3d.Texture("../textures/mountains3_512.jpg")
    self.mymap = pi3d.ElevationMap("../textures/mountainsHgt.png", name="map",
                         width=mapsize, depth=mapsize, height=mapheight,
                         divx=32, divy=32) 
    self.mymap.set_draw_details(shader, [mountimg1, bumpimg, reflimg], 128.0, 0.0)
    self.mymap.set_fog(*FOG)
    self.mymap.position(0.0, 0.0, 0.0)

    #screenshot number
    scshots = 1

  def building(self):
    pass

class moon(object):

  def __init__(self):

    shader = pi3d.Shader("uv_reflect")
    bumpsh = pi3d.Shader("uv_bump")
    flatsh = pi3d.Shader("uv_flat")
    #shade2d = pi3d.Shader('2d_flat')

    ectex = pi3d.loadECfiles("../textures/ecubes/RedPlanet", "redplanet_256", "png", True)
    self.myecube = pi3d.EnvironmentCube(size=1800.0, maptype="FACES")
    self.myecube.set_draw_details(flatsh,ectex)

    # Create elevation map
    mapwidth=2000.0
    mapdepth=2000.0
    mapheight=100.0
    redplanet = pi3d.Texture("../textures/mars_colour.png")
    bumpimg = pi3d.Texture("../textures/mudnormal.jpg")
    self.mymap = pi3d.ElevationMap(mapfile='../textures/mars_height.png',
                     width=mapwidth, depth=mapdepth, height=mapheight,
                     divx=64, divy=64)
    self.mymap.set_draw_details(bumpsh,[redplanet, bumpimg],128.0, 0.0)
    self.mymap.set_fog((0.3, 0.15, 0.1, 0.0), 1000.0)

    #Load Corridors sections

    sttnbmp = pi3d.Texture("../textures/floor_nm.jpg")
    sttnshn = pi3d.Texture("../textures/stars.jpg")
    x,z = 0,0
    y = self.mymap.calcHeight(x, z)
    #corridor with windows
    self.cor_win = pi3d.Model(file_string="../models/MarsStation/corridor_win_lowpoly.egg",
                x=x, y=y, z=z, sx=0.1, sy=0.1, sz=0.1)
    self.cor_win.set_shader(shader)
    #normal corridor
    self.corridor = pi3d.Model(file_string="../models/MarsStation/corridor_lowpoly.egg",
                 x=x, y=y, z=z, sx=0.1, sy=0.1, sz=0.1)
    self.corridor.set_shader(shader)
    #corridor crossing
    self.cor_cross = pi3d.Model(file_string="../models/MarsStation/cross_room.egg",
                 x=x, y=y, z=z, sx=0.1, sy=0.1, sz=0.1)
    self.cor_cross.set_shader(shader)
    self.cor_cross.set_normal_shine(sttnbmp, 32.0, sttnshn, 0.1)
    #corridor crossing with doors
    self.cor_cross_doors = pi3d.Model(file_string="../models/MarsStation/cross_room_doors.egg",
                        x=x, y=y, z=z, sx=0.1, sy=0.1, sz=0.1)
    self.cor_cross_doors.set_shader(shader)
    self.cor_cross_doors.set_normal_shine(sttnbmp, 32.0, sttnshn, 0.1)
    #corridor with 90 degree bend
    self.cor_bend = pi3d.Model(file_string="../models/MarsStation/bend_lowpoly.egg",
                 x=x, y=y, z=z, sx=0.1, sy=0.1, sz=0.1)
    self.cor_bend.set_shader(shader)
    self.cor_bend.set_normal_shine(sttnbmp, 32.0)
    self.cor_bend.rotateToY(180)

  def building(self):
    mody = 3
    spc = 39.32
    #pi3d.Utility.draw_level_of_detail([xm, ym, zm], [0, mody, 0], [[opendist,cor_cross],[1000,cor_cross_doors]])
    #90 degree units
    self.corridor.rotateToY(90)
    self.cor_win.rotateToY(90)
    self.cor_win.position(0, mody, spc*1.5)
    self.cor_win.draw()
    self.corridor.position(0, mody, spc*2.5)
    self.corridor.draw()
    self.cor_win.position(0, mody, spc*3.5)
    self.cor_win.draw()
    self.cor_win.position(0, mody, spc*6.5)
    self.cor_win.draw()
    #0 degree units
    self.corridor.rotateToY(0)
    self.cor_win.rotateToY(0)
    #pi3d.Utility.draw_level_of_detail([xm, ym, zm], [0, mody, spc*5],[[opendist,cor_cross],[1000,cor_cross_doors]])
    #pi3d.Utility.draw_level_of_detail([xm, ym, zm],[0, mody, spc*8], [[opendist,cor_cross],[1000,cor_cross_doors]])
    self.cor_win.position(-spc*1.5, mody, spc*5)
    self.cor_win.draw()
    self.cor_bend.position(-spc*2.5, mody, spc*5)
    self.cor_bend.draw()
    #pi3d.Utility.draw_level_of_detail([xm, ym, zm],[-spc*2.6, mody, spc*6.6],[[opendist,cor_cross],[1000,cor_cross_doors]])
    self.cor_win.position(spc*1.5, mody, spc*5)
    self.cor_win.draw()
    self.corridor.position(spc*2.5, mody, spc*5)
    self.corridor.draw()
    #pi3d.Utility.draw_level_of_detail([xm, ym, zm],[spc*4, mody, spc*5],[[opendist,cor_cross],[1000,cor_cross_doors]])


