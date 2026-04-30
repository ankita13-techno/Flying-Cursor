import numpy as np
import pyautogui
import time

class CursorController:
    def __init__(self, frame_r=100, smooth_factor=5):
        """
        frame_r: Frame reduction to increase sensitivity
        smooth_factor: Smoothing factor for cursor movement
        """
        self.frame_r = frame_r
        self.smooth_factor = smooth_factor
        self.w_scr, self.h_scr = pyautogui.size()
        self.ploc_x, self.ploc_y = 0, 0
        self.cloc_x, self.cloc_y = 0, 0
    
    def move_cursor(self, x1, y1, w_cam, h_cam):
        # 1. Convert Coordinates
        # Map range from camera resolution (w_cam, h_cam) to screen resolution (w_scr, h_scr)
        # We use frame_r to crop the camera feed for mapping, so movements are amplified
        
        x3 = np.interp(x1, (self.frame_r, w_cam - self.frame_r), (0, self.w_scr))
        y3 = np.interp(y1, (self.frame_r, h_cam - self.frame_r), (0, self.h_scr))
        
        # 2. Smoothen Values
        self.cloc_x = self.ploc_x + (x3 - self.ploc_x) / self.smooth_factor
        self.cloc_y = self.ploc_y + (y3 - self.ploc_y) / self.smooth_factor
        
        # 3. Move Mouse
        # Clamp values to screen size to avoid errors
        self.cloc_x = max(0, min(self.cloc_x, self.w_scr - 1))
        self.cloc_y = max(0, min(self.cloc_y, self.h_scr - 1))
        
        try:
            pyautogui.moveTo(self.w_scr - self.cloc_x, self.cloc_y) # Mirror X axis
        except pyautogui.FailSafeException:
            pass # Ignore fail safe for now or handle gracefully

        self.ploc_x, self.ploc_y = self.cloc_x, self.cloc_y
        
    def click(self, dist):
        # Simple click if distance is small enough (pinch)
        # Verify distance threshold in main loop
        pyautogui.click()

    def right_click(self):
        pyautogui.click(button='right')

    def scroll(self, y_movement):
        # Determine scroll amount based on movement
        # Adjust sensitivity as needed
        pyautogui.scroll(int(y_movement * 2)) # Multiplier for sensitivity
