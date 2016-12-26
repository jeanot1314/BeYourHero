#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import math,random
import pi3d
import avatars
import maps
import objects
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
DEFAULT_SCREEN_WIDTH=300
DEFAULT_SCREEN_HEIGHT=200
DEFAULT_EYE_SEPERATION=0.65

# height of the camera
DEFAULT_AVATAR_EYE_HEIGHT = 4.0
DEFAULT_AVATAR_MOVEMENT_SPEED = 0.6

# two maps for now, so Hall (True) or Forest (False) :)
MAP_HALL = True
# Select your Avatars here (you can manualy add more)
AVATAR_1 = 'Lego'
AVATAR_2 = 'Roshi'

if(USE_STEREO):
  engine.show_stats=SHOW_STAT
  engine.debug = True
  engine.use_simple_display=not USE_TUNNEL
  engine._avatar_eye_height = DEFAULT_AVATAR_EYE_HEIGHT
  engine._avatar_movement_speed = DEFAULT_AVATAR_MOVEMENT_SPEED
  engine.hmd_screen_width = DEFAULT_SCREEN_WIDTH
  engine.hmd_screen_height = DEFAULT_SCREEN_HEIGHT
  engine.hmd_eye_seperation = DEFAULT_EYE_SEPERATION
  engine.init()
  #engine.use_crosseyed_method=False

# Setup display and initialise pi3d
if(USE_STEREO == False):
  DISPLAY = pi3d.Display.create()
  #DISPLAY = pi3d.Display.create(x=250, y=250)
  DISPLAY.set_background(0.4,0.8,0.8,1)      # r,g,b,alpha
  DISPLAY.frames_per_second = 30
  # yellowish directional light blueish ambient light
  pi3d.Light(lightpos=(1, -1, -3), lightcol=(1.0, 1.0, 0.8), lightamb=(0.25, 0.2, 0.3))

#========================================

# Create Hero & map, Select your avatars here
#avatar = avatars.cloud()
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

if MAP_HALL:
  map1 = maps.hall()
else:
  map1 = maps.forest()

bulle = objects.object()

#avatar
step = [0.0, 0.0, 0.0]
xm = 0.0
zm = 0.0
if MAP_HALL:
  avhgt = 15 # doit etre DEFAULT_AVATAR_EYE_HEIGHT
  ym = avhgt
else:
  avhgt = 9
  ym = map1.mymap.calcHeight(xm, zm) + avhgt

# camera position
rot = 0.0
tilt = -7.0
norm = None
crab = False
roll = 0.0

# variables
#distance_hero = 15
synchro_serial=0
movement = 0
mv_tmp = 0
mv_run = 0
mv_run_diff = 0
avatar_speed = DEFAULT_AVATAR_MOVEMENT_SPEED
lx = 0
ly = 0
lz = 0
orientation = 0
camera_distance = -13


shader_light = pi3d.Shader("uv_light")
coffimg = pi3d.Texture("../textures/COFFEE.PNG")
earth = pi3d.Texture("../textures/rock1.png")
flatsh = pi3d.Shader("uv_flat")
font = pi3d.Pngfont("../fonts/GillSansMT.png", (255,80,0,255))
mystring = pi3d.String(font=font, string="NOW NO EXCUSES", size=0.8, x=2, y=2, z=2, is_3d=True)
mystring2 = pi3d.String(font=font, string="BE YOUR HERO !!!", size=0.8, x=2, y=2, z=2, is_3d=True)
#mystring.translate(0.0, 0.0, 1)
mystring.scale(3, 3, 3)
mystring.set_shader(flatsh)
mystring2.scale(3, 3, 3)
mystring2.set_shader(flatsh)
myPlane = pi3d.Plane(w=7, h=1.8, name="plane")
myTriangle = pi3d.Triangle(sx=2, sy=2, sz=2, name="triangle", rz = 180)
mycone = pi3d.Cone(radius=1, height=2, sides=24, name="Cone", rz=180)
#myTriangle.set_shader(shader)

# Fetch key presses
mykeys = pi3d.Keyboard()
mymouse = pi3d.Mouse(restrict = False)
mymouse.start()

pos_armR = [0, 0, 0]
pos_forarmR = [0, 0, 0]
pos_armL = [0, 0, 0]
pos_forarmL = [0, 0, 0]
body_orientation = 0
timer =0
keep_running = True


# Initialize Camera
if(USE_STEREO == False):
  CAMERA = pi3d.Camera(absolute=False)

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

def update():
  global xm, ym, zm, step, norm, roll, orientation, movement, lx, ly, lz, mv_run, mv_run_diff, body_orientation, synchro_serial

  if(USE_STEREO): 
    (x, y, z) = engine.avatar_position
    if MAP_HALL:
      pass
    else:
      engine.avatar_y_pos = map1.mymap.calcHeight(x, z+18) + engine.avatar_eye_height +0
  
  if not USE_STEREO:
    if step != [0.0, 0.0, 0.0]: #i.e. previous loop set movmement
      pass
      if MAP_HALL:
        ym = 0
      else:
        ym, norm = map1.mymap.calcHeight(xm, zm, True)
      ym += avhgt
      #print(" Position : ", xm, " === ", ym, " === ",zm, " === ")
      step = [0.0, 0.0, 0.0]
  

  map1.myecube.position(xm, ym, zm)
  roll = 0.0
  #map1.mymap.position(0.0, 0.0, 0.0)
  #avatar.body.position(xm, mymap.calcHeight(xm, zm+distance_hero)+5.5, zm+distance_hero)

  if MAP_HALL:
    avatar.center.position(xm, ym-5, zm) # others
    avatar2.center.position(-10, 10, 15) # equivalent a -13, 15 et 0
    #bulle.Position(xm,ym,zm)
    mystring.position(-10, 18.5, 14.9)
    mystring2.position(-10, 17.5, 14.9)
    #bulle.mycone.position(-10, ym+2, 15)
    myPlane.position(-10, 18, 15)
  else:
    avatar.center.position(xm, map1.mymap.calcHeight(xm, zm), zm)
    avatar2.center.position(-30, map1.mymap.calcHeight(-30, 80), 80)
    #print(xm, ym, zm)

  if(mv_run_diff > 0):
    avatar.run(mv_run, mv_run_diff)
    synchro_serial=10
  
  if(synchro_serial == 1):
    avatar.stand()

  if (synchro_serial > 0): 
    synchro_serial -=1

  avatar.center.rotateToY(body_orientation)
  #bulle.mycone.rotateToY(movement)

  mv_run_diff=0
  lx = xm
  ly = ym
  lz = zm
  movement += 4


def update_scenario():
  global xm, ym, zm
  #print(xm, ym, zm)
  if -15 <= xm and xm <= -5 and 14 <= ym and ym <= 16 and 10 <= zm and zm <= 19:
    if -13 <= xm and xm <= -10:
      xm = -13
    elif -10 <= xm and xm <= -7:
      xm = -7
    if 13 <= zm and zm <= 14.5:
      zm = 13
    elif 14.5 <= zm and zm <= 16:
      zm = 16
      #bulle.myPlane.draw(shader_light, [earth])
      mystring.draw()
      mystring2.draw()
      myPlane.draw(shader_light, [earth])
   

def draw():
  global mv_tmp
  mv_tmp += 0.2

  #bulle.mycone.draw(shader, [coffimg])
  #avatar.handR.rotateToY(50 * math.sin(mv_tmp))
  avatar2.center.draw()
  avatar.center.draw()
  map1.mymap.draw()
  map1.myecube.draw()
  #mystring.draw()
  #myTriangle.draw()
  

def read_inputs():
  global mymouse, my, mx, rot, tilt, keep_running, xm, zm, mv_run, mv_run_diff, body_orientation

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
    elif k == 112:  #key p picture
      pi3d.screenshot("forestWalk" + str(scshots) + ".jpg")
      scshots += 1
    elif k == 10:   #key RETURN
      mc = 0
    elif k == 27:  #Escape key to exit
      print("***** Try to quit *****")
      if USE_STEREO:
        engine.hmd.close()
        engine.DISPLAY.destroy()
        engine.keep_running = False
      else:
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
  global xm, ym, zm, rot, tilt, norm
  camRad = [camera_distance, camera_distance, camera_distance]
  #print("DBG {:03.2f},{:03.2f},{:03.2f} dist {:03.2f},{:03.2f},{:03.2f}".format(xm, ym, zm, *step))
  #xm, ym, zm = CAMERA.relocate(rot, tilt, point=[xm, ym, zm], distance=step, 
  #                            normal=norm, crab=crab, slope_factor=1.5)

  if MAP_HALL:
    CAMERA.relocate(rot, tilt, point=[xm, ym, zm], distance=camRad)
  else:
    CAMERA.relocate(rot, tilt, point=[xm, map1.mymap.calcHeight(xm, zm)+3, zm], distance=camRad)
  CAMERA.rotateZ(roll)

# Main loop
if(USE_STEREO):
  while engine.DISPLAY.loop_running() or engine.keep_running:
      #read_inputs()
      engine.poll_inputs()
      engine.update_avatar()
      update()
      engine.update_camera()
      engine.render_stereo_scene(draw)
      engine.stats()
  if USE_SERIAL:
    ser.stop()

else: # not stereo
  while DISPLAY.loop_running() or keep_running:
    read_inputs()
    camera_update()
    update()
    update_scenario()
    draw()
  print(" STOP STOP")

  


