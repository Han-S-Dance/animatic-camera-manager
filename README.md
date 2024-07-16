# animatic-camera-manager
Maya UI tool that creates an Uber camera from cameras in the scene.

# Specification
Imaging an artist has built an animatic scene, where rough animation for a sequence has been blocked out. As well as animated proxy characters, they have also blocked out a few rough cameras for the shots the sequence will contain. The Maya scene delivered with the test is an example you can use to develop with, if you wish.

When run, the tool should open a UI, which should list all the cameras in the scene. Next to each camera should be input widgets for the "In Frame" and "Out Frame". The user can then enter values for the in and out frames of each camera, as well as having a way to select/deselect each camera for inclusion.

Lastly, the user will click a "Build Uber Camera" button, which will create a new camera in the scene, named "UberCam". This camera should follow the animation of the selected cameras, over the configured frame ranges.

Now the artist can use this new UserCam, to see the entire sequence play through. The camera will follow the motion of each shot camera, darting around the scene to track each camera in turn.

# Solution
Below is my personal solution to the above challenge, created using PyQt.

## Loading the Script
Run the following in script editor, replacing the absolute path, to the location of the AnimaticCameraManager folder
```
import sys
sys.path.insert(0,'D:\\ MayaTool\\AnimaticCameraManager')

from importlib import reload

import animatic_camera_manager
reload(animatic_camera_manager)

animatic_camera_manager.run()
```

## Catching Input Errors
Three types of initial user input error are caught when ‘Build Uber Camera’ is clicked, the user is taken back to the main ui to resolve these.
1. No checked cameras
2. ‘In Frame’  > ‘Out Frame’
3. Frame range overlaps for checked cameras

## Missing frames between cameras
When building an uber camera , a continuous range of frames between cameras is expected.
In the example to the right the ‘In Frames’ and ‘Out Frames’ follow on from each other. 
- camera3: 1001 - 1006
- camera1: 1007 - 1189
- camera4: 1190 - 1195

When a continuous range of frames between cameras is not provided the user is given 2 options.
1. Extend first camera’s ‘Out Frame’ to the next camera’s ‘In Frame’
    - camera2: 1100-1105 -> 1100-1139
    - camera3: 1140-1141 -> 1140-1155
    - camera4: 1156-1171
2. The user can return to the main ui and manually edit.
   
