import os
import sys
import signal

from PySide6 import QtCore
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, \
    QHBoxLayout

from PySide6NodeGraph.nodegraph import (
    NodeGraph,
    PropertiesBinWidget,
    NodesTreeWidget,
    NodesPaletteWidget
)

# import example nodes from the "example_nodes" package
from PySide6NodeGraph.examples import group_node
from PySide6NodeGraph.examples.custom_nodes import (
    basic_nodes,
    custom_ports_node,
    widget_nodes,
)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # Create a central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.camera_names = ['Traffic 00', 'Traffic 030t', 'Traffic 02', 'Camera_192.168.1.250_0', 'Camera_14.241.65.20_00', 'GIAO THONG 01 00t', 'Camera 11 00t', 'Face 1', 'Face 2', 'Face 3', 'Face 4', 'Face 5', 'Face 6', 'Face 7', 'Face 8', 'Face 9', 'Face 10', 'Face 11', 'Face 12', 'Face 13', 'Face 14', 'Face 15', 'Face 16', 'Face 17', 'Face 18', 'Face 19', 'Traffic 040t', 'Traffic 050t', 'Traffic 060t', 'Traffic 07', 'RESTREAM T4 DBQH', 'Camera_14.241.65.20_0', 'VAN PHONG FORWARD 192.168.1.250', 'Camera_14.241.65.122_0', 'Camera_14.241.65.20_1', 'Camera_14.241.65.172_2', 'Camera_14.241.65.147_3', 'Camera_14.241.65.109_0', 'Camera_210.86.224.217_0', 'Camera_123.22.7.105_0', 'Camera_123.22.7.105_0_1', 'Camera_123.22.7.105_1', 'Camera_123.22.7.105_2', 'Camera_14.241.85.150_0', 'Camera_27.72.116.8_0', 'Camera_27.72.116.8_1', 'Camera_27.72.116.8_2', 'Camera_27.72.116.8_3', 'Camera_27.72.116.8_4', 'Camera_27.72.116.8_5', 'Camera_27.72.116.8_6', 'Camera_27.72.116.8_7', 'Camera_27.72.116.8_8', 'Camera_27.72.116.8_9', 'Camera_27.72.116.8_10', 'Camera_27.72.116.8_11', 'Camera_27.72.116.8_12', 'Camera_27.72.116.8_13', 'Camera_27.72.116.8_14', 'Camera_27.72.116.8_15']
        self.create_node_graphic()


        # Create a layout for the central widget
        lay = QVBoxLayout(self.central_widget)
        lay.setContentsMargins(0, 0, 0, 0)

        self.button_create_node = QPushButton('Create Node')
        self.button_create_node.clicked.connect(self.create_node_click)

        self.button_save = QPushButton("SAVE")
        self.button_save.clicked.connect(self.save_click)

        self.layout_button = QHBoxLayout()
        self.layout_button.addWidget(self.button_create_node)
        self.layout_button.addWidget(self.button_save)

        lay.addWidget(QLabel("Node Graph"))
        lay.addLayout(self.layout_button)
        lay.addWidget(self.graph_widget)
        self.graph_widget.show()

    def create_node_graphic(self):
        # handle SIGINT to make the app terminate on CTRL+C
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)

        # create graph controller.
        self.graph = NodeGraph()
        self.graph.set_grid_mode(1)
        self.graph.set_background_color(47, 47, 47)
        # registered example nodes.
        self.graph.register_nodes([
            basic_nodes.BasicNodeA,
            basic_nodes.BasicNodeB,
            custom_ports_node.CustomPortsNode,
            group_node.MyGroupNode,
            widget_nodes.DropdownMenuNode,
            widget_nodes.TextInputNode,
            widget_nodes.CheckboxNode
        ])
        drop_down_node = widget_nodes.DropdownMenuNode(list_camera=self.camera_names)
        print(f"HanhLT: drop_down_node = {drop_down_node}")
        self.graph.add_node(drop_down_node)
        # show the node graph widget.
        self.graph_widget = self.graph.widget
        self.graph_widget.resize(1100, 800)

        self.custom_default_create_node()
        # self.default_init_node()

        # auto layout nodes.
        self.graph.auto_layout_nodes()

        # crate a backdrop node and wrap it around
        # "custom port node" and "group node".
        # n_backdrop = self.graph.create_node('Backdrop')
        # n_backdrop.wrap_nodes([n_custom_ports, n_combo_menu])

        # fit node selection to the viewer.
        self.graph.fit_to_selection()

        # Custom builtin widgets from nodegraph
        # ---------------------------------------

        # create a node properties bin widget.
        self.properties_bin = PropertiesBinWidget(node_graph=self.graph)
        self.properties_bin.setWindowFlags(QtCore.Qt.Tool)

        # example show the node properties bin widget when a node is double clicked.
        def display_properties_bin(node):
            if not self.properties_bin.isVisible():
                self.properties_bin.show()

        # wire function to "node_double_clicked" signal.
        self.graph.node_double_clicked.connect(display_properties_bin)

        # create a nodes tree widget.
        self.nodes_tree = NodesTreeWidget(node_graph=self.graph)
        self.nodes_tree.set_category_label('nodegraph.nodes', 'Builtin Nodes')
        self.nodes_tree.set_category_label('nodes.custom.ports', 'Custom Port Nodes')
        self.nodes_tree.set_category_label('nodes.widget', 'Widget Nodes')
        self.nodes_tree.set_category_label('nodes.basic', 'Basic Nodes')
        self.nodes_tree.set_category_label('nodes.group', 'Group Nodes')
        # nodes_tree.show()

        # create a node palette widget.
        self.nodes_palette = NodesPaletteWidget(node_graph=self.graph)
        self.nodes_palette.set_category_label('nodegraph.nodes', 'Builtin Nodes')
        self.nodes_palette.set_category_label('nodes.custom.ports', 'Custom Port Nodes')
        self.nodes_palette.set_category_label('nodes.widget', 'Widget Nodes')
        self.nodes_palette.set_category_label('nodes.basic', 'Basic Nodes')
        self.nodes_palette.set_category_label('nodes.group', 'Group Nodes')

    def custom_default_create_node(self):
        # create node with the QComboBox widget.
        n_combo_menu_1 = self.graph.create_node('nodes.widget.DropdownMenuNode', name='Camera')
        n_combo_menu_2 = self.graph.create_node('nodes.widget.DropdownMenuNode', name='Camera')
        # (connect nodes using the .connect_to method from the port object)
        port = n_combo_menu_2.input(0)
        port.connect_to(n_combo_menu_1.output(0))

    def create_node_click(self):
        self.graph.create_node('nodes.widget.DropdownMenuNode', name='NEW COMBOBOX NODE')

    def save_click(self):
        drop_down_list = self.graph.get_nodes_by_type('nodes.widget.DropdownMenuNode')
        for widget in drop_down_list:
            for name, widget_child in widget.widgets().items():
                print(f"HanhLT: widget_child = {widget_child.get_value()}")
                combo_box: QComboBox = widget_child.get_custom_widget()
                print(f"HanhLT: combo_Box = {combo_box.currentText()}  ")

    def default_init_node(self):
        # create node with custom text color and disable it.
        n_basic_a = self.graph.create_node(
            'nodes.basic.BasicNodeA', text_color='#feab20')
        n_basic_a.set_disabled(True)

        # create node and set a custom icon.
        n_basic_b = self.graph.create_node(
            'nodes.basic.BasicNodeB', name='custom icon')
        this_path = os.path.dirname(os.path.abspath(__file__))
        icon = os.path.join(this_path, 'PySide6NodeGraph/examples', 'star.png')
        n_basic_b.set_icon(icon)

        # create node with the custom port shapes.
        n_custom_ports = self.graph.create_node(
            'nodes.custom.ports.CustomPortsNode', name='custom ports')

        # create node with the embedded QLineEdit widget.
        n_text_input = self.graph.create_node(
            'nodes.widget.TextInputNode', name='text node', color='#0a1e20')

        # create node with the embedded QCheckBox widgets.
        n_checkbox = self.graph.create_node(
            'nodes.widget.CheckboxNode', name='checkbox node')

        # create node with the QComboBox widget.
        n_combo_menu = self.graph.create_node(
            'nodes.widget.DropdownMenuNode', name='combobox node')

        # create group node.
        n_group = self.graph.create_node('nodes.group.MyGroupNode')

        # make node connections.

        # (connect nodes using the .set_output method)
        n_text_input.set_output(0, n_custom_ports.input(0))
        n_text_input.set_output(0, n_checkbox.input(0))
        n_text_input.set_output(0, n_combo_menu.input(0))
        # (connect nodes using the .set_input method)
        n_group.set_input(0, n_custom_ports.output(1))
        n_basic_b.set_input(2, n_checkbox.output(0))
        n_basic_b.set_input(2, n_combo_menu.output(1))
        # (connect nodes using the .connect_to method from the port object)
        port = n_basic_a.input(0)
        port.connect_to(n_basic_b.output(0))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.showMaximized()
    sys.exit(app.exec())
