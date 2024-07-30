
from PySide6NodeGraph.nodegraph import BaseNode


class DropdownMenuNode(BaseNode):
    """
    An example node with a embedded added QCombobox menu.
    """

    # unique node identifier.
    __identifier__ = 'nodes.widget'

    # initial default node name.
    NODE_NAME = 'menu'

    def __init__(self, list_camera = []):
        super(DropdownMenuNode, self).__init__()

        # create input & output ports
        self.add_input('IN', multi_input=True)
        self.add_output('OUT', multi_output=True)
        # self.add_input('IN', multi_input=True)
        # self.add_input('IN 2', multi_input=True)
        # self.add_output('OUT 1', multi_output=True)
        # self.add_output('OUT 2', multi_output=True)

        # create the QComboBox menu.
        items = ['Choose Camera', 'Camera 1111111111111111', 'Camera 222222222222222222222222222222222222222', 'Camera 3']
        camera_names = ['Traffic 00', 'Traffic 030t', 'Traffic 02', 'Camera_192.168.1.250_0', 'Camera_14.241.65.20_00', 'GIAO THONG 01 00t', 'Camera 11 00t', 'Face 1', 'Face 2', 'Face 3', 'Face 4', 'Face 5', 'Face 6', 'Face 7', 'Face 8', 'Face 9', 'Face 10', 'Face 11', 'Face 12', 'Face 13', 'Face 14', 'Face 15', 'Face 16', 'Face 17', 'Face 18', 'Face 19', 'Traffic 040t', 'Traffic 050t', 'Traffic 060t', 'Traffic 07', 'RESTREAM T4 DBQH', 'Camera_14.241.65.20_0', 'VAN PHONG FORWARD 192.168.1.250', 'Camera_14.241.65.122_0', 'Camera_14.241.65.20_1', 'Camera_14.241.65.172_2', 'Camera_14.241.65.147_3', 'Camera_14.241.65.109_0', 'Camera_210.86.224.217_0', 'Camera_123.22.7.105_0', 'Camera_123.22.7.105_0_1', 'Camera_123.22.7.105_1', 'Camera_123.22.7.105_2', 'Camera_14.241.85.150_0', 'Camera_27.72.116.8_0', 'Camera_27.72.116.8_1', 'Camera_27.72.116.8_2', 'Camera_27.72.116.8_3', 'Camera_27.72.116.8_4', 'Camera_27.72.116.8_5', 'Camera_27.72.116.8_6', 'Camera_27.72.116.8_7', 'Camera_27.72.116.8_8', 'Camera_27.72.116.8_9', 'Camera_27.72.116.8_10', 'Camera_27.72.116.8_11', 'Camera_27.72.116.8_12', 'Camera_27.72.116.8_13', 'Camera_27.72.116.8_14', 'Camera_27.72.116.8_15']
        self.add_combo_menu('my_menu', 'Camera List', items=camera_names)


class TextInputNode(BaseNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'nodes.widget'

    # initial default node name.
    NODE_NAME = 'Camera'

    def __init__(self, value):
        super(TextInputNode, self).__init__()

        # create input & output ports
        self.add_input('IN', multi_input=True)
        self.add_output('OUT', multi_output=True)

        # create QLineEdit text input widget.
        self.add_text_input('my_input', 'Text Inputttttt', tab='widgets')
        for idx, widget_child in self.widgets().items():
            line_edit = widget_child.get_custom_widget()
            line_edit.setText(value)
            line_edit.setReadOnly(True)


class CheckboxNode(BaseNode):
    """
    An example of a node with 2 embedded QCheckBox widgets.
    """

    # set a unique node identifier.
    __identifier__ = 'nodes.widget'

    # set the initial default node name.
    NODE_NAME = 'checkbox'

    def __init__(self):
        super(CheckboxNode, self).__init__()

        # create the checkboxes.
        self.add_checkbox('cb_1', '', 'Checkbox 1', True)
        self.add_checkbox('cb_2', '', 'Checkbox 2', False)

        # create input and output port.
        self.add_input('in', color=(200, 100, 0))
        self.add_output('out', color=(0, 100, 200))
