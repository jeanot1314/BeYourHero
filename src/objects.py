#!/bin/python


import pi3d
import math,random		


shader_light = pi3d.Shader("uv_light")
earth = pi3d.Texture("../textures/rock1.png")
flatsh = pi3d.Shader("uv_flat")

class object(object):

  def __init__(self):
    global flatsh

    #font = pi3d.Pngfont("../fonts/GillSansMT.png", (221,0,170,255))
    font = pi3d.Pngfont("../fonts/GillSansMT.png", (255,80,0,255))
    self.mystring = pi3d.String(font=font, string="NOW NO EXCUSES", size=0.8, x=2, y=2, z=2, is_3d=True)
    self.mystring2 = pi3d.String(font=font, string="BE YOUR HERO !!!", size=0.8, x=2, y=2, z=2, is_3d=True)
    #mystring.translate(0.0, 0.0, 1)
    self.mystring.scale(3, 3, 3)
    self.mystring.set_shader(flatsh)
    self.mystring2.scale(3, 3, 3)
    self.mystring2.set_shader(flatsh)
    self.myPlane = pi3d.Plane(w=7, h=1.8, name="plane")
    self.myTriangle = pi3d.Triangle(sx=2, sy=2, sz=2, name="triangle", rz = 180)
    self.mycone = pi3d.Cone(radius=1, height=2, sides=24, name="Cone", rz=180)
    #self.myTriangle.set_shader(shader)

  def Position(self, xm, ym, zm):
    self.mystring.position(-10, ym+2.5, 14.9)
    self.mystring2.position(-10, ym+1.5, 14.9)
    self.mycone.position(-10, ym+2, 15)
    self.myPlane.position(-10, ym+2, 15)

  def Draw(self):
    global shader_light, earth
    #self.myPlane.draw(shader_light, [earth])
    #self.mystring.draw()
    #self.mystring2.draw()




