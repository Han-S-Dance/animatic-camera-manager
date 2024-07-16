from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QLineEdit, QStyle, QStyleOptionViewItem, QStyledItemDelegate, QSpinBox

# modified from https://github.com/marcel-goldschen-ohm/ModelViewPyQt/blob/master/
class IntEditDelegateQt(QStyledItemDelegate):
    """ Delegate for editing int values with arbitrary precision that may also be in scientific notation.
    Based on a QLineEdit rather than Qt's default QDoubleSpinBox that limits values to two decimal places
    and cannot handle scientific notation.
    """
    def __init__(self, parent=None):
        QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        """ Return a QLineEdit for arbitrary representation of a int value.
        """
        editor = QLineEdit(parent)
        value = index.model().data(index, Qt.DisplayRole)
        editor.setText(str(value))
        return editor

    def setModelData(self, editor, model, index):
        """ Cast the QLineEdit text to a float value, and update the model with this value.
        """
        try:
            value = int(editor.text())
            model.setData(index, value, Qt.EditRole)
        except:
            pass  # If we can't cast the user's input to a int, don't do anything.

class EmptyDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        opt.text = ""
        QApplication.style().drawControl(QStyle.CE_ItemViewItem, opt, painter)
