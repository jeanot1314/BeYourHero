#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import math,random
import pi3d
import avatars
import maps
import building
import objects
import os
#import sys
from serial_data import Serial_data
#sys.path.insert(0, "../python-vrzero")
from vrzero import engine

###### Select the mode here
USE_SERIAL = False # try the app without a serial connection, keyboard still work
USE_STEREO = False # Mode Stereoscopic
USE_TUNNEL = True # If mode stereo is on, use Tunnel effect
SHOW_STAT = False # Show FPS stat (Calibrated for Raspberry Pi)

# Change screen size to adapt your config
DEFAULT_SCREEN_WIDTH=1200
DEFAULT_SCREEN_HEIGHT=600
DEFAULT_EYE_SEPERATION=0.65

# height of the camera
DEFAULT_AVATAR_EYE_HEIGHT = 4.0
DEFAULT_AVATAR_MOVEMENT_SPEED = 0.6

# Select your map moon or forest
MAP = 'forest'

# Select your Avatars here (you can manualy add more)
AVATAR_1 = 'Link'
AVATAR_2 = 'Goku'

os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv('SDL_VIDEODRIVER', 'fbcon')

DISPLAY = pi3d.Display.create(w=DEFAULT_SCREEN_WIDTH, h=DEFAULT_SCREEN_HEIGHT, use_pygame=True)
DISPLAY.set_background(0.0,0.0,0.0,1)
DISPLAY.frames_per_second = 30
pi3d.Light(lightpos=(1, -1, -3), lightcol=(1.0, 1.0, 0.8), lightamb=(0.25, 0.2, 0.3))

# Initialize Camera
if(USE_STEREO):
  shader_name = "barrel" if USE_TUNNEL else "uv_flat"
  CAMERA = pi3d.StereoCam(separation=DEFAULT_EYE_SEPERATION, interlace=0, shader=shader_name)
else:
  CAMERA = pi3d.Camera(absolute=False)

#========================================

# Create Hero & map, Select your avatars here
if AVATAR_1 == 'Link':
  avatar = avatars.link()
elif AVATAR_1 == 'Cloud':
  avatar = avatars.cloud()
elif AVATAR_1 == 'Lego':
  avatar = avatars.lego()
elif AVATAR_1 == 'Roshi':
  avatar = avatars.roshi()
elif AVATAR_1 == 'Goku':
  avatar = avatars.goku()
elif AVATAR_1 == 'Goomba':
  avatar = avatars.goomba()

if AVATAR_2 == 'Link':
  avatar2 = avatars.link()
elif AVATAR_2 == 'Cloud':
  avatar2 = avatars.cloud()
elif AVATAR_2 == 'Lego':
  avatar2 = avatars.lego()
elif AVATAR_2 == 'Roshi':
  avatar2 = avatars.roshi()
elif AVATAR_2 == 'Goku':
  avatar2 = avatars.goku()

if MAP == 'forest':
  map1 = maps.forest()
elif MAP == 'moon':
  map1 = maps.moon()

bulle = objects.object()

#avatar
#step = [0.0, 0.0, 0.0]
xm = 0.0
zm = 0.0
ym = map1.mymap.calcHeight(xm, zm) + 9 + DEFAULT_AVATAR_EYE_HEIGHT
xc = 0.0
yc = 0.0
zc = 0.0


# camera position
rot = 0.0
tilt = -0.0
norm = None
crab = False
roll = 0.0

stereo_rot = 0.0
stereo_tilt = 0.0
stereo_roll = 0.0

# variables
synchro_serial=0
movement = 0
mv_tmp = 0
mv_run = 0
mv_run_diff = 0
avatar_speed = DEFAULT_AVATAR_MOVEMENT_SPEED
orientation = 0
camera_distance = -20

# Fetch key presses
mykeys = pi3d.Keyboard()
mymouse = pi3d.Mouse(restrict = False)
mymouse.start()

pos_armR = [0, 0, 0]
pos_forarmR = [0, 0, 0]
pos_armL = [0, 0, 0]
pos_forarmL = [0, 0, 0]
body_orientation = 0
flag_jump = 0
flag_view = True
jump_height = 28
timer =0
keep_running = True


def roger_handler(sensor, Euler0, Euler1, Euler2):
  global pos_armR, pos_forarmR, pos_armL, pos_forarmL, timer, body_orientation, mv_run, mv_run_diff, xm, zm
  timer += 1
  print("Sensor:", sensor)
  if timer == 13:
    timer = 0
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
  elif sensor == 'J':
    #print("JOY {:03.2f} {:03.2f}".format(Euler0, Euler1))
    if Euler0 <= 128 and Euler1 <= 128:
      body_orientation = 270 - Euler1 #
    elif Euler0 >= 128 and Euler1 <= 128:
      body_orientation = 90 + Euler1
    elif Euler0 >= 128 and Euler1 >= 128:
      body_orientation = -157 + Euler1
    elif Euler0 <= 128 and Euler1 >= 128:
      body_orientation = 360 - Euler0

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
        xm -= math.sin(math.pi/2+camera_orientation*20)*-joystick_v_axis_pos*avatar_speed
        zm += math.cos(-math.pi/2+camera_orientation*20)*-joystick_v_axis_pos*avatar_speed
        mv_run += math.fabs(joystick_v_axis_pos*avatar_speed*2/3)
     
    if math.fabs(joystick_h_axis_pos) > 0.1:
        xm -= math.cos(math.pi/2+(-camera_orientation*20))*-joystick_h_axis_pos*avatar_speed
        zm += math.sin(-math.pi/2+(-camera_orientation*20))*-joystick_h_axis_pos*avatar_speed
        mv_run += math.fabs(joystick_h_axis_pos*avatar_speed*2/3)
    mv_run_diff = math.fabs(joystick_v_axis_pos*avatar_speed*2/3) + math.fabs(joystick_h_axis_pos*avatar_speed*2/3)

    #print(xm, ym, zm, "Euler : ",joystick_v_axis_pos, joystick_h_axis_pos )

  else:
    print("unhandled sensor:", sensor)


# Implement Threading to read Serial
if(USE_SERIAL):
  ser = Serial_data('ABCDEFJ', roger_handler)
  ser.start()

#============================================================================================================

def update_position():
  global xm, ym, zm, xc, yc, zc

  ym = map1.mymap.calcHeight(xm, zm)

  avatar.center.position(xm, ym, zm)
  avatar2.center.position(-10, map1.mymap.calcHeight(-10, 15), 15)
  #avatar2.center.position(-5, map1.mymap.calcHeight(-5, 5), 5)
  bulle.myplane.position(-10, map1.mymap.calcHeight(-10, 15)+11, 15.2)

  map1.myecube.position(xm, ym, zm)

def update_avatar():
  global xm, ym, zm, mv_run, mv_run_diff, body_orientation, synchro_serial, flag_jump

  # if we are moving
  if(mv_run_diff > 0):
    avatar.run(mv_run, mv_run_diff)

    # if we are jumping
    #if(flag_jump > 0):
    #  avatar.jump(flag_jump, xm, ym, zm, body_orientation)
    #  flag_jump -=1
    synchro_serial=10

  # if we are standing
  if(synchro_serial == 1):
    avatar.stand()

    #avatar.pose()

  avatar.center.rotateToY(body_orientation)

  if (synchro_serial > 0): 
    synchro_serial -=1
  mv_run_diff=0

def update_scenario():
  global xm, ym, zm
  #print(xm, ym, zm)
  if -15 <= xm and xm <= -5 and 10 <= zm and zm <= 19:
    if -13 <= xm and xm <= -10:
      xm = -13
    elif -10 <= xm and xm <= -7:
      xm = -7
    if 13 <= zm and zm <= 14.5:
      zm = 13
    elif 14.5 <= zm and zm <= 16:
      zm = 16
    bulle.myplane.draw()

def draw():
  #global body_rotation
  #avatar.center.rotateToY(180)
  #avatar.center.position(-5, 74.5, 1)
  #global mv_tmp
  #mv_tmp += 0.2
  #avatar.pose()
  #avatar2.pose()
  avatar2.center.draw()
  avatar.center.draw()
  map1.building()
  map1.mymap.draw()
  map1.myecube.draw()
  

def read_inputs():
  global mymouse, my, mx, rot, tilt, keep_running, xm, zm, mv_run, mv_run_diff, body_orientation, flag_jump, flag_view

  k = mykeys.read() # Read Keyboard inputs
  
  if k >-1:
    if k == 119:  #key w forward
      zm+=1
      mv_run += math.fabs(avatar_speed*2/3)
      mv_run_diff = 1
      body_orientation = 180
    elif k == 115:  #kry s back
      zm+= -1
      mv_run += math.fabs(avatar_speed*2/3)
      mv_run_diff = 1
      body_orientation = 0
    elif k == 97:   #key a left
      xm+= -1
      mv_run += math.fabs(avatar_speed*2/3)
      mv_run_diff = 1
      body_orientation = 90
    elif k == 100:  #key d right
      xm+=1
      mv_run += math.fabs(avatar_speed*2/3)
      mv_run_diff = 1
      body_orientation = 270
    elif k == 99:  #key c jump
      flag_jump = 28
    elif k == 111:  #key c jump
      view = flag_view
      flag_view = not view
    elif k == 112:  #key p picture
      pi3d.screenshot("forestWalk" + str(scshots) + ".jpg")
      scshots += 1
    elif k == 10:   #key RETURN
      mc = 0
    elif k == 27:  #Escape key to exit
      print("***** EXIT *****")
      DISPLAY.destroy()
      keep_running = False
      mykeys.close()
      if USE_SERIAL:
        ser.stop()
      mymouse.stop()
      DISPLAY.stop()

    elif k == ord('f'):
      roll = 1.0

  mx, my = mymouse.velocity() #change to position() if Camera switched to absolute=True (default)
  buttons = mymouse.button_status()

  rot = - mx * 0.8
  tilt = my * 0.8

def camera_update():
  global xm, ym, zm, xc, yc, zc, rot, tilt, norm, flag_view, stereo_rot, stereo_tilt, stereo_roll

  if(USE_STEREO):
    stereo_rot += rot
    stereo_tilt += tilt
    stereo_roll += roll
    CAMERA.move_camera([xm, map1.mymap.calcHeight(xm, zm)+5, zm], stereo_rot, stereo_tilt, - stereo_roll)

    for i in range(2):
      CAMERA.start_capture(i)
      draw()
      CAMERA.end_capture(i)
    CAMERA.draw()

  else:
    if flag_view:
      camRad = [camera_distance, camera_distance, camera_distance]
    else:
      camRad = [0, 0, 0]
    
    #CAMERA.relocate(rot, tilt, point=[-5, 84.5, -0], distance=camRad)
    xc, yc, zc = CAMERA.relocate(rot, tilt, point=[xm, map1.mymap.calcHeight(xm, zm)+5, zm], distance=camRad)
    draw()
    print( xm, ym, zm, "  ----  ", xc, yc, zc)
    #CAMERA.rotateZ(roll)


# Main loop
while DISPLAY.loop_running() or keep_running:
  read_inputs()
  update_position()
  update_avatar()
  update_scenario()
  camera_update()
  #engine.stats()


