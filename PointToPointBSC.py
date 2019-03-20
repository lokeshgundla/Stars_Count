import numpy as np
import time
from mpi4py import MPI
import cv2
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
	timebefore_readingimage= time.time()
	image = cv2.imread("image.jpg",0)
	height, width=image.shape
	height = height/size
	width = width/size
	timeafter_readingimge = time.time()
	print " Time taken to open and read the image is : %r sec " %(timeafter_readingimge-timebefore_readingimage) 
	print " sending the image slices to different nodes "   # size of image is send to different nodes
	timebefore_slicedimage = time.time()                                        # time before slicing images and send to different node for compuatation using point to point communication
	image_node1 = image[height,width]                            # sliced the first part of image
	comm.send(image[:height,(width):(width*2)], dest=1, tag=11)             # overlapping of images so that boundary values are cpvered
	comm.send(image[:height,(width*2):(width*3)], dest=2, tag=11)
	comm.send(image[:height,(width*3):(width*4)], dest=3, tag=11)
	comm.send(image[:height,(width*4):(width*5)], dest=4, tag=11)
	comm.send(image[:height,(width*5):(width*6)], dest=5, tag=11)
	comm.send(image[:height,(width*6):(width*7)], dest=6, tag=11)
	comm.send(image[:height,(width*7):(width*8)], dest=7, tag=11)
	comm.send(image[:height,(width*8):(width*9)], dest=8, tag=11)
	comm.send(image[:height,(width*9):(width*10)], dest=9, tag=11)
	


        image_node_thresh1 =  cv2.adaptiveThreshold(image_node1,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,59,0) 
	brightspots_count = [0,1,2,3,4,5,6,7,8,9]
	brightspots_count[0] = ((200 < image_node_thresh1)).sum()
	
	
	C_dictionary1 = {}
	#C_dictionary2 = {}
	C_dictionary1[0] = image_node_thresh1
	
	# Receiving the count of the stars from all the nodes	
	brightspots_count[1] = comm.recv(source=1, tag=15)
	print "Bright spots count received from node 1"
	brightspots_count[2] = comm.recv(source=2, tag=15)
	print "Bright spots count received from node 2"
	brightspots_count[3] = comm.recv(source=3, tag=15)
	print "Bright spots count received from node 3"
	brightspots_count[4] = comm.recv(source=4, tag=15)
	print "Bright spots count received from node 4"
	brightspots_count[5] = comm.recv(source=5, tag=15)
	print "Bright spots count received from node 5"
	brightspots_count[6] = comm.recv(source=6, tag=15)
	print "Bright spots count received from node 6"
	brightspots_count[7] = comm.recv(source=7, tag=15)
	print "Bright spots count received from node 7"
	brightspots_count[8] = comm.recv(source=8, tag=15)
	print "Bright spots count received from node 8"
	brightspots_count[9] = comm.recv(source=9, tag=15)
	print "Bright spots count received from node 9"
	timeafter_slicedimage = time.time()
	print " The total number of stars : %s " %(sum(brightspots_count))
	print " Time taken to count the stars : %r sec " %(timeafter_slicedimage-timebefore_slicedimage)
	
	
	C_dictionary1[0] = comm.recv(source=1, tag=13)
	print "received result from node 1"
	C_dictionary1[1] = comm.recv(source=2, tag=13)
	print "received result from node 2"
	C_dictionary1[1] = comm.recv(source=3, tag=13)
	print "received result from node 3"
	C_dictionary1[2] = comm.recv(source=4, tag=13)
	print "received result from node 4"
	C_dictionary1[2] = comm.recv(source=5, tag=13)
	print "received result from node 5"
	C_dictionary1[3] = comm.recv(source=6, tag=13)
	print "received result from node 6"
	C_dictionary1[3] = comm.recv(source=7, tag=13)
	print "received result from node 7"
	C_dictionary1[4] = comm.recv(source=8, tag=13)
	print "received result from node 8"
	C_dictionary1[4] = comm.recv(source=9, tag=13)
	print "received result from node 9"


	
	

 
	for i in range(10):
		if i > 0:
			img_process = np.hstack((img_process,C_dictionary1[i]))
		else :
			img_process = C_dictionary1[i]	
   	print " The size of the reconstructed image from all the nodes is  "
	print img_process.shape
	
	
	timetakenbeforeto_countbrightspots_insinglenode = time.time()
	img_node_thresh1 =  cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,59,0) 
	total_brightspots_count = ((200 < img_node_thresh1)).sum()
	timetakenafterto_countbrightspots_insinglenode = time.time()
	print " Time taken to count the bright spots in single node : %r sec " %(timetakenafterto_countbrightspots_insinglenode-timetakenbeforeto_countbrightspots_insinglenode)
	print " The bright spots count when used serial algo is : %r " %(total_brightspots_count)
	

else:
	B_local = comm.recv(source=0, tag=11)	
	print "at Node %r received matrix of shape %s " %(rank, B_local.shape )
        img_node_thresh =  cv2.adaptiveThreshold(B_local,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,59,0)	
        brightspots_count_node = ((200 < img_node_thresh)).sum()
	comm.send(brightspots_count_node,dest=0, tag=15)
	print "sent back the bright spots count %s" %(rank)
	comm.send(img_node_thresh, dest=0, tag=13)
	
	
