from PIL import Image

#contains classes for MapGenerator

#stores all patterns and contains method that generates output image
class PatternManager(object):
	
	def __init__(self, setPatternSize):
		self.refPatterns = []
		self.drawPatterns = []
		self.patternSize = setPatternSize
		
	#append a new Reference Pattern object onto list of Reference Patterns
	def appendRefPattern(self, RGBValue, pattern):
		self.refPatterns.append(ReferencePattern(RGBValue, pattern, self.patternSize))
		
	#import all information from template to create list of Reference Patterns
	def importTemplate(self, templateFile):

		#loop through each line of the Template file
		while True:
			line = templateFile.readline()
			
			#break if reached file end
			if line == '':
				break
			elements = line.split()
			
			#store values from line
			try:
				readRed, readGreen, readBlue, patternName = elements
			except ValueError:
				print "Incorrect amount of arguments in line within Template file:"
				print "Incorrect line: %s" % line
				print "Correct Usage: <redValue> <greenValue> <blueValue> <fileName>"
				exit(3)
			red = int(readRed)
			green = int(readGreen)
			blue = int(readBlue)
			RGBValue = [red, green, blue]
			
			#use fileName to find image file of pattern
			try:
				patternFile = Image.open(patternName)
			except IOError:
				print "Could not find image file named '%s' as listed on template file" % patternName
				exit(3)
				
			#test size of image file to ensure that it matches 'pattern size'
			if patternFile.size[0] != self.patternSize:
				print "Image '%s' has incorrect width of %d pixels" % (patternName, patternFile.size[0])
				print "Pattern width must match initial parameter of %d pixels" % self.patternSize
				exit(3)
			if patternFile.size[1] != self.patternSize:
				print "Image '%s' has incorrect height of %d pixels" % (patternName, patternFile.size[1])
				print "Pattern height must match initial parameter of %d pixels" % self.patternSize
				exit(3)
			
			#editablePattern = patternFile.load()
			
			#use all collected information to append a new ReferencePattern object
			self.appendRefPattern(RGBValue, patternFile)
	
	#reads input image and uses information to write to output image
	def readAndWrite(self, inputImage, outputName):
		
		#create output image with exact pixel size it will need
		outputImage = Image.new("RGB", ( (self.patternSize-1) * inputImage.size[0], (self.patternSize-1) * inputImage.size[1]))
		
		#loop through all pixels of input image
		for w in range(0, inputImage.size[0]):
			for h in range(0, inputImage.size[1]):
			
				#get pixel color from input image
				r, g, b = inputImage.getpixel((w,h))
				thisRGBValue = [r, g, b]
				
				#scan for matching reference pattern object
				foundPattern = False
				for i in range(0, len(self.refPatterns)):
					if thisRGBValue == self.refPatterns[i].RGBValue:
						foundPattern = True
						
						#call draw function within reference pattern object
						self.refPatterns[i].draw(w,h, outputImage, self.patternSize)
						break
				
				#error check for case when no pattern was found
				if not foundPattern:
					print "Unable to find pattern that matches RGB value of '%s'" % thisRGBValue
					exit(3)
					
		#save output image
		outputImage.save("%s.png" % outputName)
			
#Stores image file of a pattern, RGB reference of pattern, and also draw function that copies pattern onto target image
class ReferencePattern(object):
	
	def __init__(self, setRGBValue, setPattern, setPatternSize):
		self.RGBValue = setRGBValue
		self.pattern = setPattern
		self.patternSize = setPatternSize
	
	#draws pattern onto target image at specified location
	def draw(self, x, y, targetImage, patternSize):
		baseX = (patternSize-1) * x
		baseY = (patternSize-1) * y
		for w in range(0, patternSize-1):
			for h in range(0, patternSize-1):
				targetImage.putpixel( (baseX + w, baseY + h), self.pattern.getpixel((w, h)) )
