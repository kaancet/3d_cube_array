import py5
from cube import *

w = 600
h = 600
d = 600
cubes = []

size_or_rot = 1 #0 is size 1 is rotation

def make_grid(nw:int,nh:int,nd:int=1,pad:float=20) -> np.ndarray:
    """ Makes a 2D-grid of points to instantiate the pills at """
    global w,h
    x = np.linspace(pad,w-pad,nw)
    y = np.linspace(pad,h-pad,nh)
    z = np.linspace(-d/2+pad,d/2-pad,nd)
    xx, yy, zz = np.meshgrid(x,y,z)
    return np.hstack((xx.reshape(-1,1),yy.reshape(-1,1),zz.reshape(-1,1)))

def random_delete(cube_list:list,amount:int=4) -> list:
    """ Randomly deletes some elements in the cube list"""
    if amount >= len(cube_list):
        raise ValueError(f'Amount to delete too large: {amount}>={len(cube_list)}')
         
    delete_idx = np.random.choice(np.arange(1,len(cube_list)),size=amount,replace=False)
    new_cube_list = [cube_list[i] for i in range(len(cube_list)) if i not in delete_idx]
    return new_cube_list

def setup():
    global w,h,cubes
    py5.size(w, h, py5.P3D)
    py5.frame_rate(30)
    py5.stroke_weight(1)
    
    py5.color_mode(py5.HSB,360,100,100,100)
    py5.rect_mode(py5.CENTER)
    
    grid = make_grid(3,3,3,80)
    
    # origin lines
    # py5.line(0,h/2,0,w,h/2,0)
    # py5.line(w/2,0,0,w/2,h,0)
    # py5.line(w/2,h/2,-100,w/2,h/2,100)
    
    for i in range(grid.shape[0]):
        c = Cube(x=grid[i,0],y=grid[i,1],z=grid[i,2],
                 w=30,h=50,d=30,
                 acc_coeff = np.random.randint(1,5)*0.1,
                 rot_coeff = np.random.randint(10,30)*0.01,
                 c_fill=[np.random.randint(0,360),np.random.randint(33,100),np.random.randint(33,100)])
        cubes.append(c)
        
    cubes = random_delete(cubes,10) # deleting random coordinates just because
        
    py5.camera(w/2 + 400, h/2 - 400, (h//2.0 - 50) / np.tan(np.pi*30.0 / 180.0), w/2, h/2, 0.0, 0.0, 1.0, 0.0)
    
def draw():
    global cubes,size_or_rot    
    py5.background(163,40,70)
    
    # select whether to do size or rotation change every 300 frames(10 secs)
    if py5.frame_count % 150 == 0:
        size_or_rot = np.random.randint(0,2)
        pr = 'ROTATING...' if size_or_rot else 'CHANGING SIZE...'
        print(pr)
        
    for c in cubes:
        py5.fill(py5.color(c.c_fill[0],c.c_fill[1],c.c_fill[2]))
        if size_or_rot == 0:
            c.delta_size()
        
        with py5.push():
            py5.translate(c.x, c.y, c.z)

            if size_or_rot == 1:
                c.delta_rot_y()
            
            py5.rotate_x(py5.radians(c.rot_x))
            py5.rotate_y(py5.radians(c.rot_y))
            py5.rotate_z(py5.radians(c.rot_z))

            py5.box(c.w,c.h,c.d)

py5.run_sketch()