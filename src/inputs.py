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
    self.ser = 0
    self.cpt_view = 0
    self.flag_view = True
    #mykeys = pi3d.Keyboard(use_curses=True)
    self.mykeys = pi3d.InputEvents(self.key_handler_func, self.mouse_handler_func, self.joystick_handler_func)
    self.keep_running = True

######### Return the values ##########
  def rotation(self):
    return(self.rot, self.tilt)

  def position_upd(self, x, z):
    self.x += x
    self.z += z

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
    return(jump, cut)

  def actionRead(self):
    return(self.flag_jump, self.flag_cut)

######### Fonctions ##########
  def roger_handler(self, sensor, Euler0, Euler1, Euler2):
    #timer += 1
    #print("SENSOR:", sensor)
    #if timer == 13:
    #  timer = 0

    SIMPLE_MOVE = True
    if SIMPLE_MOVE:
      if sensor == 'A':
        if flag_cut < 4 and math.fabs(Euler1) + math.fabs(Euler2) >= Euler_diff + 0.3:
          flag_cut = 12
        #print(" E1 = ", Euler1, " E2 = ", Euler2)
        #print(math.fabs(Euler1) + math.fabs(Euler2))
        Euler_diff = math.fabs(Euler1) + math.fabs(Euler2)

      elif sensor == 'C':
        if flag_cut < 4 and math.fabs(Euler1) + math.fabs(Euler2) >= Euler_diff + 0.3:
          flag_cut = 12
        Euler_diff = math.fabs(Euler1) + math.fabs(Euler2)
        #avatar.armR.rotateToZ(math.degrees(-Euler1))
        #avatar.armR.rotateToX(math.degrees(-Euler2))
        #avatar.armR.rotateToY(math.degrees(-Euler0))
        #pos_forarmR = [-Euler0 - pos_armL[0], -Euler0 - pos_armL[1], -Euler0 - pos_armL[2]]

      elif sensor == 'D':
        avatar.head.rotateToZ(math.degrees(-Euler1))
        avatar.head.rotateToX(math.degrees(-Euler2))
        avatar.head.rotateToY(math.degrees(-Euler0))

    else:
      if sensor == 'A':
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
    if key >-1:
      if key == pi3d.event.Event.key_to_code('KEY_W'):#119:  #key z forward
        self.z+=1
        self.mv_run += math.fabs(self.avatar_speed*1/2)
        self.mv_run_diff = 1
        self.body_orientation = 180
      elif key == pi3d.event.Event.key_to_code('KEY_S'): #115:  #kry s back
        self.z+= -1
        self.mv_run += math.fabs(self.avatar_speed*1/2)
        self.mv_run_diff = 1
        self.body_orientation = 0
      elif key == pi3d.event.Event.key_to_code('KEY_A'): #97:   #key a left
        self.x+= -1
        self.mv_run += math.fabs(self.avatar_speed*1/2)
        self.mv_run_diff = 1
        self.body_orientation = 90
      elif key == pi3d.event.Event.key_to_code('KEY_D'):#100:  #key d right
        self.x+=1
        self.mv_run += math.fabs(self.avatar_speed*1/2)
        self.mv_run_diff = 1
        self.body_orientation = 270
      elif key == pi3d.event.Event.key_to_code('KEY_C'): #99:  #key c jump
        if not self.flag_jump:
          self.flag_jump = 25
      elif key == pi3d.event.Event.key_to_code('KEY_V'): #118:  #key w cut
        self.flag_cut = 12
        #print("eee")
      elif key == pi3d.event.Event.key_to_code('KEY_O'): #111:  #key o
        view = self.flag_view
        self.flag_view = not view
      elif key == pi3d.event.Event.key_to_code('KEY_P'): #112:  #key p picture
        pi3d.screenshot("forestWalk" + str(scshots) + ".jpg")
        scshots += 1
      elif key == 10:   #key RETURN
        mc = 0
      elif key == pi3d.event.Event.key_to_code('KEY_ESC'):  #Escape key to exit
        print("***** EXIT *****")
        #os.system('xset r on')

        self.keep_running = False

        #mykeys.close()
        #if USE_SERIAL:
        self.ser.stop()
        #mymouse.stop()
        #DISPLAY.destroy()
        #DISPLAY.stop()

      elif key == ord('f'):
        roll = 1.0

  def read_exit(self):
    return self.keep_running






