#!/usr/bin/python

import io         # used to create file streams
from io import open
import fcntl      # used to access I2C parameters like addresses

import time       # used for sleep delay and timestamps
import string     # helps parse strings

import os
import sys



class AtlasI2C:
	long_timeout = 2        	# the timeout needed to query readings and calibrations
	short_timeout = 1        	# timeout for regular commands
	default_bus = 1         	# the default bus for I2C on the newer Raspberry Pis, certain older boards use bus 0
	default_address = 99     	# the default address for the sensor
	current_addr = default_address

	def __init__(self, address=default_address, bus=default_bus):
		# open two file streams, one for reading and one for writing
		# the specific I2C channel is selected with bus
		# it is usually 1, except for older revisions where its 0
		# wb and rb indicate binary read and write
		self.file_read = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
		self.file_write = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)

		# initializes I2C to either a user specified or default address
		self.set_i2c_address(address)

	def set_i2c_address(self, addr):
		# set the I2C communications to the slave specified by the address
		# The commands for I2C dev using the ioctl functions are specified in
		# the i2c-dev.h file from i2c-tools
		I2C_SLAVE = 0x703
		fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
		fcntl.ioctl(self.file_write, I2C_SLAVE, addr)
		self.current_addr = addr

	def write(self, cmd):
		# appends the null character and sends the string over I2C
		cmd += "\00"
		self.file_write.write(cmd.encode('latin-1'))

	def read(self, num_of_bytes=31):
		# reads a specified number of bytes from I2C, then parses and displays the result
		res = self.file_read.read(num_of_bytes)         # read from the board
		if res[0] == 1: 
			# change MSB to 0 for all received characters except the first and get a list of characters
			# NOTE: having to change the MSB to 0 is a glitch in the raspberry pi, and you shouldn't have to do this!
			char_list = list(map(lambda x: chr(x & ~0x80), list(res[1:])))
			place = 0
			for i in char_list:
				if i != "\x00":
					place = place + 1
				else:
					break
			char_list_edit = char_list[:-(len(char_list)-(place))]	
			value= ''.join(char_list_edit)
			return "Command succeeded " + ''.join(char_list)     # convert the char list to a string and returns it
		else:
			return "Error " + str(res[0])

	def query(self, string):
		# write a command to the board, wait the correct timeout, and read the response
		self.write(string)

		# the read and calibration commands require a longer timeout
		if((string.upper().startswith("R")) or
			(string.upper().startswith("CAL"))):
			time.sleep(self.long_timeout)
		elif string.upper().startswith("SLEEP"):
			return "sleep mode"
		else:
			time.sleep(self.short_timeout)

		return self.read()

	def close(self):
		self.file_read.close()
		self.file_write.close()

	def list_i2c_devices(self):
		prev_addr = self.current_addr # save the current address so we can restore it after
		i2c_devices = []
		for i in range (0,128):
			try:
				self.set_i2c_address(i)
				self.read(1)
				i2c_devices.append(i)
			except IOError:
				pass
		self.set_i2c_address(prev_addr) # restore the address we were using
		return i2c_devices
		
	def select(self,string):
		if string == "ph":
			self.set_i2c_address(99)
		elif string == "orp":
			self.set_i2c_address(98)
		elif string == "do":
			self.set_i2c_address(97)
		elif string == "ec":
			self.set_i2c_address(100)
		elif string == "rtd":
			self.set_i2c_address(102)
		elif string == "pmp":
			self.set_i2c_address(103)
		elif string == "flow":
			self.set_i2c_address(104)
		else:
			print("Error, invalid chip name entered")
				
		
		return string + " selected for modification.\n"
		
def main():
	device = AtlasI2C() 	# creates the I2C port object, specify the address or bus if necessary
	
	real_raw_input = vars(__builtins__).get('raw_input', input)
	
	#Calibration Loops and Instructions for each.
	while True:
		print( "This script will loop forever. Exit with ^C or Close the window. \n")
		print("Type the name of chip to modify below. Choices: ph, orp, do, ec, rtd, pmp, flow. \nIf An invalid name is entered, ph will be modified.")
		cmd = real_raw_input("Chip Name: ")
		device.select(str(cmd))
		exit = 'Y'
		while exit == 'N':
			print("Calibration can now be performed using the Cal command. \nAll other valid Atlas Chip Commands can also be used. \n")
			brd_cmd = real_raw_input("Enter Command: ")
			if len(brd_cmd) == 0:
				print("No command entered, please try again. \n")
			else:
				try:
					print(device.query(brd_cmd))
				except IOError:
					print("Failed Device query ")
			exit = real_raw_input("Enter Y to issue more commands, or N if you wish to enter a new chip name: ")	
	
if __name__ ==  "__main__":
	main()
	
	