# conda create -n im_env python-3.11
# conda activate im_env
# pip install opencv-python mediapipe==0.10.9
# add to path - anaconda then run these in terminal one by one
import cv2
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
            mp.drawing.draw_landmarks(
                images=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION
            )
    cv2.imshow("Facemesh",frame)
    key=cv2.waitKey(1) & 0xFF
    if key==27:
        break
cap.release()
cv2.destroyAllWindows()