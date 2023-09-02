# encoding: utf-8

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from vanilla import *
from vanilla.vanillaGroup import Group
from math import degrees, atan2
from Foundation import NSPoint, NSViewController, NSMaxX, NSMaxY

# Our own patched Vanilla Group class
class PatchedGroup(Group):
	nsViewClass = objc.lookUpClass("GSInspectorView")

class ShowAngleAndDistance(GeneralPlugin):
	
	@objc.python_method
	def settings(self):
		self.isVisible = False
		self.state = False
		self.menuName = 'Angle & Distance of Selection'
		self.name = 'Show Angle And Distance'

		# Create Vanilla window and group with controls
		viewWidth = 60
		viewHeight = 40
		self.angleWindow = Window((viewWidth, viewHeight))
		self.angleWindow.group = PatchedGroup((0, 0, viewWidth, viewHeight)) # Using PatchedGroup() here instead of Group()

		if Glyphs.versionNumber >= 3: # Glyphs 3, auto size
			self.angleWindow.group.text = TextBox("auto", self.name)
			try:
				rules = [
					"H:|-6-[text]-8-|",
					"V:|-5-[text]-5-|",
				]
				self.angleWindow.group.addAutoPosSizeRules(rules)

			except Exception as e:
				import traceback
				print(traceback.format_exc())
		
		else: # Glyphs 2, manual size because there's something wrong with auto sizing
			# self.angleWindow.group.text = TextBox((3, 2, 100, 100), self.name, sizeStyle='small')
			self.angleWindow.group.text = TextBox((3, 6, 100, 100), self.name, sizeStyle='small')

		GSCallbackHandler.addCallback_forOperation_(self, "GSInspectorViewControllersCallback")
		
		
	@objc.python_method
	def start( self ):
		self.loadPreferences()
		menuItem = NSMenuItem( self.menuName, self.toggleMenu_ )
		Glyphs.menu[VIEW_MENU].append( menuItem )
		Glyphs.menu[VIEW_MENU].submenu().itemWithTitle_(self.menuName).setState_( self.state )
		Glyphs.addCallback(self.drawForeground, DRAWFOREGROUND)
	
	def toggleMenu_(self, sender):
		currentState = Glyphs.menu[VIEW_MENU].submenu().itemWithTitle_(self.menuName).state()
		self.state = not currentState
		Glyphs.menu[VIEW_MENU].submenu().itemWithTitle_(self.menuName).setState_( self.state )
		self.savePreferences()
	
	@objc.python_method
	def savePreferences( self ):
		try:
			Glyphs.defaults['com.slobzheninov.ShowAngleAndDistance.menu'] = self.state
		except:
			import traceback
			print('Could not save preferences')
			print(traceback.format_exc())
			return False
		return True

	@objc.python_method
	def loadPreferences( self ):
		try:
			self.state = Glyphs.defaults['com.slobzheninov.ShowAngleAndDistance.menu']
			if not self.state: self.state = False
		except:
			import traceback
			print(traceback.format_exc())



	def inspectorViewControllersForLayer_(self, layer):
		if self.state and self.isVisible:
			return [self]
		return []

	def view(self):
		return self.angleWindow.group.getNSView()

	@objc.python_method
	def nicelyRound(self, value):
		roundedValue = round(value, 1)
		if roundedValue == int(roundedValue):
			return int(roundedValue)
		else:
			return roundedValue
	@objc.python_method
	def getDist(self, point1, point2):
		distance = ((point2.x - point1.x)**2 + (point2.y - point1.y)**2)**0.5 
		return(self.nicelyRound(distance))

	@objc.python_method
	def getAngle(self, point1, point2):
		# Calculate the x and y distances between the points
		dx = point2.x - point1.x
		dy = point2.y - point1.y
		# Calculate the angle in radians using arctan2
		angle_radians = atan2(dy, dx)

		# Convert the angle to degrees and adjust for upright and horizontal angles
		angle_degrees = degrees(angle_radians)
		angle_degrees = 90 - angle_degrees
		# Ensure the angle is in the range [0, 360)
		if angle_degrees < 0:
			angle_degrees += 360

		# Round
		angle_degrees = self.nicelyRound(angle_degrees)
		# Return the angle in degrees
		return angle_degrees

	@objc.python_method
	def reportAngle(self, layer):
		selection = layer.selection
		if len(selection) > 1:
			angle = None
			selectionBounds = layer.selectionBounds
			# get angle of the selecition rectangle ◿
			point1 = selectionBounds.origin
			point2 = NSPoint(NSMaxX(selectionBounds), NSMaxY(selectionBounds))
			angle = self.getAngle(point1, point2)
			distance = self.getDist(point1, point2)
			
			# report angle and distance
			if angle is not None:
				# angleString = u'◿  %s°' % angle
				angleString = u'◿  %s°\n⤢  %s' % (angle, distance)
				# set to info panel
				self.angleWindow.group.text.set(angleString)
				self.isVisible = True
		else:
			# hide the panel
			self.isVisible = False


	@objc.python_method
	def drawForeground(self, layer, info):
		self.reportAngle(layer)