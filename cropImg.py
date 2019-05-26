from wand.image import Image as wi
from PIL import ImageOps
from PIL import Image
import os
import pip
import sys

def pdf2jpg(filename,source):

    pdf = wi(filename=source+'\\'+filename+'.pdf', resolution=300)
    pdfImg = pdf.convert('jpeg')
    i=1
    name=str(filename).split('.')[0]

    for img in pdfImg.sequence:
        page = wi(image=img)
        page.save(filename=source+'\\'+name+'--'+str(i)+'.jpg')
        i+=1

def cropImg(fileName,filetype,source, dest):

    if filetype == 'jpg':
        img = Image.open(source+'\\'+fileName+'.'+filetype)
    # elif filetype == 'pdf':
    #     img = Image.open('wholeImg/'+fileName+'.jpg')
    else:
        return

    xdimSize = img.size[0]
    ydimSize = img.size[1]

    xStartTL = -1
    xStartBL = -1
    xStartMid = -1
    yStartTop = 0
    xEndTR = xdimSize
    xEndBR = xdimSize
    xEndMid = xdimSize
    yEndL = ydimSize
    yEndM = ydimSize
    yEndR = ydimSize


    y=0
    tol01=0
    while y <= ydimSize and yEndM == ydimSize:
        r,g,b = img.getpixel((int(xdimSize/2),y))       
        if(r >= 254 and g >= 254 and b>= 254):
            tol01+=1
            if tol01==50:
                yEndM = y-50
        y+=1
    y=0
    tol01=0
    while y <= ydimSize and yEndL == ydimSize:
        r,g,b = img.getpixel((int(xdimSize/4),y))       
        if(r >= 254 and g >= 254 and b>= 254):
            tol01+=1
            if tol01==50:
                yEndL = y-50
        y+=1
    y=0
    tol01=0
    while y <= ydimSize and yEndR == ydimSize:
        r,g,b = img.getpixel((int(3*xdimSize/4),y))       
        if(r >= 254 and g >= 254 and b>= 254):
            tol01+=1
            if tol01==50:
                yEndR = y-50
        y+=1

    yEnd=max(yEndL,yEndR,yEndM)


    x=0
    tol1 = 0
    while x < xdimSize and xEndTR == xdimSize:
        r,g,b = img.getpixel((x,0))
        if(xStartTL ==-1 and ( r < 254 or g< 254 or b< 254)):
            xStartTL = x
        if(xStartTL != -1 and r >= 254 and g >= 254 and b>= 254):
            tol1+=1
            if(tol1 == 50):
                xEndTR = x-50
        x+=1

    x = 0
    tol2 = 0
    while x < xdimSize and xEndBR == xdimSize:
        r,g,b = img.getpixel((x,yEnd-70))
        if(xStartBL ==-1 and ( r < 254 or g< 254 or b< 254)):
            xStartBL = x
        if(xStartTL != -1 and r >= 254 and g >= 254 and b>= 254):
            tol2+=1
            if(tol2 == 50):
                xEndBR = x-50
        
        x+=1
    x = 0
    tol3 = 0
    while x < xdimSize and xEndMid == xdimSize:
        r,g,b = img.getpixel((x,int(yEnd/2)))
        if(xStartMid ==-1 and ( r < 254 or g< 254 or b< 254)):
            xStartMid = x
        if(xStartMid != -1 and r >= 254 and g >= 254 and b>= 254):
            tol3+=1
            if(tol3 == 50):
                xEndMid = x-50
        
        x+=1

    xStart = min(xStartBL,xStartTL, xStartMid)
    xEnd = max(xEndBR,xEndTR,xEndMid)

    area=(xStart,yStartTop,xEnd,yEnd)
    croppedImg = img.crop(area)
    croppedImg.save(dest+'\\'+fileName+'.jpg')

# def install(package):
#     if hasattr(pip, 'main'):
#         pip.main(['install', package])
#     else:
#         pip.main(['install', package])    

def main():

    # only need to run once to generate the directory of jpg files
    # pdf2jpg('keith.pdf')
    print("USAGE:\n python cropImg.py C:\\path\\souceDirectory C:\\path\\destinationDirectory\nDo not include \\ after source/destination ")

    source = sys.argv[1]
    dest = sys.argv[2]

    print(source,dest)

    for fn in os.listdir(source):
        filename = str(fn).split('.')[0]
        filetype = str(fn).split('.')[1]
        name = filename.split('\\')[-1]
        if filetype=='pdf':
            pdf2jpg(name,source)

    for fn in os.listdir(source):
        filename = str(fn).split('.')[0]
        filetype = str(fn).split('.')[1]
        name = filename.split('\\')[-1]
        if filetype=='jpg':
            cropImg(name,filetype,source,dest)
        
    # for fn in os.listdir('wholeImg'):
    #     filename = str(fn).split('.')[0]
    #     # filetype = str(fn).split('.')[1]
    #     cropImg(filename,'pdf')


    # cropImg('keith--6','pdf')




if __name__ == "__main__":
    # install('argh')
    main()


