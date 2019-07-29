# Smooth Stabilize2D for Blender

Smoothes a tracked path of an object in blender in order to follow the cameramovent instead of fixating the object.
Only takes a single track of a moving object. Instead of using two transform nodes shifting the image to stabalie the object and then moving the camera back to have a smooth almost fitting image the realtive movement is directly calculated.

The script can be executed in the scripting section by modifying the clipname and the trackname.

The original code to understand the API was from:
https://scummos.blogspot.com/2012/11/blender-exporting-camera-tracking.html
