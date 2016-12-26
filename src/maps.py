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

class hall(object):

  def __init__(self):
    #Setup shaders
    flatsh = pi3d.Shader("uv_flat")
    #shade2d = pi3d.Shader('2d_flat')

    # create splash screen and draw it
    #splash = pi3d.ImageSprite("../textures/pi3d_splash.jpg", shade2d, w=10, h=10, z=0.2)
    #splash.draw()
    #DISPLAY.swap_buffers()

    #Setup environment cube
    ectex = pi3d.loadECfiles("../textures/ecubes/Miramar", "miramar_256", "png", nobottom = True)
    self.myecube = pi3d.EnvironmentCube(size=1800.0, maptype="FACES", nobottom=True)
    self.myecube.set_draw_details(flatsh, ectex)

    #Load Hall model
    self.mymap = pi3d.Model(file_string="../models/ConferenceHall/conferencehall.egg", name="Hall", sx=0.1, sy=0.1, sz=0.1)
    self.mymap.set_shader(flatsh)
    self.mymap.position(0.0,10.0, 0.0)

