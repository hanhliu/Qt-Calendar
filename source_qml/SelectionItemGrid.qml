import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
                                
    width: 32
    height: 32
    property int row: Math.floor(index / 24)
    property int col: index % 24
    Rectangle {
        id: cell
        anchors.fill: parent
        border.width: 1
        color: selectionManager.isSelected(row, col) ? "orange" : "lightblue"
        border.color: "black"
    }
    MouseArea {
        anchors.fill: parent
        onClicked: selectionManager.selectRow(row) // Example for row selection
    }
    Connections {
        target: selectionManager
        function onSelectionChanged() {
            cell.color = selectionManager.isSelected(row, col) ? "orange" : "lightblue";
        }
    }
}