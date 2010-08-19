#!/usr/bin/env python

import cv
import os

class CamShiftDemo:

	def __init__(self):
		self.capture = cv.CaptureFromCAM(1)
		cv.NamedWindow( "CamShiftDemo", 1 )
		#cv.NamedWindow( "CamShiftDemo2", 1 )
		#cv.NamedWindow( "CamShiftDemo3", 1 )

	def run(self):
		hist = cv.CreateHist([180], cv.CV_HIST_ARRAY, [(0,180)], 1 )
		backproject_mode = False
		self.hue=0
		thresh = 3
		pointer_ant = False
		x_ant = 0 
		y_ant = 0 
		while True:
			pointer = False
			frame = cv.QueryFrame( self.capture )
			self.hsv = cv.CreateImage( cv.GetSize(frame) , 8 , 3)
			cv.CvtColor(frame, self.hsv, cv.CV_BGR2HSV)
			if  False:
			#if  backproject_mode:
				cv.ShowImage( "CamShiftDemo", frame )
			else :
				filtered_image = cv.CreateImage(cv.GetSize(frame), 8, 1)
				self.hue = cv.CreateImage(cv.GetSize(frame), 8, 1)
				cv.Split(frame, self.hue, None, None, None)
				cv.Threshold(self.hue, self.hue, 200, 255 , thresh)
				#cv.CalcArrBackProject( [self.hue], filtered_image, hist )
				#cv.Sobel(self.hue, filtered_image, 1, 1, 3)

				self.s = cv.CreateImage(cv.GetSize(frame), 8, 1)
				cv.Split(self.hsv, None, self.s , None, None)
				cv.Threshold(self.s, self.s, 100, 255 , thresh)

				self.h = cv.CreateImage(cv.GetSize(frame), 8, 1)
				cv.Split(self.hsv, self.h , None , None, None)
				cv.Threshold(self.h, self.h, 0, 10 , thresh)
				for x in xrange(0,self.hue.height-1):
					for y in xrange(0,self.hue.width-1):
						if not (self.hue[x,y] == 0 ):
							pointer = True
							x_ant = x
							y_ant = y
							#print x,y
				
				if pointer_ant == True and pointer == False and backproject_mode:
					self.released(x_ant,y_ant)
					#pass

				cv.ShowImage("CamShiftDemo", self.hue )
				pointer_ant = pointer 
			#self.searchFor(0, 0, 0, frame.height-1, frame.width-1)
			c = cv.WaitKey(7)
			if c == 27:
				break
			elif c == ord('b'):
				backproject_mode = not backproject_mode
			elif c == ord('+'):
				thresh = thresh +1
			elif c == ord('-'):
				thresh = thresh -1

	def released(self, x, y):
		"""what to do when release pointer"""
		if x< self.hue.height/2 :
			if y < self.hue.width/2:
				#1r cuadrant
				os.system("xterm")
			else :
				#2n cuadrant
				os.system("urxvt")
		else :
				#3r cuadrant
			if y < self.hue.width/2:
				os.system("gvim")
			else :
				#4t cuadrant
				os.system("gqview")
				
			

	def searchFor(self, hue, xmin, ymin, xmax, ymax):
		"""search for colour"""
		acc =0;
		for x in xrange(xmin,xmax):
			for y in xrange(ymin, ymax):
				#if self.hsv[x,y] == hue:
					#print x, y 
				#if self.hsv[x,y][0] < hue + 10  and self.hsv[x,y][1] >= 140 :

				#if self.hsv[x,y][0] < hue + 10  and self.hsv[x,y][0] > hue - 5 and self.hsv[x,y][1] >= 150 and self.hsv[x,y][2] > 100:
				if self.hue[x,y][0] < hue + 10  and self.hue[x,y][0] > hue - 5 and self.hue[x,y][1] >= 150 and self.hue[x,y][2] > 100:
					print x, y ,  self.hsv[x,y] 

if __name__=="__main__":
	demo = CamShiftDemo()
	demo.run()
