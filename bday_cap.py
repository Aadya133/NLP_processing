import cv2
import numpy as np
import mediapipe as mp
mp_face_mesh=mp.solutions.face_mesh
mp_drawing=mp.solutions.drawing_utils

face_mesh=mp_face_mesh.FaceMesh(
    static_image_mode=False, #use video screen
    max_num_faces=1,   # detect 1 face 
    refine_landmarks=True, # enables more detailed landmarks -eyes
    min_detection_confidence=0.5,  # min confidence to detect face
    min_tracking_confidence=0.5  # min confidence to track face

)

bcap=cv2.imread("crown.png",cv2.IMREAD_UNCHANGED)

cap=cv2.VideoCapture(0)
while True:
    flag,frame=cap.read()
    if not flag:
        break
    rgb_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Detect face landmark
    results = face_mesh.process(rgb_frame)
    # draw landmarks
    # check if any face detected
    if results.multi_face_landmarks:
        # loop through detected faces ( here 1 only)
        for face_landmarks in results.multi_face_landmarks:
            
            h,w,_=frame.shape
            left_head=face_landmarks.landmark[68]
            right_head=face_landmarks.landmark[298]
            
            x1,y1=int(left_head.x*w),int(left_head.y*h)
            x2,y2=int(right_head.x*w),int(right_head.y*h)

            cap_width=int(np.hypot(x2-x1,y2-y1)*1.5)
            cap_height=int(cap_width*0.8)
            
            resized_cap=cv2.resize(bcap,(cap_width,cap_height))
           
            x_center=(x1+x2)//2
            y_center=(y1+y2)//2
            top_head = face_landmarks.landmark[10]  # top of forehead
            y_top = int(top_head.y * h)

            y_offset = int(y_top - cap_height * 0.9)

            x_offset=int(x_center- cap_width/2)
            #y_offset=int(y_center-cap_height *1.2)

            overlay_img = resized_cap[:,:,:3]
            mask = resized_cap[:,:,3]

            # mask inverse
            mask_inv=cv2.bitwise_not(mask)
            if y_offset < 0 or x_offset < 0 or y_offset + cap_height > h or x_offset + cap_width > w:
                continue
            roi = frame[y_offset:y_offset+cap_height,x_offset:x_offset+cap_width]

            background = cv2.bitwise_and(roi,roi,mask=mask_inv)
            foreground = cv2.bitwise_and(overlay_img,overlay_img,mask=mask)

            combined=cv2.add(background,foreground)
            frame[y_offset:y_offset+cap_height,x_offset:x_offset+cap_width]=combined

    cv2.imshow("Sunglass filter",frame)
    key=cv2.waitKey(1) & 0xFF
    if key==27:
        break
cap.release()
cv2.destroyAllWindows()