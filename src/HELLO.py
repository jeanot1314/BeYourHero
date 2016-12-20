#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import math,random
import pi3d
import avatars
import maps
#import sys
from serial_data import Serial_data
#sys.path.insert(0, "../python-vrzero")
from vrzero import engine

USE_SERIAL = False
USE_STEREO = False
USE_TUNNEL = True
SHOW_STAT = True

DEFAULT_SCREEN_WIDTH=1920
DEFAULT_SCREEN_HEIGHT=1080
DEFAULT_EYE_SEPERATION=0.65

DEFAULT_AVATAR_EYE_HEIGHT = 4.0
DEFAULT_AVATAR_MOVEMENT_SPEED = 1.0

MAP_HALL = False

if(USE_STEREO):
  engine.show_stats=SHOW_STAT
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
  DISPLAY.set_background(0.4,0.8,0.8,1)      # r,g,b,alpha
  DISPLAY.frames_per_second = 30
  # yellowish directional light blueish ambient light
  pi3d.Light(lightpos=(1, -1, -3), lightcol=(1.0, 1.0, 0.8), lightamb=(0.25, 0.2, 0.3))

#========================================

# Create Hero & map
#avatar = avatars.cloud()
avatar = avatars.lego()
avatar2 = avatars.link()
avatar3 = avatars.goku()
avatar4 = avatars.cloud()
avatar5 = avatars.roshi()
if MAP_HALL:
  map1 = maps.hall()
else:
  map1 = maps.forest()
#avatar = avatars.goku()

#avatar camera
rot = 0.0
tilt = 0.0

xm = 0.0
zm = 0.0
if MAP_HALL:
  avhgt = 15
  ym = avhgt
else:
  avhgt = 9#9
  ym = map1.mymap.calcHeight(xm, zm) + avhgt

step = [0.0, 0.0, 0.0]
norm = None
crab = False
roll = 0.0

# variables
distance_hero = 15
movement = 0
mv_run = 0
lx = 0
ly = 0
lz = 0
orientation = 0
movement = 0

shader = pi3d.Shader("uv_light")
coffimg = pi3d.Texture("../textures/COFFEE.PNG")
flatsh = pi3d.Shader("uv_flat")
#font = pi3d.Pngfont("../fonts/GillSansMT.png", (221,0,170,255))
font = pi3d.Pngfont("../fonts/GillSansMT.png", (20,10,250,255))
mystring = pi3d.String(font=font, string="Ready to play ??", size=0.8, x=2, y=2, z=2, is_3d=True)
#mystring.translate(0.0, 0.0, 1)
mystring.scale(3, 3, 3)
mystring.set_shader(flatsh)
myPlane = pi3d.Plane(w=4, h=1.2, name="plane", z=5)

# Fetch key presses
mykeys = pi3d.Keyboard()
mymouse = pi3d.Mouse(restrict = False)
mymouse.start()

pos_armR = [0, 0, 0]
pos_forarmR = [0, 0, 0]
pos_armL = [0, 0, 0]
pos_forarmL = [0, 0, 0]
body_orientation = 0
joystick_h_axis_pos = 0.0
joystick_v_axis_pos = 0.0
joystick_right_h_axis_pos = 0.0
joystick_right_v_axis_pos = 0.0
timer =0
keep_running = True

def roger_handler(sensor, Euler0, Euler1, Euler2):
  global pos_armR, pos_forarmR, pos_armL, pos_forarmL, timer, body_orientation, step, crab, mv_run
  timer += 1
  if timer == 13:
    timer = 0
  if sensor == 'C':
    avatar.armL.rotateToZ(math.degrees(-Euler2))
    avatar.armL.rotateToX(math.degrees(-Euler1))
    avatar.armL.rotateToY(math.degrees(-Euler0))
    pos_armL = [Euler0, Euler1, Euler2]
    if timer == 1:
      print("Bras : E0 = ", math.degrees(Euler0), " E1 = ", math.degrees(Euler1), " E2 = ", math.degrees(Euler2))

  elif sensor == 'B':
    avatar.forarmL.rotateToZ(math.degrees(-Euler2 + pos_armL[2]))
    avatar.forarmL.rotateToX(math.degrees(-Euler1 + pos_armL[1]))
    avatar.forarmL.rotateToY(math.degrees(-Euler0 + pos_armL[0]))
    pos_forarmL = [-Euler0 - pos_armL[0], -Euler0 - pos_armL[1], -Euler0 - pos_armL[2]]


  elif sensor == 'D':
    avatar.handL.rotateToZ(math.degrees(-Euler2))
    avatar.handL.rotateToX(math.degrees(-Euler1))
    avatar.handL.rotateToY(math.degrees(-Euler0))
    if timer == 1:
      print("                                                                     Avant : E0 = ", math.degrees(Euler0), " E1 = ", math.degrees(Euler1), " E2 = ", math.degrees(Euler2))
  elif sensor == 'J':
    
    if Euler0 <= 128 and Euler1 <= 128:
      body_orientation = +270 - Euler1
    elif Euler0 >= 128 and Euler1 <= 128:
      body_orientation = 90 + Euler1
    elif Euler0 >= 128 and Euler1 >= 128:
      body_orientation = (Euler1-157)
    elif Euler0 <= 128 and Euler1 >= 128:
      body_orientation = 360 - Euler0
 
    if body_orientation <= 225 and body_orientation >= 135:
      step = [1, 0.0, 1]
      crab = False
    elif body_orientation <= 315 and body_orientation >= 225:
      step = [-1, 0.0, -1]
      crab = True
    elif (body_orientation <= 45 and body_orientation >= 0) or (body_orientation <= 360 and body_orientation >= 315):
      step = [-1, 0.0, -1]
      crab = False
    elif body_orientation <= 135 and body_orientation >= 45:
      step = [1, 0.0, 1]
      crab = True

    avatar.body.rotateToY(body_orientation)
    mv_run += 0.3
    
    #print("ROTATION", crab, "   ", body_orientation, " ===  ", math.radians(body_orientation-180)/math.pi, "  ---  ", 1/(math.tan(math.radians(body_orientation-180)/math.pi)+1))
    """
    if craby:
      step = [1/(math.tan(math.radians(body_orientation-180)/math.pi)+1), 0.0, 1-( 1/(math.tan(math.radians(body_orientation-180)/math.pi)+1))]
    else:
      step = [1-math.tan(math.radians(body_orientation-180)/math.pi), 0.0, math.tan(math.radians(body_orientation-180)/math.pi)]
    """
  else:
    print("unhandled sensor:", sensor)


# Implement Threading to read Serial
if(USE_SERIAL):
  ser = Serial_data('ABCDEFJ', roger_handler)
  ser.start()

# Initialize Camera
if(USE_STEREO == False):
  CAMERA = pi3d.Camera(absolute=False)


def update():
  global xm, ym, zm, step, norm, roll, orientation, movement, lx, ly, lz, mv_run

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
      print(" Position : ", xm, " === ", ym, " === ",zm, " === ")
      step = [0.0, 0.0, 0.0]

  map1.myecube.position(xm, ym, zm)

  roll = 0.0
  #map1.mymap.position(0.0, 0.0, 0.0)
  #avatar.body.position(xm, mymap.calcHeight(xm, zm+distance_hero)+5.5, zm+distance_hero)
  if MAP_HALL:
    avatar.body.position(xm+3, ym-5, zm+distance_hero)
    avatar2.body.position(-10, ym-5, 15) # equivalent a -13, 15 et 0
    mystring.position(-10, ym+1.5, 15)
    myPlane.position(-10, ym+1.5, 15.05)
  else:
    #avatar.body.position(xm+3, map1.mymap.calcHeight(xm, zm+distance_hero)+2, zm+distance_hero)

    avatar2.body.position(-0, map1.mymap.calcHeight(-0, 10)+2, 10)
    avatar3.body.position(-6, map1.mymap.calcHeight(-6, 15)+5, 15)
    avatar.body.position(-3, map1.mymap.calcHeight(-3, 6)+2, 6)
    avatar4.body.position(6, map1.mymap.calcHeight(6, 8)+2, 8)
    avatar5.body.position(3, map1.mymap.calcHeight(3, 5)+2, 5)
  
  #roger.body.position(0, mymap.calcHeight(0, 28)+7, 28)
  mv_run += 0.05
  #avatar.run(mv_run)
  lx = xm
  ly = ym
  lz = zm


def update_scenario():
  global xm, ym, zm

  if -16 <= xm and xm <= -10 and 14 <= ym and ym <= 16 and -3 <= zm and zm <= 3:
    #myPlane.draw(shader)
    mystring.draw()

def draw():
  global movement
  movement += 0.2 
  """
  roger.armR.rotateToZ(-60+ 25.0 * math.sin(movement))
  roger.armR.rotateToX(0)
  roger.handR.rotateToX(40.0 * math.sin(movement))
  roger.armL.rotateToZ(-45)

  roger2.armR.rotateToZ(-60+25.0 * math.sin(movement))
  roger2.armR.rotateToX(90)
  roger2.forarmR.rotateToX(40.0 * math.sin(movement))
  roger2.armL.rotateToZ(-60)
  """
  #clash.draw(avatar2.body)
  #avatar.body.rotateToY(180)

  #roshi camera 9
  avatar5.body.draw()

  #cloud camera 9
  #avatar4.armL.rotateToZ(-60+25.0 * math.sin(movement))
  #avatar4.forarmL.rotateToZ(-60+25.0 * math.sin(movement))
  avatar4.armL.rotateToZ(135+20.0 * math.sin(movement))
  avatar4.body.rotateToY(35)
  avatar4.body.draw()

  #goku camera 9
  #avatar.armR.rotateToZ(70)
  #avatar.armL.rotateToZ(-70)
  #avatar.armR.rotateToY(0)
  #avatar.armL.rotateToY(35)
  #avatar.body.rotateToY(-55)
  avatar3.armL.rotateToZ(300)

  avatar3.armR.rotateToZ(-45)
  avatar3.armR.rotateToX(90)
  avatar3.armR.rotateToZ(-45+20.0 * math.sin(movement))
  #avatar3.handR.rotateToY(-45+40.0 * math.sin(movement))
  avatar3.body.draw()

  #Link camera 10.5
  #avatar.armR.rotateToZ(70)
  #avatar.armL.rotateToZ(-70)
  #avatar.armR.rotateToY(10)
  avatar2.armL.rotateToZ(300)

  avatar2.armR.rotateToZ(-45)
  avatar2.armR.rotateToX(90)
  avatar2.armR.rotateToZ(-45 +20.0 * math.sin(movement))
  #avatar.body.rotateToY(-55)
  avatar2.body.draw()

  #LEGO camera 9
  #avatar.head.rotateToY(65)
  avatar.armR.rotateToX(-95)
  #avatar.armL.rotateToX(+55)
  avatar.armL.rotateToX(55 + 30 * math.sin(movement))
  #avatar.body.rotateToY(-55)
  avatar.body.draw()

  #avatar2.body.draw()
  map1.mymap.draw()
  map1.myecube.draw()
  

  

def read_inputs():
  global step, crab, mymouse, my, mx, rot, tilt, keep_running

  #Press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if k == 119:  #key w forward
      step = [0.5, 0.0, 0.5]
      crab = False
    elif k == 115:  #kry s back
      step = [-0.25, 0.0, -0.25]
      crab = False
    elif k == 97:   #key a crab left
      step = [0.25, 0.0, 0.25]
      crab = True
    elif k == 100:  #key d crab right
      step = [-0.25, 0.0, -0.25]
      crab = True
    elif k == 112:  #key p picture
      pi3d.screenshot("forestWalk" + str(scshots) + ".jpg")
      scshots += 1
    elif k == 10:   #key RETURN
      mc = 0
    elif k == 27:  #Escape key
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

  rot = - mx * 0.2
  tilt = my * 0.2


def camera_update():
  global xm, ym, zm, rot, tilt, step, norm, crab
  xm, ym, zm = CAMERA.relocate(rot, tilt, point=[xm, ym, zm], distance=step, 
                              normal=norm, crab=crab, slope_factor=1.5)
  CAMERA.rotateZ(roll)


# Main loop
if(USE_STEREO):
  while engine.DISPLAY.loop_running() or engine.keep_running:
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
    camera_update()
    update()
    update_scenario()
    draw()
    read_inputs()
  print(" STOP STOP")

  


