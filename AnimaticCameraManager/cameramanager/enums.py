from collections import namedtuple
from enum import Enum
import itertools

DataColumn = namedtuple("DataColumn", "index text attribute user_input init_value")

i = itertools.count()
class ColumnEnum(Enum):
    CHECKED = DataColumn(next(i), "", "checked", True, False)
    NAME = DataColumn(next(i), "Camera", "name", False, None)
    IN_FRAME = DataColumn(next(i), "In Frame", "user_in_frame", True, 1001)
    OUT_FRAME = DataColumn(next(i), "Out Frame", "user_out_frame", True, 1001)

    @classmethod
    def at(cls, index):
        for column in cls:
            if column.index == index:
                return column

    @classmethod
    def get_init_value_from_attribute(cls, attribute):
        for column in cls:
            if column.attribute == attribute:
                return column.init_value

    @classmethod
    def get_user_defined_attrributes(cls):
        user_input_attributes = []
        for column in cls:
            if column.user_input:
                user_input_attributes.append(column.attribute)
        return user_input_attributes
    
    @classmethod
    def get_user_input_indexes(cls):
        indexes = []
        for column in cls:
            if column.user_input:
                indexes.append(column.index)
        return indexes

    @property 
    def index(self):
        return self.value.index
    
    @property
    def text(self):
        return self.value.text
    
    @property
    def attribute(self):
        return self.value.attribute
    
    @property
    def user_input(self):
        return self.value.user_input
    
    @property
    def init_value(self):
        return self.value.init_value