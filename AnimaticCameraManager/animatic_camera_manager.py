from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from cameramanager.data import CameraManager
from cameramanager.model import InputCameraModel
from cameramanager.ui import CustomDialog, CustomMessageBox
from cameramanager.view import InputCameraView

#modified from https://gist.github.com/isaacoster
class MayaUI(QWidget):
    """
    Create a default tool window.
    """
    window = None
    
    def __init__(self, input_camera_manager, parent = None):
        """
        Initialize class.
        """
        super(MayaUI, self).__init__(parent = parent)
        self.input_camera_manager = input_camera_manager
        self.setWindowFlags(Qt.Window)

        layout = QVBoxLayout(self)
        label = QLabel()
        label_text = "To create an Uber Camera check all cameras for inclusion,\ninput the corresponding in and out frames and press\n'Build Uber Camera'."
        label.setText(label_text)
        layout.addWidget(label)

        tablemodel = InputCameraModel(input_camera_manager)
        tableview = InputCameraView()
        tableview.setModel(tablemodel)
        tableview.setColumnWidth(0,16)
        
        layout.addWidget(tableview)

        button_layout = QHBoxLayout()
        build_uber_cam_button = QPushButton("Build Uber Camera", self)
        build_uber_cam_button.clicked.connect(self.builUberCamClicked)
        button_layout.addStretch(1)
        button_layout.addWidget(build_uber_cam_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setWindowTitle("Uber Camera Creator")

    def builUberCamClicked(self):
        errors = self.input_camera_manager.validateCheckedCameras()
        if errors:
            error_message = ["Please resolve the following issue(s) and rebuild:"]
            error_message.extend(errors)
            CustomDialog("\n".join(error_message), "Error", parent=self).exec()
            return
        
        non_adjoining_cameras = self.input_camera_manager.getNonAdjoiningNeighbouringCamera()
        if non_adjoining_cameras:
            non_adjoining_message = ["The following cameras have frames range errors:"]
            for neighbouring_cameras in non_adjoining_cameras:
                non_adjoining_message.append(
                    "{} - {} missing adjoining frames {}-{} ".format(
                    neighbouring_cameras.camera_one.name,
                    neighbouring_cameras.camera_two.name,
                    neighbouring_cameras.camera_one_out_frame +1,
                    neighbouring_cameras.camera_two_in_frame -1
                    )
                )
            non_adjoining_message.append(" ")
            non_adjoining_message.append(
                "Extend 'Out Frame(s)' to the next 'In Frame(s)' & build Uber Camera or return and edit frames."
            )

            message_box = CustomMessageBox(
                "\n".join(non_adjoining_message),
                "Warning - Non Adjoning Frames",
                "Extend Frames and Build Uber Camera", 
                "Return and Edit"
            )
            if message_box.exec() != QMessageBox.AcceptRole:
                return
            
            self.input_camera_manager.extendNonAdjoiningNeighbouringCameras()

        uber_camera = self.input_camera_manager.buildUberCamera()
        CustomDialog("UberCam {} has been created".format(uber_camera), "Success", parent=self)
        self.close()

 
def run():
    """
    ID Maya and attach tool window.
    """
    input_camera_manager = CameraManager()
    input_camera_manager.loadInputCameras()

    # Maya uses this so it should always return True
    if QApplication.instance():
        # Id any current instances of tool and destroy
        for win in (QApplication.allWindows()):
            if 'myToolWindowName' in win.objectName(): # update this name to match name below
                win.destroy()

    #QtWidgets.QApplication(sys.argv)
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)
    MayaUI.window = MayaUI(input_camera_manager, parent = mayaMainWindow)
    MayaUI.window.setObjectName('myToolWindowName') # code above uses this to ID any existing windows
    MayaUI.window.show()
