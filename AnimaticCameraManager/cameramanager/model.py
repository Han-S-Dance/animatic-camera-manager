from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt
from .enums import ColumnEnum


class InputCameraModel(QAbstractTableModel):
    def __init__(self, input_camera_manager, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.input_camera_manager = input_camera_manager

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.input_camera_manager.input_cameras)
    
    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(ColumnEnum)
    
    def data(self, index, role):
        if not index.isValid():
            return None
        attribute_name = self._getAttrAtColumn(index.column())
        input_camera = self.input_camera_manager.input_cameras[index.row()]
        attribute = getattr(input_camera, attribute_name)
        if role == Qt.DisplayRole:
            return attribute
        elif role == Qt.CheckStateRole and index.column() == ColumnEnum.CHECKED.index:
            if attribute:
                return Qt.Checked
            else:
                return Qt.Unchecked
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        else:
            return None

    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return ColumnEnum.at(section).text
        return QAbstractTableModel.headerData(self, section, orientation, role)
    
    def _getAttrAtColumn(self, column):
        return ColumnEnum.at(column).attribute
    
    def flags(self, index):
        if index.column() == ColumnEnum.CHECKED.index:
            return Qt.ItemIsUserCheckable|Qt.ItemIsEnabled
        elif index.column() in ColumnEnum.get_user_input_indexes():
            return Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled|Qt.ItemIsSelectable
    
    def setData(self, index, value, role):
        if role in (Qt.EditRole, Qt.CheckStateRole):
            if role == Qt.CheckStateRole:
                value = value!=Qt.Unchecked
            input_camera = self.input_camera_manager.input_cameras[index.row()]
            attribute = ColumnEnum.at(index.column()).attribute
            setattr(input_camera, attribute, value)
            return True


           