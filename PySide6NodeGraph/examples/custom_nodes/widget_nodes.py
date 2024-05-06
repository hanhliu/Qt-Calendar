
from PySide6NodeGraph.nodegraph import BaseNode


class DropdownMenuNode(BaseNode):
    """
    An example node with a embedded added QCombobox menu.
    """

    # unique node identifier.
    __identifier__ = 'nodes.widget'

    # initial default node name.
    NODE_NAME = 'menu'

    def __init__(self):
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
        self.add_combo_menu('my_menu', 'Camera List', items=items)


class TextInputNode(BaseNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'nodes.widget'

    # initial default node name.
    NODE_NAME = 'text'

    def __init__(self):
        super(TextInputNode, self).__init__()

        # create input & output ports
        self.add_input('in')
        self.add_output('out')

        # create QLineEdit text input widget.
        self.add_text_input('my_input', 'Text Input', tab='widgets')


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
