import maya.cmds as cmds

TAG = "UberCam"

def rename(old_name, suggested_name):
    new_name = cmds.rename(old_name, suggested_name)
    return new_name

def add_uber_tag(obj):
    cmds.addAttr(obj, ln=TAG, attributeType="message")

def query_uber_tag(obj):
    return cmds.attributeQuery(TAG, node=obj, ex=True)

def create_camera():
    obj = cmds.camera() # returns([str]): [transform name, shape name]
    return obj[0]

def set_frame(frame):
    cmds.currentTime(frame)

def get_camera_names(filter_startup_and_uber_cams=True):
    cameras = cmds.listCameras()
    if filter_startup_and_uber_cams:
        cameras = [
            cam for cam in cameras
            if not cmds.camera(cam, startupCamera = True, q=True)
            and not(query_uber_tag(cam))
        ]
    return cameras

def get_attributes_to_copy(source_obj):
    return cmds.listAnimatable(source_obj)

def apply_camera_attributes(target_camera, source_camera, start_frame, end_frame):
    source_objs = cmds.ls(source_camera)
    if not source_objs:
        return
    source_obj = source_objs[0]
    source_shapes = cmds.listRelatives(source_obj, shapes=True)
    if not source_shapes:
        return
    source_shape = source_shapes[0]
    
    target_objs = cmds.ls(target_camera)
    if not target_objs:
        return 
    target_obj = target_objs[0]
    target_shapes = cmds.listRelatives(target_obj, shapes=True)
    if not target_shapes:
        return
    target_shape = target_shapes[0]

    animAttributes = get_attributes_to_copy(source_obj)

    for frame in range(start_frame, end_frame+1):
        cmds.currentTime(frame)
        for attribute in animAttributes:
            try:
                value = cmds.getAttr(attribute)
                for r in ((source_obj, target_obj), (source_shape, target_shape)):
                    attribute = attribute.replace(*r)
                cmds.setAttr(attribute, value)
            except Exception as e:
                print(e)
        cmds.setKeyframe(target_obj, hi='none')
    
