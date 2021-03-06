#!/usr/bin/env python
# Copyright 2008, 2009 Hannes Hochreiner
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.

# These lines are only needed if you don't put the script directly into
# the installation directory
import sys
# Unix
sys.path.append('/usr/share/inkscape/extensions')
# OS X
sys.path.append('/Applications/Inkscape.app/Contents/Resources/extensions')
# Windows
sys.path.append('C:\Program Files\Inkscape\share\extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex

def propStrToList(str):
	list = []
	propList = str.split(";")
	for prop in propList:
		if not (len(prop) == 0):
			list.append(prop.strip())
	return list

def propListToDict(list):
	dictio = {}

	for prop in list:
		keyValue = prop.split(":")

		if len(keyValue) == 2:
			dictio[keyValue[0].strip()] = keyValue[1].strip()

	return dictio

class JessyInk_Summary(inkex.Effect):
	def __init__(self):
		# Call the base class constructor.
		inkex.Effect.__init__(self)

		self.OptionParser.add_option('--tab', action = 'store', type = 'string', dest = 'what')

		inkex.NSS[u"jessyink"] = u"https://launchpad.net/jessyink"

	def effect(self):
		# Find the script node, if present
		for node in self.document.xpath("//svg:script[@id='JessyInk']", namespaces=inkex.NSS):
			sys.stderr.write("JessyInk script ")

			if node.get("{" + inkex.NSS["jessyink"] + "}version"):
				sys.stderr.write("version " + node.get("{" + inkex.NSS["jessyink"] + "}version") + " ")

			sys.stderr.write("installed.\n")
	
		slides = []
		masterSlide = None 

		for node in self.document.xpath("//svg:g[@inkscape:groupmode='layer']", namespaces=inkex.NSS):
			if node.get("{" + inkex.NSS["jessyink"] + "}masterSlide"):
				masterSlide = node
			else:
				slides.append(node)

		if masterSlide is not None:
			sys.stderr.write("\nMaster slide:\n")
			self.describeNode(masterSlide, "\t", "<the number of the slide>", str(len(slides)), "<the title of the slide>")

		slideCounter = 1

		for slide in slides:
			sys.stderr.write("\nSlide " + str(slideCounter) + ":\n")
			self.describeNode(slide, "\t", str(slideCounter), str(len(slides)), slide.get("{" + inkex.NSS["inkscape"] + "}label"))
			slideCounter += 1

	def describeNode(self, node, prefix, slideNumber, numberOfSlides, slideTitle):
		sys.stderr.write(prefix + "Layer name: " + node.get("{" + inkex.NSS["inkscape"] + "}label") + "\n")
		
		# Display information about transitions.
		transitionInAttribute = node.get("{" + inkex.NSS["jessyink"] + "}transitionIn")
		if transitionInAttribute:
			transInDict = propListToDict(propStrToList(transitionInAttribute))
			sys.stderr.write(prefix + "Transition in: " + transInDict["name"])

			if (transInDict["name"] != "appear") and transInDict.has_key("length"):
				sys.stderr.write(" (" + str(int(transInDict["length"]) / 1000.0) + " s)")

			sys.stderr.write("\n")

		transitionOutAttribute = node.get("{" + inkex.NSS["jessyink"] + "}transitionOut")
		if transitionOutAttribute:
			transOutDict = propListToDict(propStrToList(transitionOutAttribute))
			sys.stderr.write(prefix + "Transition out: " + transOutDict["name"])

			if (transOutDict["name"] != "appear") and transOutDict.has_key("length"):
				sys.stderr.write(" (" + str(int(transOutDict["length"]) / 1000.0) + " s)")

			sys.stderr.write("\n")

		# Display information about auto-texts.
		autoTexts = {"slideNumber" : slideNumber, "numberOfSlides" : numberOfSlides, "slideTitle" : slideTitle}
		autoTextNodes = node.xpath(".//*[@jessyink:autoText]", namespaces=inkex.NSS)
		
		if (len(autoTextNodes) > 0):
			sys.stderr.write("\n" + prefix + "Auto-texts:\n")
			
			for atNode in autoTextNodes:
				sys.stderr.write(prefix + "\t\"" + atNode.text + "\" (object id \"" + atNode.getparent().get("id") + "\") will be replaced by")
				sys.stderr.write(" \"" + autoTexts[atNode.get("{" + inkex.NSS["jessyink"] + "}autoText")] + "\".\n")

		# Collect information about effects.
		effects = {}

		for effectNode in node.xpath(".//*[@jessyink:effectIn]", namespaces=inkex.NSS):
			dictio = propListToDict(propStrToList(effectNode.get("{" + inkex.NSS["jessyink"] + "}effectIn")))
			dictio["direction"] = "in"
			dictio["id"] = effectNode.get("id")

			if not effects.has_key(dictio["order"]):
				effects[dictio["order"]] = []

			effects[dictio["order"]].append(dictio)

		for effectNode in node.xpath(".//*[@jessyink:effectOut]", namespaces=inkex.NSS):
			dictio = propListToDict(propStrToList(effectNode.get("{" + inkex.NSS["jessyink"] + "}effectOut")))
			dictio["direction"] = "out"
			dictio["id"] = effectNode.get("id")

			if not effects.has_key(dictio["order"]):
				effects[dictio["order"]] = []

			effects[dictio["order"]].append(dictio)

		order = sorted(effects.keys())
		orderNumber = 1

		# Display information about effects.
		for orderItem in order:
			sys.stderr.write("\n" + prefix + "Effect " + str(orderNumber) + " (order number " + effects[orderItem][0]["order"]  + "):\n")
		
			for item in effects[orderItem]:
				sys.stderr.write(prefix + "\tObject \"" + item["id"] + "\"")

				if item["direction"] == "in":
					sys.stderr.write(" will appear")
				elif item["direction"] == "out":
					sys.stderr.write(" will disappear")

				if item["name"] != "appear":
					sys.stderr.write(" using effect \"" + item["name"] + "\"")
					
				if item.has_key("length"):
					sys.stderr.write(" in " + str(int(item["length"]) / 1000.0) + " s")

				sys.stderr.write(".\n")

			orderNumber += 1

# Create effect instance
effect = JessyInk_Summary()
effect.affect()

