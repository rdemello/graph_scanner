print("\n\n This script requires the following libraries: \n   PIL(pillow) \n   scipy \n   matplotlib \n   pandas \n   warnings \n   os \n\n Ensure they are installed or errors will follow")

from PIL import Image
from scipy import *
from pylab import *
import os
import pandas as pd
import warnings
from scipy.signal import savgol_filter
mainDF = pd.DataFrame([])
warnings.filterwarnings("ignore", category=RuntimeWarning) 
print("\n Libraries found and loaded")

low_x = 300
high_x = 2400
low_y = 0
high_y = 1

red = 255
blue = 0
green = 0

xTitle = "Wavelength"
yTitle = "Transmission"

path = "Images"

def setAxes():
    low_x = input('\n Define minimum X Value: ')
    high_x = input(' Define maximum X Value: ')
    low_y = input(' Define minimum Y Value: ')
    high_y = input(' Define maximum Y Value: ')

    print("\n Using {}-{} for X and {}-{} for Y".format(low_x,high_x,low_y,high_y))
    return low_x, high_x, low_y, high_y

def setColours():
    red = int(input("\n Target red value (0-255): "))
    green = int(input(" Target green value (0-255): "))
    blue = int(input(" Target blue value (0-255): "))

    print("\n Using R:{}, G:{}, B:{}".format(red, green, blue))
    return red, green, blue

def smoother(xData, yData):
    # spl = make_interp_spline(xData, yData, k=3)
    # ysmooth = spl(xData)
    ysmooth = savgol_filter(yData, 51, 3)
    return ysmooth


colourSet = "n"
while colourSet!= "y":
    colourSet = input('\n Current target colour is set to \n   R:{} \n   G:{} \n   B:{} \n Proceed with current colour (y/n) or quit (q)? '.format(red, green, blue))
    if(colourSet =="n"):
        red, green, blue = setColours()
    elif(colourSet == "q"):
        quit()
    elif(colourSet == "y"):
        break


changeAxes = "n"
while changeAxes!= "y":
    changeAxes = input('\n Current axes are set to \n   X-axis: {}-{} \n   Y-axis: {}-{} \n Proceed with current scales (y/n) or quit (q)? '.format(low_x,high_x,low_y,high_y))
    if(changeAxes =="n"):
        low_x, high_x, low_y, high_y = setAxes()
    elif(changeAxes == "q"):
        quit()
    elif(changeAxes == "y"):
        break

titlesSet = "n"
while titlesSet!= "y":
    titlesSet = input('\n Current axes are titled as \n   X-axis: {}\n   Y-axis: {} \n Proceed with current titles (y/n) or quit (q)? '.format(xTitle, yTitle))
    if(titlesSet =="n"):
        xTitle = input("\n Input title for X Axis: ")
        yTitle = input("\n Input title for X Axis: ")
    elif(titlesSet == "q"):
        quit()
    elif(titlesSet == "y"):
        break

smoothData = input('\n Data smoothing is turned off by default to preserve the raw interpretted data, however it can help reduce the number of hard steps. \n WARNING: Smoothing will alter the output data. \n Smooth the data (y/n)? '.format(xTitle, yTitle))

if not os.path.exists(path):
    print('\n "Images" folder not found. Ensure folder exsists, is named correctly and is located within the same folder as this script \n')
    quit()

if(len(os.listdir(path))==0):
    print("\n No images contained in Images folder \n")
    quit()

totalImages = len(os.listdir(path))

print("\n {} images found".format(totalImages))

for x, image_path in enumerate(os.listdir(path)):   

    pos = x+1
    fileName = image_path[:-4]

    im = array(Image.open("{}/{}".format(path, image_path)))
    print("\n [{}/{}] Scanning {}".format(pos, totalImages, fileName))

    hh = im.shape[0]
    ww = im.shape[1]

    Col = array([red,green,blue,255])

    yax = linspace(0,1,hh)
    xax = linspace(300,2400,ww)

    for i in range(hh):
        for j in range(ww):
            im[i,j,:] = 255*(all(im[i,j,:]==Col))

    mapim = abs(im[:,:,0]/255-1).astype(bool)
    mapim = ~mapim
    ryax = yax[::-1]
    yval = array([average(list(compress(mapim[:,t], ryax))) for t in range(ww)])

    table = [xax,yval]
    table = np.transpose(table)
    table = table[~np.isnan(table).any(axis=1)]
    

    if(smoothData=="y"):
        table = np.transpose(table)
        yval = smoother(table[0], table[1])
        newTable = [table[0],yval]
        newTable = np.transpose(newTable)
    else:
        newTable = table

    title = array([fileName + " " + xTitle,fileName + " " + yTitle])
    thisDF = pd.DataFrame(newTable)
    thisDF.columns = title 
    mainDF = pd.concat([mainDF, thisDF], axis=1)
    print(" [{}/{}] Closing {}".format(pos, totalImages, fileName))

chosenFileName = input('\n Type desired filename, or hit enter to use default "Results": ')

if(len(chosenFileName)<1):
    chosenFileName = "Results"

print("\n Writing to {}.csv".format(chosenFileName))
mainDF.to_csv('{}.csv'.format(chosenFileName))
print("\n Completed! \n\n")