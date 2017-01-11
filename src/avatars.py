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


class cloud(BaseAvatar):

  def __init__(self):
    super().__init__()
    shader = pi3d.Shader("uv_flat")

    self.center = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_butt.obj")
    self.center.set_shader(shader)
    self.center.scale(6, 6, 6)

    self.body = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_Body.obj")
    self.body.set_shader(shader)
    self.head = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_head.obj", cy=-0.88, cz=-0.0)
    self.head.set_shader(shader)

    self.armR = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_armR.obj", cy=-0.85, cx=0.08, cz=-0.06)
    self.armR.set_shader(shader)
    self.forarmR = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_forarmR.obj", cy=-0.85, cx=0.23, cz=-0)
    self.forarmR.set_shader(shader)
    self.handR = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_handR.obj", cy=-8.8, cx=4.4, cz=-0.7)
    self.handR.set_shader(shader)

    self.armL = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_armL.obj", cy=-0.85, cx=-0.08, cz=-0.02)
    self.armL.set_shader(shader)
    self.forarmL = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_forarmL.obj", cy=-0.65, cx=-0.12, cz=-0.04)
    self.forarmL.set_shader(shader)

    self.legL = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_legL.obj", cy = -0.53)
    self.legL.set_shader(shader)
    self.footL = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_footL.obj", cy = -0.28)
    self.footL.set_shader(shader)

    self.legR = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_legR.obj", cy = -0.53)
    self.legR.set_shader(shader)
    self.footR = pi3d.Model(file_string="../Blender/FF7/Cloud Board Piece/Cloud_footR.obj", cy = -0.28)
    self.footR.set_shader(shader)

    self.center.add_child(self.body)              
    self.body.add_child(self.head)
    self.body.add_child(self.armR)
    self.armR.add_child(self.forarmR)
    self.forarmR.add_child(self.handR)
    self.body.add_child(self.armL)
    self.armL.add_child(self.forarmL)

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

    self.armL = pi3d.Model(file_string="../Blender/lego/emmet_armL_sword.obj", cy=-0.55, cx=-0.15, cz=-0)
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

  def cut(self, position):
    #self.armL.rotateToZ(300)
    self.armL.rotateToX(300+90.0 * math.sin(position/4)) # half a move
    #self.armL.rotateToY(0+70.0 * math.sin(position/4)) # half a move


class roshi(BaseAvatar):

  def __init__(self):
    super().__init__()
    self.center = pi3d.Model(file_string="../Blender/DBZ/Roshi/Master_Roshi.obj")
    shader = pi3d.Shader("uv_flat")
    self.center.set_shader(shader)
    self.center.scale(0.3,0.3,0.3)
  def run(self, position, diff):
    pass
  def stand(self):
    pass

class goomba(BaseAvatar):

  def __init__(self):
    super().__init__()
    self.center = pi3d.Model(file_string="../Blender/goomba/goomba/goomba.obj")
    shader = pi3d.Shader("uv_flat")
    self.center.set_shader(shader)
    #self.center.scale(0.1,0.1,0.1)
    self.center.scale(0.3,0.3,0.3)
  def run(self, position, diff):
    self.center.rotateToX(12.0 * math.sin(position*2))
    self.center.rotateToZ(12.0 * math.sin(position*3))
  def stand(self):
    self.body.rotateToX(0)
    self.body.rotateToZ(0)

class toad(BaseAvatar):

  def __init__(self):
    super().__init__()
    self.center = pi3d.Model(file_string="../Blender/toad/toad.obj")
    shader = pi3d.Shader("uv_flat")
    self.center.set_shader(shader)
    #self.center.scale(0.1,0.1,0.1)
    self.center.scale(0.03,0.03,0.03)
  def run(self, position, diff):
    self.center.rotateToX(12.0 * math.sin(position*2))
    self.center.rotateToZ(12.0 * math.sin(position*3))
  def stand(self):
    self.body.rotateToX(0)
    self.body.rotateToZ(0)

class goombaB(BaseAvatar):

  def __init__(self):
    super().__init__()
    self.center = pi3d.Model(file_string="../Blender/goomba/goomba_blood/goomba.obj")
    shader = pi3d.Shader("uv_bump")
    self.center.set_shader(shader)
    #self.center.scale(0.1,0.1,0.1)
    self.center.scale(0.3,0.3,0.3)
  def run(self, position, diff):
    self.center.rotateToX(12.0 * math.sin(position*2))
    self.center.rotateToZ(12.0 * math.sin(position*3))
  def stand(self):
    self.body.rotateToX(0)
    self.body.rotateToZ(0)

class goombaD(BaseAvatar):

  def __init__(self):
    super().__init__()
    self.center = pi3d.Model(file_string="../Blender/goomba/goomba_dead/goomba.obj")
    shader = pi3d.Shader("uv_bump")
    self.center.set_shader(shader)
    self.center.scale(0.4,0.4,0.4)

class link(BaseAvatar):

  def __init__(self):
    super().__init__()
    self.center = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_full_butt.obj")
    shader = pi3d.Shader("uv_flat")
    self.center.set_shader(shader)
    self.center.scale(0.6, 0.6, 0.6)

    self.body = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_body.obj", cy=-7.4)
    self.body.set_shader(shader)
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
    self.footL = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_footL.obj", cy = -3)
    self.footL.set_shader(shader)

    self.legR = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_legR.obj", cy = -6)
    self.legR.set_shader(shader)
    self.footR = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_footR.obj", cy = -3)
    self.footR.set_shader(shader)

    self.center.add_child(self.body)
    self.body.add_child(self.head)

    self.body.add_child(self.armR)
    self.armR.add_child(self.forarmR)
    self.forarmR.add_child(self.handR)

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

  def pose(self):

    self.legR.rotateToX(15)
    self.legL.rotateToX(-15)
    self.footR.rotateToX(-10)
    self.footL.rotateToX(0)

    #self.armL.rotateToZ(280)
    self.armL.rotateToZ(40)
    self.forarmL.rotateToY(10)

    self.armR.rotateToX(30)
    self.armR.rotateToY(280)
    #self.armR.rotateToZ(280)
    self.forarmR.rotateToZ(90)
    self.forarmR.rotateToY(300)

    self.body.rotateToY(0)
    self.body.rotateToX(0)
    self.head.rotateToY(0)
    self.head.rotateToX(0)

  def jump(self, position):

    self.armL.rotateToZ(60)
    #self.armR.rotateToZ(300)
    #self.armR.rotateToY(35.0 * math.sin(positionRun))
    #self.armL.rotateToY(35.0 * math.sin(positionRun))

  def cut(self, position):
    #self.armL.rotateToZ(300)
    self.armL.rotateToZ(300+30.0 * math.sin(position/4)) # half a move
    self.armL.rotateToY(0+70.0 * math.sin(position/4)) # half a move
    self.forarmL.rotateToY(0+70.0 * math.sin(position/4))

class linkstereo(BaseAvatar):

  def __init__(self):
    super().__init__()
    self.center = pi3d.Model(file_string="../Blender/Zelda/Custom_Link/Link_full_butt.obj")
    shader = pi3d.Shader("uv_flat")
    self.center.set_shader(shader)
    self.center.scale(0.6, 0.6, 0.6)
                
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

    self.center.add_child(self.armR)
    self.armR.add_child(self.forarmR)
    self.forarmR.add_child(self.handR)

    self.center.add_child(self.armL)
    self.armL.add_child(self.forarmL)
    self.forarmL.add_child(self.handL)

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

  def pose(self):

    self.legR.rotateToX(15)
    self.legL.rotateToX(-15)
    self.footR.rotateToX(-10)
    self.footL.rotateToX(0)

    #self.armL.rotateToZ(280)
    self.armL.rotateToZ(40)
    self.forarmL.rotateToY(10)

    self.armR.rotateToX(30)
    self.armR.rotateToY(280)
    #self.armR.rotateToZ(280)
    self.forarmR.rotateToZ(90)
    self.forarmR.rotateToY(300)

    self.body.rotateToY(0)
    self.body.rotateToX(0)
    self.head.rotateToY(0)
    self.head.rotateToX(0)

  def jump(self, position):

    self.armL.rotateToZ(60)
    #self.armR.rotateToZ(300)
    #self.armR.rotateToY(35.0 * math.sin(positionRun))
    #self.armL.rotateToY(35.0 * math.sin(positionRun))

  def cut(self, position):
    #self.armL.rotateToZ(300)
    self.armL.rotateToZ(300+30.0 * math.sin(position/4)) # half a move
    self.armL.rotateToY(0+70.0 * math.sin(position/4)) # half a move
    self.forarmL.rotateToY(0+70.0 * math.sin(position/4))

class goku(BaseAvatar):

  def __init__(self):
    super().__init__()
    shader = pi3d.Shader("uv_light")

    self.center = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_butt.obj")
    self.center.set_shader(shader)
    self.center.scale(0.2, 0.2, 0.2)

    self.body = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_body.obj", cy=-23)
    self.body.set_shader(shader)

    self.head = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_head.obj", cy=-33, cz=0.5)
    self.head.set_shader(shader)
    self.legs = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_legs.obj")
    self.legs.set_shader(shader)
                
    self.armR = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_armR.obj", cy=-29, cx=4, cz=0.4)
    self.armR.set_shader(shader)
    self.handR = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_handR.obj", cy=-29, cx=8.5, cz=0)
    self.handR.set_shader(shader)

    self.armL = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_armL.obj", cy=-29, cx=-5, cz=0.4)
    self.armL.set_shader(shader)
    self.handL = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_handL2.obj", cy=-29, cx=-11, cz=0.8)
    self.handL.set_shader(shader)

    self.legL = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_legL.obj", cy = -21)
    self.legL.set_shader(shader)
    self.footL = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_footL.obj", cy = -15)
    self.footL.set_shader(shader)

    self.legR = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_legR.obj", cy = -21)
    self.legR.set_shader(shader)
    self.footR = pi3d.Model(file_string="../Blender/DBZ/Goku/goku_footR.obj", cy = -15)
    self.footR.set_shader(shader)

    self.center.add_child(self.body)
    self.body.add_child(self.head)

    self.body.add_child(self.armR)
    self.armR.add_child(self.handR)
    self.body.add_child(self.armL)
    self.armL.add_child(self.handL)

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
      self.handL.rotateToZ(80)
      self.handR.rotateToZ(-80)
      self.handL.rotateToY(80)
      self.handR.rotateToY(-80)

      self.body.rotateToY(10.0 * math.sin(positionRun))
      self.body.rotateToX(-15.0)
      self.head.rotateToY(-8.0 * math.sin(positionRun))
      self.head.rotateToX(10.0)

  def stand(self):

    self.legR.rotateToX(0)
    self.legL.rotateToX(0)
    self.footR.rotateToX(0)
    self.footL.rotateToX(0)

    self.armL.rotateToZ(300)
    self.armR.rotateToZ(60)
    self.armR.rotateToY(0)
    self.armL.rotateToY(0)
    self.handL.rotateToY(0)
    self.handR.rotateToY(0)
    self.handL.rotateToZ(0)
    self.handR.rotateToZ(0)

    self.body.rotateToY(0)
    self.body.rotateToX(0)
    self.head.rotateToY(0)
    self.head.rotateToX(0)

  def pose(self):

    self.legR.rotateToX(40)
    self.legL.rotateToX(-40)
    self.footR.rotateToX(-35)
    self.footL.rotateToX(0)

    #self.armL.rotateToZ(280)
    #self.armL.rotateToZ(40)
    #self.forarmL.rotateToY(10)

    self.armL.rotateToX(30)
    self.armL.rotateToY(-280)

    #self.armR.rotateToZ(90)
    self.armR.rotateToZ(70)
    self.handR.rotateToY(-90)
    #self.handR.rotateToY(350)

    self.body.rotateToY(0)
    self.body.rotateToX(-30)
    #self.head.rotateToY(0)
    self.head.rotateToX(20)

  def jump(self, position):
    self.armL.rotateToX(20 * math.sin(position))
    #self.armR.rotateToX(-20 * math.sin(position))

  def cut(self, position):
    #self.armL.rotateToZ(300)
    self.armL.rotateToZ(300+30.0 * math.sin(position/4)) # half a move
    self.armL.rotateToY(0+70.0 * math.sin(position/4)) # half a move
    self.handL.rotateToY(0+70.0 * math.sin(position/4))

class guy(BaseAvatar):

  def __init__(self):
    super().__init__()
    #Create human
    #porl = pi3d.Model(file_string="Blender/Porl.obj", name="monument")
    #porl.translate(90.0, -mymap.calcHeight(100.0, 235) + 12.0, 235.0)
    #porl.scale(5.0, 5.0, 5.0)

    self.body = pi3d.Model(file_string="../Blender/pi_Porl_Body.obj")
    #body.translate(90.0, -mymap.calcHeight(100.0, 235) + 20.0, 235.0)
    self.body.scale(1.0, 1.0, 1.0)

    self.head = pi3d.Model(file_string="../Blender/pi_Porl_Head.obj", y=1.84)
    self.armR = pi3d.Model(file_string="../Blender/pi_Porl_Arm_Right.obj", x=-0.5, y=1.64, z=0.1)
    self.handR = pi3d.Model(file_string="../Blender/pi_Porl_Hand_Right.obj", x=-0.75)

    self.legs = pi3d.Model(file_string="../Blender/pi_Porl_Legs.obj", y=-3.7)
    self.armL = pi3d.Model(file_string="../Blender/pi_Porl_Arm_Left.obj", x=0.5, y=1.64, z=0.1)
    self.handL = pi3d.Model(file_string="../Blender/pi_Porl_Hand_Left.obj", x=0.75)

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

