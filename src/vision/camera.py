import os
import sys
import cv2
import numpy as np
import utils

import random
from scipy import ndimage  #seulement parce que imread de OpenCV retourne "None" au lieu d'une liste



class Camera:

   is_somebody=0
   
   coor_X = 0
   coor_Y = 0
   def __init__(self, imagePath, cascadePath):
          	
          
          self._cascadePath= cascadePath
          self._imagePath=imagePath
          
               
   
   def _runCaptureLoop(self):
        
        if len(sys.argv) < 3:
             print "USAGE: Face_Recognition.py </path/to/images> <path/to/cascadefile>"
             sys.exit()
         
        print "  cliquer sur 'Echap' pour quitter"
        print "  cliquer sur 'a' pour ajouter une image a la base de donnees"
        print "  cliquer sur 't' pour retenir le modele"
    
        # si le dossier n'existe pas, on le cree
        imgdir=self._imagePath        
        try:
            os.mkdir(imgdir)
        except:
            pass # le chemin existe deja

        # taille des images dans la bdd

    
         # open the webcam
       
        cam = cv2.VideoCapture(0)
        		
        if ( not cam.isOpened() ):
           print "camera non detectee!"
           sys.exit()      
        print "camera detectee!."         
    
        # load the cascadefile:
        cascadePath= self._cascadePath
        cascade = cv2.CascadeClassifier(cascadePath)
        if ( cascade.empty() ):
            print "aucune cascade precisee!"
            sys.exit()         
        print "cascade:",cascadePath
    
         
        faceSize= (90, 90)
        model= cv2.createLBPHFaceRecognizer(threshold=70.0)	
        
        		
        images,labels,names = utils.retrain(imgdir,model,faceSize)
        print "Nouvel etat:",len(images),"images",len(names),"personnes"
        while True:
             	  
             ret, img = cam.read()
             			 
             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		     #a voir si c'est necessaire
             gray = cv2.equalizeHist(gray)
             # dectection de visage
             rects = cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(40, 40), flags=cv2.cv.CV_HAAR_SCALE_IMAGE) #flags = cv2.CASCADE_SCALE_IMAGE     
        
             # ne prend que la region de l'image qui nous interesse (le visage)
             roi = None
             for x, y, w, h in rects:
                 # crop & resize it 
                 roi = cv2.resize( gray[y:y+h, x:x+h], faceSize )
                 #calcule les coordonnees du rectangle et les affiche
                 xCentre1=(2*x+w)/2
	         yCentre1=(2*y+h)/2  
	         xCentre=str(xCentre1)
	         yCentre=str(yCentre1)
	         centre="("+xCentre+":"+yCentre+")"
	    
                 cv2.rectangle(img, (x,y),(x+w,y+h), (0,255,0),2)
                 if len(images)>0:
                
                    [p_label, p_confidence] = model.predict(np.asarray(roi))
                    name="unknown"
                    if p_label !=-1 : name = names[p_label]
                    cv2.putText( img, "%s %.2f %.2f" % (name,p_confidence,p_label),(x+10,y+20), cv2.FONT_HERSHEY_PLAIN,1.5, (0,255,0))
                 break # use only 1st detected
             cv2.imshow('Face Recognition For Poppy', img)
             k = cv2.waitKey(5) & 0xFF
        
             # quitter avec Echap
             if k == 27: break
       
             # on clique sur 'a' et on ajoute la personne a la bdd
             if (k == 97) and (roi!=None): 
                 print "Entrer le nom de la personne: "
                 name = sys.stdin.readline().strip('\r').strip('\n')
                 #creer un dossier pour cette personne
                 dirname = os.path.join(imgdir,name)
                 try:
                     os.mkdir(dirname)
                 except:
                     pass #on continue si le dossier existe deja
                # on sauvegarde l'image
                 path=os.path.join(dirname,"%d.png" %(rand.uniform(0,10000)))
                 print "added:",path
                 cv2.imwrite(path,roi)
        
             # on met a jour le modele
             if (k == 116): # 't' pressed
                 images,labels,names = retrain(imgdir,model,faceSize)
                 print "Nouvel etat:",len(images),"images",len(names),"personnes"
   
	
   
             		 