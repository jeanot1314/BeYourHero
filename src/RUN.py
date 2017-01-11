#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import math,random
import pi3d
import avatars
import maps
import building
import objects
import inputs
import os

#import sys
#from serial_data import Serial_data
#sys.path.insert(0, "../python-vrzero")
from vrzero import engine


################ Select the mode here ###########
USE_SERIAL = False # try the app without a serial connection, keyboard still work
USE_STEREO = False # Mode Stereoscopic
USE_TUNNEL = True # If mode stereo is on, use Tunnel effect

############ Use a more simple sensor movement like on the Wii remote ########
SIMPLE_MOVE = True

################ Select your map : moon or forest ##########
MAP = 'temple'

################ Select your Avatars here (you can manualy add more) #########
AVATAR_1 = 'Link'
ENEMIS_2 = 'Goomba'
AVATAR_3 = 'toad'

################ Show stat on terminal #############
SHOW_STAT = False # Show FPS stat (Calibrated for Raspberry Pi)

################ Change screen size to adapt your config ################
DEFAULT_SCREEN_WIDTH=600 # 0 for full screen
DEFAULT_SCREEN_HEIGHT=400 # 0 for full screen
DEFAULT_EYE_SEPERATION=0.65

# height of the camera
DEFAULT_AVATAR_EYE_HEIGHT = 4.0
DEFAULT_AVATAR_MOVEMENT_SPEED = 1.2

#os.system('xset r off')
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
  CAMERA = pi3d.Camera(absolute=True)

# initialize inputs
handler = inputs.handlers()

# Implement Threading to read Serial
if(USE_SERIAL):
  handler.serial()
#========================================

# Create Hero & map, Select your avatars here
if AVATAR_1 == 'Link':
  avatar = avatars.link()
  avatarstereo = avatars.linkstereo()
  avatar1_3 = avatars.goombaD()
elif AVATAR_1 == 'Cloud':
  avatar = avatars.cloud()
elif AVATAR_1 == 'Lego':
  avatar = avatars.lego()
  avatarstereo = avatars.lego()
elif AVATAR_1 == 'Roshi':
  avatar = avatars.roshi()
elif AVATAR_1 == 'Goku':
  avatar = avatars.goku()
elif AVATAR_1 == 'Goomba':
  avatar = avatars.goomba()

if ENEMIS_2 == 'Link':
  enemis = [avatars.link(), avatars.link(), avatars.link(), avatars.link()]
elif ENEMIS_2 == 'Cloud':
  enemis = avatars.cloud()
elif ENEMIS_2 == 'Lego':
  enemis = avatars.lego()
elif ENEMIS_2 == 'Roshi':
  enemis = avatars.roshi()
elif ENEMIS_2 == 'Goku':
  enemis = avatars.goku()
  enemisD = avatars.goombaD()
elif ENEMIS_2 == 'Goomba':
  enemis = [avatars.goomba(), avatars.goomba(), avatars.goomba(), avatars.goomba()]
  enemisD = [avatars.goombaD(), avatars.goombaD(), avatars.goombaD(), avatars.goombaD()]
elif ENEMIS_2 == 'toad':
  enemis = avatars.toad()
  enemisD = avatars.goombaD()

if AVATAR_3 == 'Link':
  avatar3 = avatars.link()
elif AVATAR_3 == 'Goomba':
  avatar3 = avatars.goomba()
  avatar3_3 = avatars.goombaD()
elif AVATAR_3 == 'Goku':
  avatar3 = avatars.goku()
  avatar3_3 = avatars.goombaD()
elif AVATAR_3 == 'toad':
  avatar3 = avatars.toad()
  avatar3_3 = avatars.goombaD()

if MAP == 'forest':
  map1 = maps.forest()
elif MAP == 'moon':
  map1 = maps.moon()
elif MAP == 'temple':
  map1 = maps.templeoftime()
elif MAP == 'kokiri':
  map1 = maps.kokiri()

bulle = objects.object()
TEXTURE = pi3d.Texture('../textures/Raspi256x256.png')
SHADER = pi3d.Shader('uv_flat')
#size = random.uniform(0.5, 2.5)

life = [pi3d.ImageSprite(texture=TEXTURE, shader=SHADER, w=1, h=1), pi3d.ImageSprite(texture=TEXTURE, shader=SHADER, w=1, h=1), pi3d.ImageSprite(texture=TEXTURE, shader=SHADER, w=1, h=1), pi3d.ImageSprite(texture=TEXTURE, shader=SHADER, w=1, h=1), pi3d.ImageSprite(texture=TEXTURE, shader=SHADER, w=1, h=1)]
life_pos = [-1.2, -0.6, 0, 0.6, 1.2]
#life.position(5, 5, 0)
#DISPLAY.add_sprites(life)

# variables
synchro_serial=0
camera_distance = -20
keep_running = True

# camera position
stereo_rot = 0.0
stereo_tilt = 0.0
stereo_roll = 0.0

# Other Avatar
xm_enemis = [-20.0, 0.0, 20.0, 0.0]
zm_enemis = [80.0, 70.0, 60.0, 30.0]
xm_av3 = 0.0
zm_av3 = 100.0
flag_choc_av = 0
flag_choc_enemis = [0, 0, 0, 0]
flag_choc_av3 = 0
mv_enemis = [1.0, 0.5, 6.0, 30.0]
mv_enemis_diff = [0.0, 0.0, 0.0, 0.0]
mv_avatar3 = 0.0
mv_avatar3_diff = 0.0
life_av = 5
life_enemis = [2, 2, 2, 2]
life_av3 = 2
#============================================================================================================

def update_position():
  global xm_enemis, zm_enemis, xm_av3, zm_av3
  #print( xm, zm, map1.height(xm, zm))
  jump, cut, protect= handler.actionRead()
  xm, zm, body_orientation, mv, mv_diff, flag_view = handler.position()
  #print(body_orientation)
  if flag_view:
    avatar.center.position(xm, map1.height(xm, zm) + 2*math.sin(jump/8), zm)
    avatar.center.rotateToY(body_orientation)
  else:
    avatarstereo.center.position(xm, map1.height(xm, zm) + 2*math.sin(jump/8), zm)
    avatarstereo.center.rotateToY(body_orientation)
  for i in range(0,4):
    enemis[i].center.position(xm_enemis[i], map1.height(xm_enemis[i], zm_enemis[i]), zm_enemis[i])
    enemisD[i].center.position(xm_enemis[i], map1.height(xm_enemis[i], zm_enemis[i]), zm_enemis[i])

  #enemis.center.position(xm_enemis[0], map1.height(xm_enemis[0], zm_enemis[0]), zm_enemis[0])
  #enemisD.center.position(xm_enemis[0], map1.height(xm_enemis[0], zm_enemis[0]), zm_enemis[0])
  avatar3.center.position(xm_av3, map1.height(xm_av3, zm_av3), zm_av3)
  avatar3_3.center.position(xm_av3, map1.height(xm_av3, zm_av3), zm_av3)

  bulle.myplane.position(xm, map1.height(xm, zm)+9, zm)


  for i in range(0,5): 
    if flag_view: 
      life[i].position(xm+life_pos[i], map1.height(xm, zm)+8, zm)
    else:
      life[i].position(xm+life_pos[i], map1.height(xm, zm)+6, zm+2)

  map1.update_pos(xm, zm)


def update_avatar():
  global xm_enemis, zm_enemis, xm_av3, zm_av3, synchro_serial, mv_enemis, mv_avatar3, flag_choc_av, flag_choc_enemis, flag_choc_av3, life_av, life_enemis, life_av3

  xm, zm, body_orientation, mv_run, mv_run_diff, flag_view = handler.position()
  jump, cut, protect = handler.action_update()

  if mv_run_diff:
    avatar.run(mv_run, mv_run_diff)
    synchro_serial=10
  if cut >= 1:
    avatar.cut(cut)
    avatarstereo.cut(cut)

  if protect >= 1:
    avatar.armR.rotateToZ(60) # half a move
    avatar.armR.rotateToY(-70) # half a move
    avatar.forarmR.rotateToZ(70) # half a move
    avatarstereo.armR.rotateToZ(60) # half a move
    avatarstereo.armR.rotateToY(-70) # half a move
    avatarstereo.forarmR.rotateToZ(30) # half a move
  else:
    #avatar.armR.rotateToZ(0) # half a move
    avatar.armR.rotateToY(0) # half a move
    avatar.forarmR.rotateToZ(0) # half a move
    #avatarstereo.armR.rotateToZ(0) # half a move
    avatarstereo.armR.rotateToY(0) # half a move
    avatarstereo.forarmR.rotateToZ(0) # half a move
  if jump:
    pass

  # if we are standing
  if(synchro_serial == 1):
    avatar.stand()
    #avatar.pose()

  if (synchro_serial > 0): 
    synchro_serial -=1
  mv_run_diff=0
  xm_enemis_tmp = 0.0  
  for i in range(0,4):
    if life_enemis[i] > 0:
      mv_enemis[i] += 0.04
      xm_enemis_tmp = xm_enemis[i] - (0.4*math.sin(mv_enemis[i]))
      xm_enemis[i] = xm_enemis_tmp
      enemis[i].run(mv_enemis[i]*3, 1)
      if math.cos(mv_enemis[i]) <= math.cos(mv_enemis[i] - 0.02):
        enemis[i].center.rotateToY(90)
      else:
        enemis[i].center.rotateToY(270)

  if life_av3 > 0:
    mv_avatar3 += 0.04
    zm_av3_tmp = zm_av3 - (0.4*math.sin(mv_avatar3))
    zm_av3 = zm_av3_tmp
    avatar3.run(mv_avatar3*4, 1)
    if math.cos(mv_avatar3) <= math.cos(mv_avatar3 - 0.02):
      avatar3.center.rotateToY(0)
    else:
      avatar3.center.rotateToY(180)

  if flag_choc_av:
    flag_choc_av -= 1
  if flag_choc_av3:
    flag_choc_av3 -= 1

  for i in range(0,4):
    if flag_choc_enemis[i]:
      flag_choc_enemis[i] -= 1
    distance_choc_av = 5
    distance_choc_enemis = 2
    distance_choc_av3 = 2

    if xm_enemis[i] - distance_choc_av <= xm and xm <= xm_enemis[i] + distance_choc_av and zm_enemis[i] - distance_choc_av <= zm and zm <= zm_enemis[i] + distance_choc_av:
      #bulle.myplane.draw()

      if cut and not flag_choc_enemis[i] and life_enemis[i] > 0:
        life_enemis[i] -= 1
        flag_choc_enemis[i] = 19

    if xm_enemis[i] - distance_choc_enemis <= xm and xm <= xm_enemis[i] + distance_choc_enemis and zm_enemis[i] - distance_choc_enemis <= zm and zm <= zm_enemis[i] + distance_choc_enemis:
      life_av -= 1
      flag_choc_av = 19
      if xm_enemis[i] - distance_choc_enemis <= xm and xm <= xm_enemis[i]:
        handler.position_upd(-5,0)
      elif xm_enemis[i] <= xm and xm <= xm_enemis[i] + distance_choc_enemis:
        handler.position_upd(5,0)
      if zm_enemis[i] - distance_choc_enemis <= zm and zm <= zm_enemis[i]:
        handler.position_upd(0,-5)
      elif zm_enemis[i] <= zm and zm <= zm_enemis[i] + distance_choc_enemis:
        handler.position_upd(0,5)

  if xm_av3 - distance_choc_av <= xm and xm <= xm_av3 + distance_choc_av and zm_av3 - distance_choc_av <= zm and zm <= zm_av3 + distance_choc_av:
    #bulle.myplane.draw()

    if cut and not flag_choc_av3 and life_av3 > 0:
      life_av3 -= 1
      flag_choc_av3 = 19

  if xm_av3 - distance_choc_av3 <= xm and xm <= xm_av3 + distance_choc_av3 and zm_av3 - distance_choc_av3 <= zm and zm <= zm_av3 + distance_choc_av3:
    life_av -= 1
    flag_choc_av = 19

    if xm_av3 - distance_choc_av3 <= xm and xm <= xm_av3:
      handler.position_upd(-5,0)
    elif xm_av3 <= xm and xm <= xm_av3 + distance_choc_av3:
      handler.position_upd(5,0)
    if zm_av3 - distance_choc_av3 <= zm and zm <= zm_av3:
      handler.position_upd(0,-5)
    elif zm_av3 <= zm and zm <= zm_av3 + distance_choc_av3:
      handler.position_upd(0,5)
  #print(life_enemis[0]+life_av3)

def draw():
  global flag_choc_av, life_av,flag_choc_enemis, life_enemis,flag_choc_av3, life_av3
  #print(flag_choc_av)
  flag_view = handler.view()

  if life_av > 0:
    if not (flag_choc_av % 2):
      if flag_view:
        avatar.center.draw()
      else:
        pass
        avatarstereo.center.draw()
  else:
    pass
    #avatar1_3.center.draw()
  for i in range(0,4):
    if life_enemis[i] > 0:
      if not (flag_choc_enemis[i] % 2):
        enemis[i].center.draw()
    else:
      enemisD[i].center.draw()

  if life_av3 > 0:
    if not (flag_choc_av3 % 2):
      avatar3.center.draw()
  else:
    avatar3_3.center.draw()

  if not (life_av3):
    bulle.myplane.draw()

  for i in range(0,life_av):  
    life[i].draw()

  map1.draw()


def camera_update():
  global stereo_rot, stereo_tilt, stereo_roll

  rot, tilt = handler.rotation()
  xm, zm, body_orientation, mv, mv_diff, flag_view = handler.position()
  roll = 0

  if(USE_STEREO):
    #print(rot, stereo_rot, tilt, stereo_tilt)
    #print(body_orientation)
    #print(flag_view)      
    if flag_view:
      tilt = 8
      CAMERA.move_camera([xm, map1.height(xm, zm)+12, zm+camera_distance], rot+stereo_rot, -tilt-stereo_tilt, -stereo_roll)

    else:
      rot = -body_orientation#+180
      CAMERA.move_camera([xm, map1.height(xm, zm)+5, zm], rot + stereo_rot, -tilt-stereo_tilt, -stereo_roll)

    #stereo_rot = rot
    stereo_tilt = tilt
    stereo_roll = roll

    for i in range(2):
      CAMERA.start_capture(i)
      draw()
      CAMERA.end_capture(i)
    CAMERA.draw()

  else:
    if flag_view:
      camRad = [camera_distance, camera_distance, camera_distance]
      #rot = -body_orientation+180

    else:
      camRad = [0, 0, 0]
      rot = -body_orientation+180
    #tilt = 15
    CAMERA.relocate(rot, -tilt, point=[xm, map1.height(xm, zm)+5, zm], distance=camRad)
    draw()

# Main loop
while DISPLAY.loop_running() and keep_running:
  handler.mykeys.do_input_events()
  update_position()
  update_avatar()
  camera_update()
  handler.update()
  #engine.stats()
  keep_running = handler.read_exit()

DISPLAY.destroy()
DISPLAY.stop()



