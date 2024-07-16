import itertools
from collections import namedtuple

from .enums import ColumnEnum
from .maya_utils import add_uber_tag, apply_camera_attributes, create_camera, get_camera_names, rename, set_frame

NeighbouringCameras = namedtuple('NeighbouringCameras', ['camera_one', 'camera_one_out_frame', 'camera_two', 'camera_two_in_frame'])

class InputCamera():
    def __init__(self, name):
        self.name = name
        self.initUserDefinedAttributes()

    def initUserDefinedAttributes(self):
        for attr in ColumnEnum.get_user_defined_attrributes():
            setattr(self, attr, ColumnEnum.get_init_value_from_attribute(attr))

class CameraManager():
    def __init__(self):
        self.input_cameras = []
        self.non_adjoining_neighbouring_cameras = []

    def loadInputCameras(self):
        for camera in get_camera_names():
            self.input_cameras.append(InputCamera(camera))

    def getCheckedCameras(self):
        checked_input_cameras = []
        for input_camera in self.input_cameras:
            if input_camera.checked:
                checked_input_cameras.append(input_camera)
        return checked_input_cameras

    def validateCheckedCameras(self):
        error_message = []

        # check input range <= output range
        checked_cameras = self.getCheckedCameras()
        if not checked_cameras:
            error_message.append("No cameras checked")
            return error_message

        for input_camera in checked_cameras:
            in_frame = getattr(input_camera, ColumnEnum.IN_FRAME.attribute)
            out_frame = getattr(input_camera, ColumnEnum.OUT_FRAME.attribute)
            if in_frame > out_frame:
                error_message.append("{} 'In Frame' is larger than 'Out Frame'.".format(input_camera.name))

        for (cam1, cam2) in list(itertools.combinations(checked_cameras, 2)):
            if CameraManager.checkFrameOverlap(cam1, cam2):
                error_message.append("Frame ranges of {} and {} overlap.".format(
                    cam1.name,
                    cam2.name
                ))
        
        return error_message
    
    def getCheckedCamerasSortedByFrames(self):
        checked_cameras = self.getCheckedCameras()
        checked_cameras.sort(key = lambda x: getattr(x, ColumnEnum.IN_FRAME.attribute))
        return checked_cameras
    
    def getFirstInFrame(self):
        checked_cameras = self.getCheckedCamerasSortedByFrames()
        if checked_cameras:
            return getattr(checked_cameras[0], ColumnEnum.IN_FRAME.attribute)
        return 1001

    def getNonAdjoiningNeighbouringCamera(self):
        self.non_adjoining_neighbouring_cameras = []
        checked_cameras = self.getCheckedCamerasSortedByFrames()
        for camera_one, camera_two in zip(checked_cameras, checked_cameras[1:]):
            camera_one_out = getattr(camera_one, ColumnEnum.OUT_FRAME.attribute)
            camera_two_in = getattr(camera_two, ColumnEnum.IN_FRAME.attribute)
            if camera_one_out +1 != camera_two_in:
                self.non_adjoining_neighbouring_cameras.append(NeighbouringCameras(camera_one, camera_one_out, camera_two, camera_two_in))
        return self.non_adjoining_neighbouring_cameras
    
    def extendNonAdjoiningNeighbouringCameras(self):
        for neighbouring_cameras in self.non_adjoining_neighbouring_cameras:
            camera_one = neighbouring_cameras.camera_one
            setattr(
                camera_one,
                ColumnEnum.OUT_FRAME.attribute,
                neighbouring_cameras.camera_two_in_frame -1
                )
        self.non_adjoining_neighbouring_cameras = []

    def buildUberCamera(self):
        uber_cam = create_camera()
        add_uber_tag(uber_cam)
        for input_camera in self.getCheckedCameras():
            start_frame = getattr(input_camera, ColumnEnum.IN_FRAME.attribute)
            end_frame = getattr(input_camera, ColumnEnum.OUT_FRAME.attribute)
            apply_camera_attributes(uber_cam, input_camera.name, start_frame, end_frame)
        set_frame(self.getFirstInFrame())
        new_name = rename(uber_cam, "UberCam")
        return new_name

    @staticmethod
    def checkFrameOverlap(camera1, camera2):
        in_frame_attribute = ColumnEnum.IN_FRAME.attribute
        out_frame_attribute = ColumnEnum.OUT_FRAME.attribute

        camera1_in_frame = getattr(camera1, in_frame_attribute)
        camera1_out_frame = getattr(camera1, out_frame_attribute)

        camera2_in_frame = getattr(camera2, in_frame_attribute)
        camera2_out_frame = getattr(camera2, out_frame_attribute)

        if camera1_in_frame <= camera1_out_frame:
            range_camera1 = range(camera1_in_frame, camera1_out_frame+1)
        else:
            range_camera1 = range(camera1_out_frame, camera1_in_frame+1)
        
        if camera2_in_frame <= camera2_out_frame:
            range_camera2 = range(camera2_in_frame, camera2_out_frame+1)
        else:
            range_camera2 = range(camera2_out_frame, camera2_in_frame+1)

        overlap = list(set(range_camera1) & set(range_camera2))
        return bool(overlap)
