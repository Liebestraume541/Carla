import sys
import time 
import os

from numpy.lib.type_check import imag
import carla
import glob
import random
import numpy as np
import cv2
import PIL
from PIL import Image, ImageFile
import matplotlib.pyplot as plt


try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

def main():
    actor_list = []
    IMG_HEIGHT = 720
    IMG_WIDTH = 1280
    def process_img(image, l_images):
         i = np.array(image.raw_data, dtype=np.uint8) 
         i2 = i.reshape((IMG_HEIGHT, IMG_WIDTH, 4)) #rgba, a for alpha (opacity)
         i3 = i2[:, :, :3] # /255.0 # entire height, entire width, only rgb (no alpha)
         print(i3.shape)
         l_images.append(i3)
         img = Image.fromarray(i3, "RGB")
         img.show()
         
         
         return i3/255.0 # normalize the data
         
         
    #     #import pdb; pdb.set_trace()
    #     #cv2.imshow("image", i3)
    #     #cv2.waitKey(0)
         
     # normalize the data
    # # def process(image):
    # #     i = np.array(image.raw_data)
    # #     i2 = i.reshape((IMG_HEIGHT, IMG_WIDTH, 4))
    # #     i3 = i2[:,:, :3]
    # #     cv2.imshow("", i3)
    #     cv2.waitKey(0)
    #     return i3 / 255.0
    
    try:
        client = carla.Client("localhost", 2000)
        client.set_timeout(2.0)
        world = client.load_world('Town03')
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()
        
        bp = blueprint_library.find("vehicle.ford.mustang")
        
        #Transform = carla.Transform()
        
        
        #transform = Transform(Location(x=230, y=195, z=40), Rotation(yaw=180))
        
        #transform = random.choice(world.get_map().get_spawn_points())
        transform = world.get_map().get_spawn_points()
        
        vehicle = world.spawn_actor(bp, transform[1])
        
        
        actor_list.append(vehicle)
        print('created %s' % vehicle.type_id)
        print(client.get_available_maps())
        

        
        vehicle.set_autopilot(False)
        
        
        camera_bp = blueprint_library.find("sensor.camera.rgb")
        camera_bp.set_attribute("image_size_x", str(IMG_WIDTH))
        camera_bp.set_attribute("image_size_y", str(IMG_HEIGHT))
        camera_bp.set_attribute("fov", str(90))
        #camera_bp.set_attribute("sensor_tick", str(1.0))
        camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        actor_list.append(camera)
        print('created %s' % camera.type_id)
        
        
        #cc = carla.ColorConverter.Raw
        
        #camera.listen(lambda image: image.save_to_disk('_out/%06d.png' % image.frame,))
        l_images = []
        camera.listen(lambda image: process_img(image, l_images))
        
        
        
        
        
        
  
        
        vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
        
        time.sleep(10)
        
    finally:

        print('destroying actors')
        camera.destroy()
        client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
        print('done.')
        
main()

