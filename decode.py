# Code designed and written by: Zaryab Shahzaib
# Andrew ID: zshahzai   
# File Created: September 29, 3:00pm
# Modification History:
# Start End
# 29/09 3:00pm 29/09 7:00pm
# 30/09 10:00am 30/09 3:40pm
import ImageWriter

#This function converts the input picture to Black and White
def convertBlackWhite(pic):
    #First we get the rows and columns 
    rows = ImageWriter.getHeight(pic)
    columns = ImageWriter.getWidth(pic)
    #Loop over the rows and columns and get the color of every pixel as a list, and take the average of the colors within the list.
    #If average is greater than 100, change the value to 255 i.e white, if less than 100, change the value of average to 0 i.e Black.
    for i in range(0,rows):
        for j in range(0,columns):
            c = ImageWriter.getColor(pic,j,i)
            if sum(c)/3 >= 100:
                ImageWriter.setColor(pic,j,i,[255,255,255])
            else:
                ImageWriter.setColor(pic,j,i,[0,0,0])

#This Function takes a picture as an argument and removes the border from the right.
#The basic appraoch is to first remove the border from the right using this funciton and then remove the border from the left using the main removeBorder function.                
def remfromRight(pic):
    #Get the width and height of the image.
    w = ImageWriter.getWidth(pic)
    h=  ImageWriter.getHeight(pic)
    #Loop over the whole image to convert black pixels to white.
    for y in range(h):
        #Initially we have not seen any black pixel.
        blackseen=0
        try:
            for x in range(w,0,-1):#This loop starts from the right
                color = ImageWriter.getColor(pic,x,y)
                if color == [0,0,0]:
                    blackseen=1
                    ImageWriter.setColor(pic,x,y,[255,255,255])                 
                #If we have seen a black pixel and the color is white, it means we need to change the row to the next row, so we raise an exception at this point.
                elif (blackseen==1) and (color==[255,255,255]):
                    raise Exception()
        except Exception:
            #This increments the row by 1.
            y=y+1
       
#This function combines the functionality if the previous remFromRight funciton to remove the whole border.
def removeBorder(pic):
    remfromRight(pic)
    w = ImageWriter.getWidth(pic)
    h=  ImageWriter.getHeight(pic)
    for y in range(h):
        blackseen=0
        try:
            for x in range(w):#This Loop starts from the Left
                color = ImageWriter.getColor(pic,x,y)
                if color == [0,0,0]:
                    blackseen=1
                    ImageWriter.setColor(pic,x,y,[255,255,255])                 
                elif (blackseen==1) and (color==[255,255,255]):
                    raise Exception()#If we have seen a black pixel and the color is white, it means we need to change the row to the next row, so we raise an exception at this point.
        except Exception:
            #This increments the row by 1.
            y=y+1
#This function finds the top and bottom of the biggest blob of black pixels in the image, in other words, it finds the section that contains arabia numbers             
#in the image.
def horizontalSegmentation(pic):
    inBlob =False #We have not seen a blob yet so it is False.
    w = ImageWriter.getWidth(pic)
    h=  ImageWriter.getHeight(pic)
    startOfBlob=0
    maxBlob=0
    blobstart=0
    final=[]#An empty list to store the final result
    compare=[]#This empty list is used to store all the blob sizes and compare at the end.
    for y in range(h):
        row=[]#An empty list to store all the colors in the row.
        lis=[]#An empty list to store the blob size, the start of the blob and the row value.
        #Loop over the image to to get the sizes of blobs of black pixels.
        for x in range(w):
            color = ImageWriter.getColor(pic,x,y)
            row.append(color)#Append all the colors of pixels in the row to the list.
        if ([0,0,0] in row) and inBlob==False:#If black pixel found it means the blob has started so set value to True.
            inBlob = True
            startOfBlob=y#Set the start of blob to current row.
        elif ([0,0,0] not in row) and inBlob==True:#If black not found in the colors, and inBlob is true, it means we have finished a blob so we find the size and append to the list.
            inBlob=False
            blobsize= abs(y-startOfBlob)*w
            lis.append(blobsize)
            lis.append(startOfBlob)
            lis.append(y)#this is the ending row, where the blob ends.
            final.append(lis)
    #Append all the blob sizes to the compare list so the biggest one can be found by comparing.
    for i in final:
        compare.append(i[0])
    #Find the Index of the maximum value in the list, ie the index of the max blob size.
    a= compare.index(max(compare))
    result = [final[a][1],final[a][2]]#Append the Blobstart and the ending row to the result list.
    return result 

#This function takes the start and end rows between which the numbers exists as input arguments.
#The function also takes a column number from which to start looking for the next digit.
#This function determines the position of the next number and returns the start and end column for the next digit.             
def verticalSegmentation(pic,startrow,endrow,col=0):
    w = ImageWriter.getWidth(pic)
    h=  ImageWriter.getHeight(pic)
    digitstart=0
    digitend=0
    blobstart=0
    CurrentColor=[255,255,255]
    PrevColor=[255,255,255]
    final=[]#Empty list to store the final result.
    #Loop over each columns in the horizontal segment one by one.
    for x in range(col,w):
        #We assume that there is no black pixel in the column.
        CurrentColor=[255,255,255]
        #Go through each row of this column and check if there are any black pixels.
        #We should only check between the start and end locations of the biggest blob we found
        #in previous step
        for y in range(startrow,endrow+1):
            color = ImageWriter.getColor(pic,x,y)
            if color == [0,0,0]:#If black pixel found set the current color to black.
                CurrentColor=[0,0,0]
        if CurrentColor != PrevColor:#If previous color is not equal to current color it means that either we have started a blob or we have ended a blob.
            if CurrentColor==[255,255,255]:#If current color is white previous must be black so we have ended the blob. Check the size of the blob and append to the final list
                if x-blobstart>5:
                    digitstart=blobstart
                    digitend=x-1
                    final.append(digitstart)
                    final.append(digitend)
                    return final
            PrevColor=CurrentColor#If current color is not white, it means we have started a blob, so set the value of prevcolor to black.
            blobstart=x

#This function takes a pic as input parameter and decodes the number bounded by the rectangle represented by startrow, endrow, startcol, and endcol.      
def decodeCharacter(pic,startrow,endrow,startcol,endcol):
    #Storing input arguments in variables.
    stC= startcol
    enC= endcol
    stR= startrow
    enR= endrow
    bcount=0#Initial count of Black pixels
    wcount=0#Initial Count of White pixels.
    final=[]#List to store the final percentages of black pixels in the quadrants.
    #The approach is to scan each quadrant, count the number of black and white pixels seenm, and divide the number of black pixels with the sum of black and white pixels
    #to find the percentage of black pixels in the quadrant. We append each percentage to the final list and reset the count of black and white to 0 each time we start
    #scanning a new quadrant.
    for x in range(stC+(enC-stC)/2,enC):
        for y in range(stR,stR+(enR-stR)/2):
            color = ImageWriter.getColor(pic,x,y)
            if color == [0,0,0]:
                bcount=bcount+1
            else:
                wcount=wcount+1
    final.append(float(bcount)/(bcount+wcount))
    bcount=0
    wcount=0
    for x in range(stC,(stC+(enC-stC)/2)):
        for y in range(stR,(stR+(enR-stR)/2)):
            color = ImageWriter.getColor(pic,x,y)
            if color == [0,0,0]:
                bcount=bcount+1
            else:
                wcount=wcount+1
    final.append(float(bcount)/(bcount+wcount))
    bcount=0
    wcount=0
    for x in range(stC,(stC+(enC-stC)/2)):
        for y in range(stR+(enR-stR)/2,enR):
            color = ImageWriter.getColor(pic,x,y)
            if color == [0,0,0]:
                bcount=bcount+1
            else:
                wcount=wcount+1
    final.append(float(bcount)/(bcount+wcount))
    bcount=0
    wcount=0
    for x in range(stC+(enC-stC)/2,enC):
        for y in range(stR+(enR-stR)/2,enR):
            color = ImageWriter.getColor(pic,x,y)
            if color == [0,0,0]:
                bcount=bcount+1
            else:
                wcount=wcount+1
    final.append(float(bcount)/(bcount+wcount))
    #A List to store the standard percentage values of black pixels in the four quadrants, each list represents a digit that is the index value of the list in the list.
    lis=[[0.21,0.31,0.27,0.26],[0.16,0.58,0.12,0.54],[0.38,0.80,0.33,0.23],[0.47,0.58,0.34,0.00],[0.10,0.58,0.72,0.32],[0.52,0.37,0.59,0.51],[0.45,0.44,0.04,0.43],[0.33,0.37,0.25,0.25],[0.22,0.26,0.40,0.36],[0.52,0.80,0.22,0.55]]
    AbsDiff=[]
    #A loop to append all the absolute differences of the elements of the final list, with the elements of the list which has all the standard percentage values.
    for i in lis:
        AbsDiff.append(abs((final[0]-i[0])/4) + abs((final[1]-i[1])/4) + abs((final[2]-i[2])/4) + abs((final[3]-i[3])/4))
    return AbsDiff.index(min(AbsDiff))#We returnt the index of the minimum difference, which is the number represented by the final list.    

#This fucntion combines the functionality of all the previous functions and uses them to decode a license plate. It takes a filename of a license plate image as input.
#The function then loads the image represented by filename and returns a string that represents the number on the license plate.
def decodeLicensePlate(filename):
    pic = ImageWriter.loadPicture(filename)#Load the input image file.
    lis=[]#Empty list to store the values of the decoded percentages of black pixels in the four quadrants.
    convertBlackWhite(pic)#Converts the picture to black and white
    removeBorder(pic)#Removes the borders of the image
    a = horizontalSegmentation(pic)#Stores the top and bottom of the arabia numbers in the image in the variable.
    b= verticalSegmentation(pic,a[0],a[1],0)#finds the start and end column of the first character
    c= verticalSegmentation(pic,a[0],a[1],b[1])#finds the start and end column of the seconf character
    d= verticalSegmentation(pic,a[0],a[1],c[1])#finds the start and end column of the third character
    e= verticalSegmentation(pic,a[0],a[1],d[1])#finds the start and end column of the fourth character
    f= verticalSegmentation(pic,a[0],a[1],e[1])#finds the start and end column of the fifth character
    g= verticalSegmentation(pic,a[0],a[1],f[1])#finds the start and end column of the sixth character
    lis.append(decodeCharacter(pic,a[0],a[1],b[0],b[1]))#Decodes the first character
    lis.append(decodeCharacter(pic,a[0],a[1],c[0],c[1])) #Decodes the second character
    lis.append(decodeCharacter(pic,a[0],a[1],d[0],d[1])) #Decodes the third character                         
    lis.append(decodeCharacter(pic,a[0],a[1],e[0],e[1]))#Decodes the fourth character
    lis.append(decodeCharacter(pic,a[0],a[1],f[0],f[1]))   #Decodes the fifth character 
    try:#Some license plates have only 5 characters, this checks id decoding the 6th character causes an error. If an error is caused it means that the license
        #plate has only 5 characters. 
        lis.append(decodeCharacter(pic,a[0],a[1],g[0],g[1]))
    except TypeError:#If error caused, use current characters in the list to form a string.       
        for i in range(len(lis)): #Loop to join the elements of th list into a string.
            lis[i] = str(lis[i])
        PlateNum= str("".join(lis))
        return PlateNum
    for i in range(len(lis)):#If error not caused use the 6 characters and join them to form the string.
        lis[i] = str(lis[i])
    PlateNum= str("".join(lis))
    return PlateNum #Return the final string, that contains the license plate number.                                  


