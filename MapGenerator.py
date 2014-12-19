#This program takes a 'input image' and template as input (along with some specifications)
#Then generates a textured background image

#each pixel on the 'input image' represents a square pattern on the output image
#The template determines which pixels map to which pattern based on color values

#usage: MapGenerator <inputFileName> <outputFileName> <templateFileName> <patternSize>
#do not add .png extension to output file name, program will do this automatically
#exit conditions: 0 = fine, 1 = illegal arguments, 2 = file not found (from args), 3 = read error/file not found (from template file)

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

#create instance of class that will oversee program
patternManager = Classes.PatternManager(patternSize)	

#Import data from template
patternManager.importTemplate(templateFile)

#create the output image
patternManager.readAndWrite(inputImage, outputName)
print 'Success!'
exit(0)