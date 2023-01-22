import RPi.GPIO as GPIO
import cv2 
import numpy as np
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
motor1=8
motor2=10
GPIO.setup(motor1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(motor2, GPIO.OUT, initial=GPIO.LOW)
cap=cv2.VideoCapture(0)
def dis(known_scale,know_daba_with,foc):
        distance=(foc*known_scale/know_daba_with)
        return distance        
        
cv2.namedWindow('Track')
cv2.resizeWindow('Track',300,200)
def track(x):
    pass      
cv2.createTrackbar('hue_min','Track',108,179,track )
cv2.createTrackbar('hue_max','Track',134,179, track)
cv2.createTrackbar('sat_min','Track',58,255, track)
cv2.createTrackbar('sat_max','Track',172,255, track)
cv2.createTrackbar('val_min','Track',95,255, track)
cv2.createTrackbar('val_max','Track',255,255, track)
while True:
    _,frame=cap.read()
    hsv_=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    known_scale=30
    foc=93
   
    
    
    
    h_min=cv2.getTrackbarPos('hue_min','Track')
    h_max=cv2.getTrackbarPos('hue_max','Track')
    sat_min=cv2.getTrackbarPos('sat_min','Track')
    sat_max=cv2.getTrackbarPos('sat_max','Track')
    val_min=cv2.getTrackbarPos('val_min','Track')
    val_max=cv2.getTrackbarPos('val_max','Track')   
    lower_=np.array([h_min,sat_min,val_min])
    upper_=np.array([h_max,sat_max,val_max])
    mask=cv2.inRange(hsv_,lower_,upper_)
    
    contours,hierarchy=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for contours in contours:
        area=cv2.contourArea(contours)

        if area>800:
          
            cv2.drawContours(frame,contours,-1,(0,255,0),3)
            (x,y,w,h)=cv2.boundingRect(contours)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),5)
            know_daba_with=w
            d1=dis(known_scale,know_daba_with,foc)
            d11='distance:' +' '+ str(d1)
            cv2.putText(frame,d11,(x,y),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),3,cv2.LINE_AA)
            if(d1>20):
                GPIO.output(motor1, GPIO.LOW)
                GPIO.output(motor2, GPIO.HIGH)
                sleep (1)
            elif(w==15):
                GPIO.output(motor1, GPIO.HIGH)
                GPIO.output(motor2, GPIO.HIGH)
                sleep (1)
            else:
                GPIO.output(motor1, GPIO.HIGH)
                GPIO.output(motor2, GPIO.LOW)
                sleep (1)
                
        else:
            GPIO.output(8, GPIO.LOW)
            GPIO.output(10, GPIO.LOW)
            
    cv2.imshow('original',frame)
    
    cv2.imshow('maked img',mask)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        if mask==True:
            print('object dected')
    
        break