import os
import sys
import signal

from PySide6 import QtCore
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QComboBox

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

        self.create_node_graphic()

        # Create a layout for the central widget
        lay = QVBoxLayout(self.central_widget)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(QLabel("HanhLT"))
        lay.addWidget(self.graph_widget)
        self.graph_widget.show()

    def create_node_graphic(self):
        # handle SIGINT to make the app terminate on CTRL+C
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)

        # create graph controller.
        self.graph = NodeGraph()

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

        # show the node graph widget.
        self.graph_widget = self.graph.widget
        self.graph_widget.resize(1100, 800)


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

        widget = self.graph.get_nodes_by_type('nodes.widget.DropdownMenuNode')[0]
        for name, widget_child in widget.widgets().items():
            combo_box: QComboBox = widget_child.get_custom_widget()
            print(f"HanhLT: combo_Box = {combo_box.currentText()}  ")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.showMaximized()
    sys.exit(app.exec())
