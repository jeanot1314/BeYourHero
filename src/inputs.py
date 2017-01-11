#!/bin/python

import math,random
import pi3d
import inputs
from serial_data import Serial_data

# Serial DOF
#pos_armR = [0, 0, 0]
#pos_forarmR = [0, 0, 0]
#pos_armL = [0, 0, 0]
#pos_forarmL = [0, 0, 0]

class handlers:

  def __init__(self):

    self.USE_SERIAL = False
    self.rot = 0
    self.tilt = 0

    self.x = 0
    self.z = 0
    self.body_orientation = 180
    self.mv_run = 0
    self.mv_run_diff = 0
    self.avatar_speed = 2

    self.flag_jump = 0
    self.flag_cut = 0
    self.flag_protect = 0.0
    self.ser = 0
    self.cpt_view = 0
    self.flag_view = True
    self.Euler_diff=0
    #mykeys = pi3d.Keyboard(use_curses=True)
    self.mykeys = pi3d.InputEvents(self.key_handler_func, self.mouse_handler_func, self.joystick_handler_func)
    self.keep_running = True

######### Return the values ##########
  def rotation(self):
    return(self.rot, self.tilt)

  def position_upd(self, x, z):
    self.x += x
    self.z += z

  def update(self):
    self.mv_run_diff=0

  def position(self):
    return(self.x, self.z, self.body_orientation, self.mv_run, self.mv_run_diff, self.flag_view)

  def view(self):
    return(self.flag_view)

  def action_update(self):
    cut = self.flag_cut
    jump = self.flag_jump
    if self.flag_cut:
      self.flag_cut-=1
    if self.flag_jump:
      self.flag_jump-=1
    return(jump, cut, self.flag_protect)

  def actionRead(self):
    return(self.flag_jump, self.flag_cut, self.flag_protect)

######### Fonctions ##########
  def roger_handler(self, sensor, Euler0, Euler1, Euler2):
    #timer += 1
    #print("SENSOR:", sensor)
    #if timer == 13:
    #  timer = 0

    SIMPLE_MOVE = True
    if SIMPLE_MOVE:
      if sensor == 'A':
        if not self.flag_cut and math.fabs(Euler1) + math.fabs(Euler2) >= self.Euler_diff + 0.3:
          self.flag_cut = 12
        #print(" E1 = ", Euler1, " E2 = ", Euler2)
        #print(math.fabs(Euler1) + math.fabs(Euler2))
        self.Euler_diff = math.fabs(Euler1) + math.fabs(Euler2)

      elif sensor == 'D':
        #print(math.fabs(Euler1) + math.fabs(Euler2))
        if math.fabs(Euler1) + math.fabs(Euler2) >= 0.7:
          self.flag_protect = 1
        else:
          self.flag_protect = 0
        #avatar.armR.rotateToZ(math.degrees(-Euler1))
        #avatar.armR.rotateToX(math.degrees(-Euler2))
        #avatar.armR.rotateToY(math.degrees(-Euler0))
        #pos_forarmR = [-Euler0 - pos_armL[0], -Euler0 - pos_armL[1], -Euler0 - pos_armL[2]]

      elif sensor == 'C':
        avatar.head.rotateToZ(math.degrees(-Euler1))
        avatar.head.rotateToX(math.degrees(-Euler2))
        avatar.head.rotateToY(math.degrees(-Euler0))

    else:
      if sensor == 'B':
        avatar.armL.rotateToZ(math.degrees(-Euler1))
        avatar.armL.rotateToX(math.degrees(-Euler2))
        avatar.armL.rotateToY(math.degrees(-Euler0))
        #pos_armL = [Euler0, Euler1, Euler2]
        #print("Bras : E0 = ", math.degrees(Euler0), " E1 = ", math.degrees(Euler1), " E2 = ", math.degrees(Euler2))

      elif sensor == 'C':
        avatar.armR.rotateToZ(math.degrees(-Euler1))
        avatar.armR.rotateToX(math.degrees(-Euler2))
        avatar.armR.rotateToY(math.degrees(-Euler0))
        #pos_forarmR = [-Euler0 - pos_armL[0], -Euler0 - pos_armL[1], -Euler0 - pos_armL[2]]

      elif sensor == 'D':
        avatar.head.rotateToZ(math.degrees(-Euler1))
        avatar.head.rotateToX(math.degrees(-Euler2))
        avatar.head.rotateToY(math.degrees(-Euler0))

        #if timer == 1:
        #  print("                                        Avant : E0 = ", math.degrees(Euler0), " E1 = ", math.degrees(Euler1), " E2 = ", math.degrees(Euler2))
    
    if sensor == 'J':
      #print("JOY {:03.2f} {:03.2f}".format(Euler0, Euler1))
      #print(Euler2)
      #print("ENTER EULER 2 ", Euler0, Euler1, Euler2)
      if Euler2 == '0':

        if Euler0 <= 128 and Euler1 <= 128:
          self.body_orientation = 270 - Euler1 
        elif Euler0 >= 128 and Euler1 <= 128:
          self.body_orientation = 90 + Euler1
        elif Euler0 >= 128 and Euler1 >= 128:
          self.body_orientation = -157 + Euler1
        elif Euler0 <= 128 and Euler1 >= 128:
          self.body_orientation = 360 - Euler0

        #print(body_orientation)
   
        if Euler0 >= 128:
          Euler0 -= 255
        if Euler1 >= 128:
          Euler1 -= 255
        joystick_v_axis_pos = Euler0/128
        joystick_h_axis_pos = Euler1/128

        #camera_tilt, camera_orientation= CAMERA.point_at()
        #print("ORIENTATION : ", camera_orientation)

        camera_orientation = 0


    
        if math.fabs(joystick_v_axis_pos) > 0.1:
          self.x -= math.sin(math.pi/2+camera_orientation*20)*-joystick_v_axis_pos*self.avatar_speed
          self.z += math.cos(-math.pi/2+camera_orientation*20)*-joystick_v_axis_pos*self.avatar_speed
          self.mv_run += math.fabs(joystick_v_axis_pos*self.avatar_speed*2/3)
     
        if math.fabs(joystick_h_axis_pos) > 0.1:
          self.x -= math.cos(math.pi/2+(-camera_orientation*20))*-joystick_h_axis_pos*self.avatar_speed
          self.z += math.sin(-math.pi/2+(-camera_orientation*20))*-joystick_h_axis_pos*self.avatar_speed
          self.mv_run += math.fabs(joystick_h_axis_pos*self.avatar_speed*2/3)
        self.mv_run_diff = math.fabs(joystick_v_axis_pos*self.avatar_speed*2/3) + math.fabs(joystick_h_axis_pos*self.avatar_speed*2/3)

        #print(xm, ym, zm, "Euler : ",joystick_v_axis_pos, joystick_h_axis_pos )
    
      else:
        self.cpt_view += 1
        if self.cpt_view == 2:
          view = self.flag_view
          self.flag_view = not view
          self.cpt_view = 0

    else:
      pass
      #print("sensor:", sensor)

  def serial(self):
    self.ser = Serial_data('ABCDEFJ', self.roger_handler)
    self.ser.start()
    self.USE_SERIAL = True
  
  def joystick_handler_func(self, sourceType, sourceIndex, x1, y1, z1, x2, y2, z2, hatx, haty):
    #print(x1, y1)
    #global rot, tilt
    #mymouse.velocity() #change to position() if Camera switched to absolute=True (default)
    #buttons = #mymouse.button_status()
    self.rot = - x1 * 200
    self.tilt = y1 * 200

  def mouse_handler_func(self, sourceType, sourceIndex, delta_x, delta_y, v, h):
    pass
    #print("ENTER MOUSE")

  def key_handler_func(self, sourceType, sourceIndex, key, value):
    #k = mykeys.read() # Read Keyboard inputs
    #print(key)
    orientation = 0
    if self.mykeys.key_state("KEY_S"): #115:  #kry s back
      self.z+= -1
      self.mv_run += math.fabs(self.avatar_speed*1/2)
      self.mv_run_diff = 1
      orientation += 1
      #self.body_orientation = 0
    if self.mykeys.key_state("KEY_A"): #97:   #key a left
      self.x+= -1
      self.mv_run += math.fabs(self.avatar_speed*1/2)
      self.mv_run_diff = 1
      orientation += 2
      #self.body_orientation = 90
    if self.mykeys.key_state("KEY_W"): #pi3d.event.Event.key_to_code('KEY_W'):#119:  #key z forward
      self.z+=1
      self.mv_run += math.fabs(self.avatar_speed*1/2)
      self.mv_run_diff = 1
      orientation += 4
      #self.body_orientation = 180
    if self.mykeys.key_state("KEY_D"):#100:  #key d right
      print("         RIGHT")
      self.x+=1
      self.mv_run += math.fabs(self.avatar_speed*1/2)
      self.mv_run_diff = 1
      orientation += 8
      #self.body_orientation = 270
    if self.mykeys.key_state("KEY_C"): #99:  #key c jump
        if not self.flag_jump:
          self.flag_jump = 25
    if self.mykeys.key_state("KEY_V"): #118:  #key cut
        self.flag_cut = 12
    if self.mykeys.key_state("KEY_O"): #111:  #key o
        self.cpt_view += 1
        if self.cpt_view == 2:
          view = self.flag_view
          self.flag_view = not view
          self.cpt_view = 0
    if self.mykeys.key_state("KEY_P"): #112:  #key p picture
        pi3d.screenshot("BeYourHero" + str(scshots) + ".jpg")
        scshots += 1
    if self.mykeys.key_state("KEY_ESC"):  #Escape key to exit
        print("***** EXIT *****")
        #os.system('xset r on')

        self.keep_running = False

        #self.mykeys.release()
        if self.USE_SERIAL:
          self.ser.stop()
        #mymouse.stop()
        #DISPLAY.destroy()
        #DISPLAY.stop()

    if orientation == 1:
      self.body_orientation = 0
    elif orientation == 3:
      self.body_orientation = 45
    elif orientation == 2:
      self.body_orientation = 90
    elif orientation == 6:
      self.body_orientation = 135
    elif orientation == 4:
      self.body_orientation = 180
    elif orientation == 12:
      self.body_orientation = 225
    elif orientation == 8:
      self.body_orientation = 270
    elif orientation == 9:
      self.body_orientation = 315

  def read_exit(self):
    return self.keep_running






