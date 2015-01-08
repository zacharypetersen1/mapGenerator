#contains classes used by MapGenerator script

from PIL import Image

#stores all Tiles and contains method that generates output image
class TileManager(object):
	
	def __init__(self, setTileSize):
		self.refTiles = []	#will store ReferenceTile objects
		self.tileSize = setTileSize
		
	#append a new Reference Tile object onto list of Reference Tiles
	def appendRefTile(self, RGBValue, tile):
		self.refTiles.append(ReferenceTile(RGBValue, tile, self.tileSize))
		
	#Read template file to create list of Reference Tiles
	def importTemplate(self, templateFile):

		#loop through each line of the Template file
		while True:
			line = templateFile.readline()
			
			#break if reached end of file
			if line == '':
				break
			
			#Split line into array of words
			elements = line.split()
			
			#store values from line
			try:
				readRed, readGreen, readBlue, tileName = elements
			except ValueError:
				print "Incorrect usage within Template file:"
				print "Incorrect line: %s" % line
				print "Correct Usage: <redValue> <greenValue> <blueValue> <fileName>"
				exit(3)
			red = int(readRed)
			green = int(readGreen)
			blue = int(readBlue)
			RGBValue = [red, green, blue]
			
			#find image file of Tile
			try:
				tileFile = Image.open(tileName)
			except IOError:
				print "Could not find image file named '%s' as listed on template file" % tileName
				exit(3)
				
			#test size of image file to ensure that it matches 'Tile size'
			if tileFile.size[0] != self.tileSize:
				print "Image '%s' has incorrect width of %d pixels" % (tileName, tileFile.size[0])
				print "Tile width must match initial parameter of %d pixels" % self.tileSize
				exit(3)
			if tileFile.size[1] != self.tileSize:
				print "Image '%s' has incorrect height of %d pixels" % (tileName, tileFile.size[1])
				print "Tile height must match initial parameter of %d pixels" % self.tileSize
				exit(3)
						
			#finally, create new ReferenceTile object
			self.appendRefTile(RGBValue, tileFile)
	
	#reads input image and uses this information to write to output image
	def readAndWrite(self, inputImage, outputName):
		
		#create output image with exact pixel dimensions it will need
		outputImage = Image.new("RGB", ( (self.tileSize-1) * inputImage.size[0], (self.tileSize-1) * inputImage.size[1]))
		
		#loop through all pixels of input image
		for w in range(0, inputImage.size[0]):
			for h in range(0, inputImage.size[1]):
			
				#get pixel color from input image
				r, g, b = inputImage.getpixel((w,h))
				thisRGBValue = [r, g, b]
				
				#scan for matching reference Tile object
				foundTile = False
				for i in range(0, len(self.refTiles)):
					if thisRGBValue == self.refTiles[i].RGBValue:
						foundTile = True
						
						#call draw function to draw Tile onto output image
						self.refTiles[i].draw(w,h, outputImage, self.tileSize)
						break
				
				#error check in case no Tile was found
				if not foundTile:
					print "Unable to find Tile that matches RGB value of '%s'" % thisRGBValue
					exit(3)
					
		#save output image
		outputImage.save("%s.png" % outputName)
			
#Stores image file of a Tile, RGB reference of Tile, and also draw function that copies tile onto output image
class ReferenceTile(object):
	
	def __init__(self, setRGBValue, setTile, setTileSize):
		self.RGBValue = setRGBValue
		self.tile = setTile
		self.tileSize = setTileSize
	
	#draws Tile onto output image at specified location
	def draw(self, x, y, targetImage, tileSize):
		baseX = (tileSize-1) * x
		baseY = (tileSize-1) * y
		for w in range(0, tileSize-1):
			for h in range(0, tileSize-1):
				targetImage.putpixel( (baseX + w, baseY + h), self.tile.getpixel((w, h)) )
