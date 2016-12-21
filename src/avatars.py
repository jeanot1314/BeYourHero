#!/bin/python


import pi3d
import math,random		


class BaseAvatar:

  class FakeModel:
    def __getattr__(self, item):
      def fake(*args, **kwargs):
        pass
      return fake

  def __init__(self):
    for name in ('armR', 'forarmR', 'handR', 'legR', 'footR', 'body', 'head', 'butt',
                 'armL', 'forarmL', 'handL', 'legL', 'footL', 'center'):
      setattr(self, name, BaseAvatar.FakeModel())


class cloud(object):

  def __init__(self):
    self.body = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_Body.obj", name="monument")
    #body.translate(90.0, -mymap.calcHeight(100.0, 235) + 20.0, 235.0)
    shader = pi3d.Shader("uv_flat")
    self.body.set_shader(shader)
    self.body.scale(6, 6, 6)
    #self.body.rotateToY(90)

    self.head = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_head.obj", name="monument", cy=-0.88, cz=-0.0)
    self.head.set_shader(shader)
    self.butt = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_butt.obj", name="monument")
    self.butt.set_shader(shader)
                
    self.armR = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_armR.obj", name="monument", cy=-0.85, cx=0.08, cz=-0.06)
    self.armR.set_shader(shader)
    self.forarmR = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_forarmR.obj", name="monument", cy=-0.85, cx=0.23, cz=-0)
    self.forarmR.set_shader(shader)
    self.handR = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_handR.obj", name="monument", cy=-8.8, cx=4.4, cz=-0.7)
    self.handR.set_shader(shader)

    self.armL = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_armL.obj", cy=-0.85, cx=-0.08, cz=-0.02)
    self.armL.set_shader(shader)
    self.forarmL = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_forarmL.obj", name="monument", cy=-0.65, cx=-0.12, cz=-0.04)
    self.forarmL.set_shader(shader)

    self.legL = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_legL.obj", name="monument", cy = -0.53)
    self.legL.set_shader(shader)
    #self.legL.scale(0.75, 0.75, 0.75)
    self.footL = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_footL.obj", name="monument", cy = -0.28)
    self.footL.set_shader(shader)
    #self.footL.scale(1.1, 1.1, 1.1)

    self.legR = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_legR.obj", name="monument", cy = -0.53)
    self.legR.set_shader(shader)
    #self.legR.scale(0.75, 0.75, 0.75)
    self.footR = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_footR.obj", name="monument", cy = -0.28)
    self.footR.set_shader(shader)
              
    self.body.add_child(self.head)
    self.body.add_child(self.butt)
    self.body.add_child(self.armR)
    self.armR.add_child(self.forarmR)
    self.forarmR.add_child(self.handR)
    self.body.add_child(self.armL)
    self.armL.add_child(self.forarmL)

    self.butt.add_child(self.legL)
    self.legL.add_child(self.footL)
    self.butt.add_child(self.legR)
    self.legR.add_child(self.footR)

  def run(self, position):
    self.legR.rotateToX(20 * math.sin(position))
    self.legL.rotateToX(-20 * math.sin(position))
    self.footR.rotateToX(-15+15 * math.sin(position))
    self.footL.rotateToX(-15-15 * math.sin(position))

  def jump(self, position):
    pass
    #compute motion

class lego(BaseAvatar):

  def __init__(self):
    super().__init__()


    self.center = pi3d.Model(file_string="../Blender/lego/Emmet_body.obj")
    shader = pi3d.Shader("uv_light")
    self.center.set_shader(shader)
    self.center.scale(6, 6, 6)

    self.head = pi3d.Model(file_string="../Blender/lego/emmet_head.obj", cy=-0.6, cz=-0)
    self.head.set_shader(shader)
                
    self.armR = pi3d.Model(file_string="../Blender/lego/Emmet_armR.obj", cy=-0.55, cx=0.15, cz=-0)
    self.armR.set_shader(shader)

    self.armL = pi3d.Model(file_string="../Blender/lego/emmet_armL.obj", cy=-0.55, cx=-0.15, cz=-0)
    self.armL.set_shader(shader)

    self.legL = pi3d.Model(file_string="../Blender/lego/Emmet_legL.obj", cy = -0.3)
    self.legL.set_shader(shader)

    self.legR = pi3d.Model(file_string="../Blender/lego/Emmet_legR.obj", cy = -0.3)
    self.legR.set_shader(shader)
              
    self.center.add_child(self.head)
    self.center.add_child(self.armR)
    self.center.add_child(self.armL)

    self.center.add_child(self.legL)
    self.center.add_child(self.legR)

  def run(self, position, diff):
    self.legR.rotateToX(20 * math.sin(position))
    self.legL.rotateToX(-20 * math.sin(position))

  def jump(self, position):
    pass
    #compute motion

  def stand(self):

    self.legR.rotateToX(0)
    self.legL.rotateToX(0)
    self.footR.rotateToX(0)
    self.footL.rotateToX(0)

    self.armL.rotateToZ(0)
    self.armR.rotateToZ(0)
    self.armR.rotateToY(0)
    self.armL.rotateToY(0)

    self.body.rotateToY(0)
    self.body.rotateToX(0)
    self.head.rotateToY(0)
    self.head.rotateToX(0)

class roshi(BaseAvatar):

  def __init__(self):
    super().__init__()
    self.center = pi3d.Model(file_string="../Blender/DBZ/Roshi/Master_Roshi.obj")
    shader = pi3d.Shader("uv_flat")
    self.center.set_shader(shader)
    self.center.scale(0.3,0.3,0.3)

class goomba(object):

  def __init__(self):
    self.body = pi3d.Model(file_string="../Blender/goomba.goomba.obj")
    shader = pi3d.Shader("uv_flat")
    self.body.set_shader(shader)
    self.body.scale(0.3,0.3,0.3)


class link(object):

  def __init__(self):

    self.center = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_full_butt.obj")
    shader = pi3d.Shader("uv_flat")
    self.center.set_shader(shader)

    self.center.scale(0.6, 0.6, 0.6)
    self.body = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_body.obj", cy=-7.4)
    #body.translate(90.0, -mymap.calcHeight(100.0, 235) + 20.0, 235.0)
    self.body.set_shader(shader)

    #self.body.rotateToY(90)

    self.head = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_head.obj", cy=-10, cz=-0.5)
    self.head.set_shader(shader)
                
    self.armR = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_armR.obj", cy=-8.6, cx=1, cz=-0.7)
    self.armR.set_shader(shader)
    self.forarmR = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_forarmR.obj", cy=-8.8, cx=2.8, cz=-0.7)
    self.forarmR.set_shader(shader)
    self.handR = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_handR.obj", cy=-8.8, cx=4.4, cz=-0.7)
    self.handR.set_shader(shader)

    self.armL = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_armL.obj", cy=-8.6, cx=-1, cz=-0.7)
    self.armL.set_shader(shader)
    self.forarmL = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_forarmL.obj", cy=-8.8, cx=-2.8, cz=-0.7)
    self.forarmL.set_shader(shader)
    self.handL = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_handL.obj", cy=-8.8, cx=-4.4, cz=-0.7)
    self.handL.set_shader(shader)

    self.legL = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_legL.obj", cy = -6)
    self.legL.set_shader(shader)
    #self.legL.scale(0.75, 0.75, 0.75)
    self.footL = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_footL.obj", cy = -3)
    self.footL.set_shader(shader)
    #self.footL.scale(1.1, 1.1, 1.1)

    self.legR = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_legR.obj", cy = -6)
    self.legR.set_shader(shader)
    #self.legR.scale(0.75, 0.75, 0.75)
    self.footR = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_footR.obj", cy = -3)
    self.footR.set_shader(shader)
                
    #self.footR.scale(1.0, 1.0, 1.0)

    self.body.add_child(self.head)
    self.body.add_child(self.armR)
    self.armR.add_child(self.forarmR)
    self.forarmR.add_child(self.handR)
    self.center.add_child(self.body)
    #self.body.add_child(self.legs)
    self.body.add_child(self.armL)
    self.armL.add_child(self.forarmL)
    self.forarmL.add_child(self.handL)

    self.center.add_child(self.legL)
    self.legL.add_child(self.footL)
    self.center.add_child(self.legR)
    self.legR.add_child(self.footR)

  def run(self, position, diff):
    #compute motion
    if diff <= 0.25:      
      self.legR.rotateToX(15 * math.sin(position))
      self.legL.rotateToX(-15 * math.sin(position))
      self.footR.rotateToX(-15+ 15 * math.sin(position))
      self.footL.rotateToX(-15 -15 * math.sin(position))

      self.armL.rotateToZ(280)
      self.armR.rotateToZ(80)
      self.armR.rotateToY(25.0 * math.sin(position))
      self.armL.rotateToY(25.0 * math.sin(position))

      self.body.rotateToY(10.0 * math.sin(position))
      self.head.rotateToY(-8.0 * math.sin(position))

    else:
      positionRun = position
      self.legR.rotateToX(25 * math.sin(positionRun))
      self.legL.rotateToX(-25 * math.sin(positionRun))
      self.footR.rotateToX(-20+ 20 * math.sin(positionRun))
      self.footL.rotateToX(-20 -20 * math.sin(positionRun))

      self.armL.rotateToZ(300)
      self.armR.rotateToZ(60)
      self.armR.rotateToY(35.0 * math.sin(positionRun))
      self.armL.rotateToY(35.0 * math.sin(positionRun))

      self.body.rotateToY(10.0 * math.sin(positionRun))
      self.body.rotateToX(-15.0)
      self.head.rotateToY(-8.0 * math.sin(positionRun))
      self.head.rotateToX(10.0)

  def stand(self):

    self.legR.rotateToX(0)
    self.legL.rotateToX(0)
    self.footR.rotateToX(0)
    self.footL.rotateToX(0)

    self.armL.rotateToZ(280)
    self.armR.rotateToZ(80)
    self.armR.rotateToY(0)
    self.armL.rotateToY(0)

    self.body.rotateToY(0)
    self.body.rotateToX(0)
    self.head.rotateToY(0)
    self.head.rotateToX(0)

  def jump(self, position):
    #compute motion
    self.armL.rotateToX(20 * math.sin(position))
    self.armR.rotateToX(-20 * math.sin(position))

class goku(object):

	def __init__(self):

                self.body = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_body.obj", name="monument")
                #body.translate(90.0, -mymap.calcHeight(100.0, 235) + 20.0, 235.0)
                shader = pi3d.Shader("uv_light")
                self.body.set_shader(shader)
                self.body.scale(0.20, 0.20, 0.20)

                self.head = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_head.obj", name="monument", x=0,y=9.2, z=0.8)
                self.head.set_shader(shader)
                self.head.scale(1.25, 1.25, 1.25)
                self.legs = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_legs.obj", name="monument", x=-3,y=-22.5)
                self.legs.set_shader(shader)
                self.butt = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_but.obj", name="monument", x=0, y=0.5, z=2.2)
                self.butt.set_shader(shader)
                self.butt.scale(1.2, 1.2, 1.2)
                
                self.armR = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_armR.obj", name="monument", x=-4.8, y=4.6, z=1.2)
                self.armR.set_shader(shader)
                self.handR = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_handR.obj", name="monument", x=-6.1, y=-0, z=+1, rx=270)
                self.handR.set_shader(shader)

                self.armL = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_armL.obj", name="monument", x=4, y=4.2, z=0)
                self.armL.set_shader(shader)
                #self.armL.scale(3, 3, 3)
                self.handL = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_handL.obj", name="monument", x=5, y=-1, z=0.5, rx=270)
                self.handL.set_shader(shader)

                self.legL = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_legL.obj", name="monument", x=2.9, y=-3, z=-1)
                self.legL.set_shader(shader)
                self.legL.scale(0.75, 0.75, 0.75)
                self.footL = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_foot.obj", name="monument", x=0, y=-24, z=-2.5)
                self.footL.set_shader(shader)
                self.footL.scale(1.1, 1.1, 1.1)

                self.legR = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_legL.obj", name="monument", x=-1.5, y=-3, z=-1)
                self.legR.set_shader(shader)
                self.legR.scale(0.75, 0.75, 0.75)
                self.footR = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_foot.obj", name="monument", x=-0, y=-24, z=-2.5)
                self.footR.set_shader(shader)
                
                self.footR.scale(1.0, 1.0, 1.0)


                self.body.add_child(self.head)
                self.body.add_child(self.armR)
                self.armR.add_child(self.handR)
                self.body.add_child(self.butt)
                #self.body.add_child(self.legs)
                self.body.add_child(self.armL)
                self.armL.add_child(self.handL)

                self.butt.add_child(self.legL)
                self.legL.add_child(self.footL)
                self.butt.add_child(self.legR)
                self.legR.add_child(self.footR)

	def run(self, position):
                #compute motion
                self.legR.rotateToX(15 * math.sin(position))
                self.legL.rotateToX(-15 * math.sin(position))
                self.armL.rotateToZ(305)
                self.armR.rotateToZ(80)
                self.armR.rotateToY(25.0 * math.sin(position))
                self.armL.rotateToY(25.0 * math.sin(position))

class guy(object):

	def __init__(self):

                #Create human
                #porl = pi3d.Model(file_string="Blender/Porl.obj", name="monument")
                #porl.translate(90.0, -mymap.calcHeight(100.0, 235) + 12.0, 235.0)
                #porl.scale(5.0, 5.0, 5.0)

                self.body = pi3d.Model(file_string="../Blender/pi_Porl_Body.obj", name="monument")
                #body.translate(90.0, -mymap.calcHeight(100.0, 235) + 20.0, 235.0)
                self.body.scale(1.0, 1.0, 1.0)

                self.head = pi3d.Model(file_string="../Blender/pi_Porl_Head.obj", name="monument", y=1.84)
                #head.translate(90.0, -mymap.calcHeight(100.0, 235) + 29.6, 235.0)
                self.armR = pi3d.Model(file_string="../Blender/pi_Porl_Arm_Right.obj", name="monument", x=-0.5, y=1.64, z=0.1)
                #arm.translate(87.5, -mymap.calcHeight(100.0, 235) + 28.2, 235.5)
                self.handR = pi3d.Model(file_string="../Blender/pi_Porl_Hand_Right.obj", name="monument", x=-0.75)
                #hand.translate(83.5, -mymap.calcHeight(100.0, 235) + 28.2, 235.5)

                self.legs = pi3d.Model(file_string="../Blender/pi_Porl_Legs.obj", name="monument", y=-3.7)
                self.armL = pi3d.Model(file_string="../Blender/pi_Porl_Arm_Left.obj", name="monument", x=0.5, y=1.64, z=0.1)
                self.handL = pi3d.Model(file_string="../Blender/pi_Porl_Hand_Left.obj", name="monument", x=0.75)


                self.body.add_child(self.head)
                self.body.add_child(self.armR)
                self.armR.add_child(self.handR)
                self.body.add_child(self.legs)
                self.body.add_child(self.armL)
                self.armL.add_child(self.handL)


	def  sitDown(self):
                #motion sitdown
                pass

	def play(self, position):
                #motion sitdown
                pass

	def  jump(self):
                #motion sitdown
                pass

	def run(self, position):
                #compute motion
                self.armL.rotateToX(25.0 * math.sin(position))
                self.handL.rotateToX(30)
                self.armR.rotateToX(-25.0 * math.sin(position))
                self.handR.rotateToX(30.0)


	def test(self, position):
                #compute motion
                pass

