#!/bin/python


import pi3d
import math,random
import threading
from serial import Serial	


class Serial_data:

	def __init__(self, known_sensors, handler):
		self.running = True
		self.handler = handler
		serialPort = "/dev/ttyACM0"
		baudRate = 9600
		self.known_sensors = known_sensors
		self.ser = Serial(serialPort, baudRate)#, timeout=0.01, writeTimeout=0.01)
	
	def start(self):
		t = threading.Thread(target=self.perma_read_serial)
		t.deamon = True
		t.start()

	def stop(self):
		self.running = False
		self.ser.close()

	def perma_read_serial(self):
		while self.running:
			try:
				self.readSerial()
			except TypeError:
				break

	def readSerial(self):
		header = self.ser.read()
		if not header:
			return

		try:
			header = header.decode("utf-8")
		except ValueError:
			print ("Error in the value")
		except UnicodeDecodeError:
			print ("UnicodeDecodeError in the header")

		if header not in self.known_sensors:
			return

		line = self.ser.readline().strip()
		if line:
			line = line.decode("utf-8").strip(",")
			parts = line.split(",")
			if header == 'J':
				joyX = float(parts[0])
				joyY = float(parts[1])
				button = parts[2]
				self.handler(header, joyX, joyY, button)
			else:
				try:
					Euler0 = float(parts[0])
					Euler0 = ((Euler0 * 2.5)-320)/100
					Euler1 = float(parts[1])
					Euler1 = ((Euler1 * 2.5)-320)/100
					Euler2 = float(parts[2])
					Euler2 = ((Euler2 * 2.5)-320)/100
				except IndexError:
					print("Index Error in the list")
				else:
					# if no IndexError, call the handler!
					self.handler(header, Euler0, Euler1, Euler2)

		"""

		if(header == 'B'):
			line = self.ser.readline().strip()
			if line:
				line = line.decode("utf-8").strip(",")
				parts = line.split(",")
				try:
					Euler0 = float(parts[0])
					Euler0 = ((Euler0 * 2.5)-320)/100
					Euler1 = float(parts[1])
					Euler1 = ((Euler1 * 2.5)-320)/100
					Euler2 = float(parts[2])
					Euler2 = ((Euler2 * 2.5)-320)/100
					#print("Value : %d -- %d -- %d \r" % (math.degrees(Euler0), math.degrees(Euler1), math.degrees(Euler2)))

					human.armL.rotateToZ(math.degrees(-Euler2))
					human.armL.rotateToX(math.degrees(-Euler1))
					human.armL.rotateToY(math.degrees(-Euler0))
        
					pos_armL = [Euler0, Euler1, Euler2]
				except IndexError:
					print ("Index Error in the list")

		if(header == 'C'):
			line = self.ser.readline().strip()
			if line:
				line = line.decode("utf-8").strip(",")
				parts = line.split(",")
				try:
					Euler0 = float(parts[0])
					Euler0 = ((Euler0 * 2.5)-320)/100
					Euler1 = float(parts[1])
					Euler1 = ((Euler1 * 2.5)-320)/100
					Euler2 = float(parts[2])
					Euler2 = ((Euler2 * 2.5)-320)/100
					#print("Value : %d -- %d -- %d \r" % (math.degrees(Euler0), math.degrees(Euler1), math.degrees(Euler2)))

					human.armR.rotateToZ(math.degrees(-Euler2))
					human.armR.rotateToX(math.degrees(-Euler1))
					human.armR.rotateToY(math.degrees(-Euler0))

					pos_armR = [Euler0, Euler1, Euler2]
        
				except IndexError:
					print ("Index Error in the list")

		if(header == 'D'):
			line = self.ser.readline().strip()
			if line:
				line = line.decode("utf-8").strip(",")
				parts = line.split(",")
				try:
					Euler0 = float(parts[0])
					Euler0 = ((Euler0 * 2.5)-320)/100
					Euler1 = float(parts[1])
					Euler1 = ((Euler1 * 2.5)-320)/100
					Euler2 = float(parts[2])
					Euler2 = ((Euler2 * 2.5)-320)/100
					#print("Value : %d -- %d -- %d \r" % (math.degrees(Euler0), math.degrees(Euler1), math.degrees(Euler2)))

					human.handR.rotateToZ(math.degrees(-Euler2 + self.pos_armR[2]))
					human.handR.rotateToX(math.degrees(-Euler1 + self.pos_armR[1]))
					human.handR.rotateToY(math.degrees(-Euler0 + self.pos_armR[0]))
        
				except IndexError:
					print ("Index Error in the list")
		"""
