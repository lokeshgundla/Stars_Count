import numpy as np
import Image
import cv2
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

custom_array = np.array([0])                   #array initialization with 0

local_x = np.array([0])                        # array initialization with 0

image = cv2.imread("image.jpg",0)         # Reading Image matrix in grayscale values
height, width=image.shape                     # Getting height and width of the image 

grayscale_array = np.array((height,width),dtype='uint8') 

if rank == 0:
        timebefore_imageread = MPI.Wtime()
        image = cv2.imread("image.jpg",0) 
        timeafter_imageread = MPI.Wtime()
        print " Time taken to open and read the image is : %r sec " %(timeafter_imageread-timebefore_imageread)
        grayscale_array = np.array(image)  #Conversion to Matrix values


Timebefore_slicingimage = MPI.Wtime()
remaining_slicing = height % size               # To slice image horizontally


if rank < remaining_slicing:
        each_rowsize = height/size             # determining each row size
        each_rowsize = rowsize + 1
else:
        each_rowsize = height/size
        

custom_array = np.array((each_rowsize,width)) 
comm.Bcast(custom_array, root=0)                  # Broadcasting the array to worker nodes
local_x = np.zeros(custom_array,dtype='uint8')
comm.Bcast(local_x, root=0)                       # Broadcasting the array to worker nodes
totalbrightsspots_count = np.array([0])

comm.Scatterv(grayscale_array,local_x,root=0)     # Scattering sliced images to worker nodes to divide the work equally

#image slicing processing

img_slicedimagenode_threshold =  cv2.adaptiveThreshold(local_x,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,59,0)   
brightspots_count_node = ((200 < img_slicedimagenode_threshold)).sum()                #Getting the sum of count of bright spots greater than 200 for each pixel through array
print " Bright Spots at Node", rank,"is ", brightspots_count_node

comm.Reduce(brightspots_count_node,totalbrightsspots_count,op=MPI.SUM,root=0) 

if comm.rank == 0:
        TimeAfterCalculationOf_SlicedImage = MPI.Wtime()
        print " Total bright spots", totalbrightsspots_count              
        print " Total time taken", TimeAfterCalculationOf_SlicedImage-Timebefore_slicingimage ,"sec"


