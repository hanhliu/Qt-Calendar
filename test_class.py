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
        self.list_node_model = []
        self.create_node_graphic()
        # Create a layout for the central widget
        lay = QVBoxLayout(self.central_widget)
        lay.setContentsMargins(0, 0, 0, 0)

        self.button_create_node = QPushButton('Create Node')
        self.button_create_node.clicked.connect(self.create_node_click)

        self.button_save = QPushButton("SAVE")
        self.button_save.clicked.connect(self.save_nodes_to_model)

        self.button_save_by_name = QPushButton('SAVE BY NAME')
        self.button_save_by_name.clicked.connect(self.example_usage)

        self.layout_button = QHBoxLayout()
        self.layout_button.addWidget(self.button_create_node)
        self.layout_button.addWidget(self.button_save)
        self.layout_button.addWidget(self.button_save_by_name)

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
        list_widget = []
        line = widget_nodes.TextInputNode(value='00-camera')
        list_widget.append(line)

        line_1 = widget_nodes.TextInputNode(value='01-camera')
        list_widget.append(line_1)

        line_2 = widget_nodes.TextInputNode(value='02-camera')
        list_widget.append(line_2)

        line_3 = widget_nodes.TextInputNode(value='03-camera')
        list_widget.append(line_3)

        line_4 = widget_nodes.TextInputNode(value='04-camera')
        list_widget.append(line_4)

        line_5 = widget_nodes.TextInputNode(value='05-camera')
        list_widget.append(line_5)

        line_6 = widget_nodes.TextInputNode(value='06-camera')
        list_widget.append(line_6)

        line_7 = widget_nodes.TextInputNode(value='07-camera')
        list_widget.append(line_7)

        line_8 = widget_nodes.TextInputNode(value='08-camera')
        list_widget.append(line_8)

        line_9 = widget_nodes.TextInputNode(value='9-camera')
        list_widget.append(line_9)

        line_10 = widget_nodes.TextInputNode(value='10-camera')
        list_widget.append(line_10)

        line_11 = widget_nodes.TextInputNode(value='11-camera')
        list_widget.append(line_11)

        line_12 = widget_nodes.TextInputNode(value='12-camera')
        list_widget.append(line_12)

        line_13 = widget_nodes.TextInputNode(value='13-camera')
        list_widget.append(line_13)

        line_14 = widget_nodes.TextInputNode(value='14-camera')
        list_widget.append(line_14)

        line_15 = widget_nodes.TextInputNode(value='13-camera')
        list_widget.append(line_15)

        for i, node in enumerate(list_widget):
            self.graph.add_node(node)
            node.set_name(f'Camera-{i}')

        # (connect nodes using the .connect_to method from the port object)
        line_14.set_output(0, line_15.input(0))
        line_13.set_output(0, line_14.input(0))

        line_8.set_output(0, line_13.input(0))
        line_9.set_output(0, line_6.input(0))

        line_7.set_output(0, line_4.input(0))

        line_5.set_output(0, line_1.input(0))
        line_5.set_output(0, line_3.input(0))

        line_10.set_output(0, line_2.input(0))
        line_10.set_output(0, line_8.input(0))
        line_10.set_output(0, line_9.input(0))

        line_12.set_output(0, line_5.input(0))
        line_12.set_output(0, line_7.input(0))
        line_12.set_output(0, line_10.input(0))
        line_12.set_output(0, line_11.input(0))
        line_12.set_output(0, line.input(0))

    def get_sorted_nodes_by_position(self):
        self.graph.auto_layout_nodes()
        
        nodes = self.graph.all_nodes()
        # Ensure each node has a 'scene_pos' method or attribute
        nodes.sort(key=lambda node: (node.x_pos(), node.y_pos()))
        return nodes

    def save_nodes_in_order(self):
        sorted_nodes = self.get_sorted_nodes_by_position()
        visited = set()
        result = []

        def traverse(node):
            if node in visited:
                return
            visited.add(node)
            result.append(node)

            for port in node.output_ports():
                print(f"HanhLT: node.name = {node.name()}")
                print(f"HanhLT: port = {port}")
                list_connected_port_id = port.model.connected_ports
                print(f"HanhLT: connected_port = {list_connected_port_id}")
                for connection_port_id in list_connected_port_id:
                    print(f"HanhLT: connection = {connection_port_id}")
                    connected_node = self.graph.get_node_by_id(connection_port_id)
                    print(f"HanhLT: connected_node = {connected_node}")
                    traverse(connected_node)
                print(f"HanhLT: --------------------------- \n")

        for node in sorted_nodes:
            if node not in visited:
                traverse(node)

        return result

    def get_connected_nodes(self, start_node, max_nodes=9):
        sorted_camera_id_list = []
        seen_ids = set()

        def traverse(node):
            if len(sorted_camera_id_list) >= max_nodes:
                return
            if node not in seen_ids:
                seen_ids.add(node)
                sorted_camera_id_list.append(node)
                for port in node.output_ports():
                    connected_port = port.model.connected_ports
                    for connection in connected_port:
                        connected_node = self.graph.get_node_by_id(connection)
                        traverse(connected_node)

        traverse(start_node)
        return sorted_camera_id_list

    def example_usage(self):
        def add_connected_nodes(node, port_type, nodes_set):
            if port_type == "output":
                ports = node.output_ports()
            elif port_type == "input":
                ports = node.input_ports()

            for port in ports:
                connected_ports = port.model.connected_ports
                for connection in connected_ports:
                    connected_node = self.graph.get_node_by_id(connection)
                    if connected_node not in nodes_set:
                        nodes_set.add(connected_node)
                        if len(list_node) < 9:
                            list_node.append(connected_node)
                        if port_type == "output":
                            list_node_output.append(connected_node)
                        elif port_type == "input":
                            list_node_input.append(connected_node)

        list_node = []
        list_node_output = []
        list_node_input = []
        seen_ids = set()

        # Start with Camera-13
        start_node = self.graph.get_node_by_name('Camera-10')
        list_node.append(start_node)
        seen_ids.add(start_node)

        # First, add all outputs of the start node
        add_connected_nodes(start_node, "output", seen_ids)

        # If not enough, add all inputs of the start node
        if len(list_node) < 9:
            add_connected_nodes(start_node, "input", seen_ids)

        # If still not enough, recursively add outputs of nodes in the list, then their inputs if necessary
        index_output = 0
        while len(list_node) < 9 and (index_output < len(list_node_output)):
            if index_output < len(list_node_output):
                current_node = list_node_output[index_output]
                add_connected_nodes(current_node, "output", seen_ids)
                index_output += 1
        if len(list_node) < 9:
            for node in list_node:
                add_connected_nodes(node, "output", seen_ids)
        index_input = 0
        while len(list_node) < 9 and (index_input < len(list_node_input)):
            if len(list_node) < 9 and index_input < len(list_node_input):
                current_node = list_node_input[index_input]
                add_connected_nodes(current_node, "input", seen_ids)
                index_input += 1
        print(f"HanhLT: list_node = {[node.name() for node in list_node]}")

    # def example_usage(self):
    #     # Example usage with Camera-12
    #     list_node = []
    #     list_node_out_put = []
    #     start_node = self.graph.get_node_by_name('Camera-10')
    #     list_node.append(start_node)
    #     for port_out in start_node.output_ports():
    #         connected_port_out = port_out.model.connected_ports
    #         for connection_out in connected_port_out:
    #             if len(list_node) < 9:
    #                 connected_node_out = self.graph.get_node_by_id(connection_out)
    #                 list_node.append(connected_node_out)
    #                 list_node_out_put.append(connected_node_out)
    #
    #     for port_in in start_node.input_ports():
    #         connected_port_in = port_in.model.connected_ports
    #         for connection_in in connected_port_in:
    #             if len(list_node) < 9:
    #                 connected_node_in = self.graph.get_node_by_id(connection_in)
    #                 list_node.append(connected_node_in)
    #
    #     print(f"HanhLT: list_node = {list_node}")
    #     if len(list_node) < 9:
    #         for node in list_node:
    #             # get child connection of node inside list_node
    #             pass
    #
    #     if start_node:
    #         sorted_camera_id_list = self.get_connected_nodes(start_node)
    #         print([node.name() for node in sorted_camera_id_list])

    def save_nodes_to_model(self):
        self.list_node_model.clear()
        ordered_nodes = self.save_nodes_in_order()
        print(f"HanhLT: ordered_nodes = {ordered_nodes}")
        # for node in ordered_nodes:
        #     node_name = node.name()
        #     for idx, widget_child in node.widgets().items():
        #         current_camera_value = widget_child.get_value()  # Assuming get_value returns the QLineEdit text
        #         dict_input_connect = node.connected_input_nodes()
        #         dict_output_connect = node.connected_output_nodes()
        #
        #         input_list = []
        #         output_list = []
        #
        #         for key_input, value_input in dict_input_connect.items():
        #             if len(value_input) > 0:
        #                 for input_node in value_input:
        #                     input_list.append(input_node.name())
        #
        #         for key_output, value_output in dict_output_connect.items():
        #             if len(value_output) > 0:
        #                 for output_node in value_output:
        #                     output_list.append(output_node.name())
        #
        #         node_model = {'node_name': node_name,
        #                       'current_value': current_camera_value,
        #                       'input_list': input_list,
        #                       'output_list': output_list}
        #
        #         self.list_node_model.append(node_model)
        #
        #     # Print the saved node models
        # for item in self.list_node_model:
        #     print(f"HanhLT: item.name = {item['node_name']} ")
        #           # f" item_value={item.current_value}   "
        #           # f"item_input_list = {item.input_list}     item_output_list = {item.output_list}")

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
