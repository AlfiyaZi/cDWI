#!/usr/bin/python
# Program to import a cine set of cardiac images and find the optimal trigger delay
# Optimal delay can be used as trigger delay for cardiac DWI
# The code runs stand alone but it can be used with a wrapper script on the MRI scanner
# Mahdi S. Rahimi, 2014
import dicom
import numpy
import math
import os
import sys

# finds the most quiescent trigger delay based on a list of cineFiles and a known heart rate. 
def findOptimalTriggerDelay(cineFiles):
    maxEntropy = 0
    maxEntropyDelay = 0
    for index, dicomFileName in enumerate(sorted(listdir_fullpath(cineFiles))):
        # print dicomFileName
        dicomImage = dicom.read_file(dicomFileName, force = True)
        current_image = dicomImage.pixel_array
        if index == 0 :
            # first image to be read
            previous_image = dicomImage.pixel_array
            continue
        imageEntropy = entropy (abs(current_image - previous_image))
        previous_image = current_image
        if imageEntropy > maxEntropy:
            maxEntropy = imageEntropy
            maxEntropyDelay = dicomImage[0x18,0x1060].value # Trigger delay DICOM tag
    return maxEntropyDelay


# copied from stackoverflow to get the full path of directory lisitng
def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

# Calculates the entropy of an image. Code copied mostly from brainacle.com code snippet. 
def entropy (img):
    histogram = numpy.histogram(img)
    historgam_length = histogram[0].sum()
    samples_probability = [float(h) / historgam_length for h in histogram[0]]
    return -sum([p * math.log(p, 2) for p in samples_probability if p != 0])

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():
    args = sys.argv
    if len(sys.argv) != 2:
        print 'using default test files'
        cineFiles = '/Users/mahdi/Documents/volunteer.20140903/294_09032014/005/'
    else:
        cineFiles = args[1]
        print 'cine files are located at ', cineFiles
    print 'Optimal trigger delay is ', findOptimalTriggerDelay(cineFiles)

if __name__ == '__main__':
    main()




         

