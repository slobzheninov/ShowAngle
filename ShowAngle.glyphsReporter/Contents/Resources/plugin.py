# encoding: utf-8

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from vanilla import *
from vanilla.vanillaGroup import Group
from math import degrees, atan2
from Foundation import NSPoint, NSViewController

# Our own patched Vanilla Group class
class PatchedGroup(Group):
	nsViewClass = objc.lookUpClass("GSInspectorView")

class ShowAngle(ReporterPlugin):
	isVisible = False

	@objc.python_method
	def settings(self):
		self.menuName = 'Angle of Selection'
		self.name = 'Show Angle'

		# Create Vanilla window and group with controls
		viewWidth = 52
		viewHeight = 18
		self.angleWindow = Window((viewWidth, viewHeight))
		self.angleWindow.group = PatchedGroup((0, 0, viewWidth, viewHeight)) # Using PatchedGroup() here instead of Group()
		self.angleWindow.group.text = TextBox((3, 2, 100, 100), self.name, sizeStyle='small')
		GSCallbackHandler.addCallback_forOperation_(self, "GSInspectorViewControllersCallback")
		
	def inspectorViewControllersForLayer_(self, layer):
		return [self]

	def view(self):
		if self.isVisible:
			if Glyphs.versionNumber > 3: # Glyphs 3

				# Crashes Glyphs:
				# viewController = NSViewController.new()
				# viewController.setView_(self.angleWindow.group.getNSView())
				# return viewController
				return None
				
			else: # Glyphs 2
				return self.angleWindow.group.getNSView()
		else:
			return None			

	@objc.python_method
	def nicelyRound(self, value):
		roundedValue = round(value, 1)
		if roundedValue == int(roundedValue):
			return int(roundedValue)
		else:
			return roundedValue

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
	def reportAngle( self, layer ):
		angle = None
		selection = layer.selection
		selectionBounds = layer.selectionBounds

		if len(selection) > 1:
			# get angle of the selecition rectangle ◿
			point1 = NSPoint(selectionBounds.origin.x, selectionBounds.origin.y)
			point2 = NSPoint(selectionBounds.origin.x + selectionBounds.size.width, selectionBounds.origin.y + selectionBounds.size.height)
			angle = self.getAngle(point1, point2)
			# draw angle
			if angle is not None:
				angleString = u'◿  %s°' % angle
				# set to info panel
				self.angleWindow.group.text.set( angleString )
				self.isVisible = True
		else:
			# hide the panel
			self.isVisible = False


	@objc.python_method
	def foreground(self, layer):
		self.reportAngle( layer )