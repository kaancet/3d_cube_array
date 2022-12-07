import numpy as np

class Cube:
    def __init__(self,x:float,y:float,z:float,w:float,h:float,d:float,acc_coeff:float,rot_coeff:float,c_fill:list) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.d = d
        self.acc_coeff = acc_coeff
        self.rot_coeff = rot_coeff
        
        if c_fill is None:
            c_fill = [332, 60, 66]
        self.c_fill = c_fill
        
        self.init_aux_vars()
        
    def set_size(self,w:float,h:float,d:float) -> None:
        """ Sets the size of the cube"""
        self.w = w
        self.h = h
        self.d = d
        
        self.init_aux_vars()
        
    def init_aux_vars(self) -> None:
        """ Initializes size and rotation tracking variables"""
        self.size_change = 1
        self.max_w = self.w * 1.3
        self.max_h = self.h * 1.3
        self.max_d = self.d * 1.3
        self.min_w = self.w * 0.2
        self.min_h = self.h * 0.2
        self.min_d = self.d * 0.2
        
        self.hw_ratio = self.h/self.w
        self.dw_ratio = self.d/self.w
        
        self.rot_x = 0
        self.rot_y = 0
        self.rot_z = 0
        self.target_rot = 200
    
    def delta_rot_y(self)->None:
        """ Rotates the cube continuosly by incrementing both the current rotation and the target rotation"""
        rot_diff = self.target_rot - self.rot_y
        if rot_diff >= 0:
            rot_delta = self.rot_coeff * (rot_diff + 3)
            self.rot_y += rot_delta
            
        if self.rot_y >= self.target_rot:
            self.rot_y = self.target_rot
            new_target = (self.target_rot + self.rot_y) % 360

            self.target_rot = new_target
         
    def delta_size(self) -> None:
        """ Increments or decrements the size """
        # acceleration is dependent on distance to limit
        delta_coeff = self.acc_coeff
        if self.w >= self.max_w and self.h >= self.max_h and self.d >= self.max_d:
            self.size_change = -1
        elif self.w <= self.min_w and self.h <= self.min_h and self.d <= self.min_d:
            self.size_change = 1
        
        
        if self.size_change == 1:
            delta_coeff = self.acc_coeff * ((self.max_w - self.w) + (self.max_h - self.h) + (self.max_d - self.d)) / 3
        elif self.size_change == -1:
            delta_coeff = self.acc_coeff * ((self.w - self.min_w) + (self.h - self.min_h) + (self.d - self.min_d)) / 3
        
        size_delta = self.size_change * (delta_coeff + 0.05)
        self.w += size_delta
        self.h += size_delta * self.hw_ratio
        self.d += size_delta * self.dw_ratio
        
        