#!/bin/python


import pi3d
import math,random		

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

