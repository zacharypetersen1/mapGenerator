from sys import argv
from PIL import Image
import Classes

#check if arguments were entered correctly
if len(argv) != 5:
	print "Incorrect amount of arguments"
	print "usage: MapGenerator <inputFileName> <outputFileName> <templateFileName> <patternSize>"
	exit(1)
	
#unpack arguments
scriptName, inputName, outputName, templateName, readPatternSize = argv
patternSize = int(readPatternSize)


#Try to load input image
try:
	inputImage = Image.open(inputName)
except IOError:
	print "Input image named: '%s' could not be found" % inputName
	exit(2)

#Try  to load template
try:
	templateFile = open(templateName)
except IOError:
	print "Template file named: '%s' could not be found" % templateName
	exit(2)

#create instance of 'patternManager' class that will oversee creation of output image
patternManager = Classes.PatternManager(patternSize)	

#Import data from template
patternManager.importTemplate(templateFile)

#create the output image
patternManager.readAndWrite(inputImage, outputName)
print 'Success!'
exit(0)