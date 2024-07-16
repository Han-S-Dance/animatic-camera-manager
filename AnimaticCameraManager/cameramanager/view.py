from PySide2.QtCore import Qt
from PySide2.QtWidgets import QAbstractScrollArea, QHeaderView, QSizePolicy, QTableView

from .data import ColumnEnum
from .delegate import IntEditDelegateQt, EmptyDelegate
class InputCameraView(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
        
        self.setItemDelegateForColumn(ColumnEnum.CHECKED.index, EmptyDelegate(self))
        self.setItemDelegateForColumn(ColumnEnum.IN_FRAME.index, IntEditDelegateQt(self))
        self.setItemDelegateForColumn(ColumnEnum.OUT_FRAME.index, IntEditDelegateQt(self))
        
        self.setAlternatingRowColors(True)

        self.horizontalHeader().setMinimumSectionSize(0)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.verticalHeader().hide()
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
