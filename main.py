import cv2
import time
import math
import numpy as np
import pyautogui
from hand_tracking import HandDetector
from cursor_controller import CursorController

################################
# Initial Parameter Constants
wCam, hCam = 640, 480
################################

def nothing(x):
    pass

def main():
    # 1. Setup
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    
    detector = HandDetector(max_hands=1)
    controller = CursorController(frame_r=100, smooth_factor=5)
    
    # Settings Window
    cv2.namedWindow("Settings")
    cv2.resizeWindow("Settings", 400, 150)
    cv2.createTrackbar("Sensitivity", "Settings", 100, 150, nothing) 
    cv2.createTrackbar("Smoothing", "Settings", 5, 20, nothing)
    
    pTime = 0
    
    print("Flying Cursor started. Press 'q' to exit.")
    
    # Disable FailSafe to prevent crashing when hitting corners
    # (Since we want the app to stay open)
    pyautogui.FAILSAFE = False 
    
    while True:
        try:
            # Update parameters
            frame_r = cv2.getTrackbarPos("Sensitivity", "Settings")
            smooth = cv2.getTrackbarPos("Smoothing", "Settings")
            
            # Sanity checks
            if frame_r < 10: frame_r = 10
            if frame_r > wCam // 2 - 10: frame_r = wCam // 2 - 10
            if smooth < 1: smooth = 1
            
            controller.frame_r = frame_r
            controller.smooth_factor = smooth

            success, img = cap.read()
            if not success:
                print("Failed to capture image. Retrying...")
                time.sleep(1)
                continue
                
            # Find Hand Landmarks
            img = detector.find_hands(img)
            lm_list = detector.find_position(img, draw=False)
            
            if len(lm_list) != 0:
                # Tips: Index(8), Thumb(4), Middle(12)
                x1, y1 = lm_list[8][1:] 
                x2, y2 = lm_list[4][1:] 
                x3, y3 = lm_list[12][1:] 
                
                fingers = detector.fingersUp()
                
                # Draw Boundary
                cv2.rectangle(img, (frame_r, frame_r), (wCam - frame_r, hCam - frame_r),
                            (255, 0, 255), 2)
                
                # Logic Flow
                
                # A. SCROLLING: Index and Middle are UP
                if fingers[1] == 1 and fingers[2] == 1:
                    mid_y = hCam // 2
                    if y1 < mid_y - 50:
                        controller.scroll(20) 
                        cv2.putText(img, "Scroll UP", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                    elif y1 > mid_y + 50:
                        controller.scroll(-20) 
                        cv2.putText(img, "Scroll DOWN", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                        
                # B. MOVING: Only Index is UP
                elif fingers[1] == 1 and fingers[2] == 0:
                    controller.move_cursor(x1, y1, wCam, hCam)
                    
                    # Click Check
                    length = math.hypot(x2 - x1, y2 - y1)
                    if length < 40:
                        cv2.circle(img, ( (x1+x2)//2, (y1+y2)//2 ), 15, (0, 255, 0), cv2.FILLED)
                        controller.click(length)
                
                # C. RIGHT CLICK: Middle Finger + Thumb Pinch
                elif fingers[1] == 0 and fingers[2] == 1:
                    length_mid_thumb = math.hypot(x2 - x3, y2 - y3)
                    if length_mid_thumb < 40:
                         cv2.circle(img, ( (x3+x2)//2, (y3+y2)//2 ), 15, (255, 0, 0), cv2.FILLED)
                         controller.right_click()
                         time.sleep(0.2)

            # Display
            cTime = time.time()
            fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
            pTime = cTime
            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            
            cv2.imshow("Flying Cursor", img)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        except Exception as e:
            # If an error happens inside the loop, print it but DON'T CRASH
            print(f"Loop Error: {e}")
            # Introduce a small delay to prevent log spamming if error is persistent
            cv2.waitKey(100) 

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
