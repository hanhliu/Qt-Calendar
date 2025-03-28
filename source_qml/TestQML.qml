import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    width: 900
    height: 400
    border.width: 2
    border.color: "blue"
    color: "lightblue"
    radius: 10

    property bool selecting: false
    property point startPos: Qt.point(0, 0)
    property point endPos: Qt.point(0, 0)

    // The selection rectangle
    Rectangle {
        id: selectionBox
        color: "transparent"
        border.color: "red"
        border.width: 2
        visible: parent.selecting

        x: Math.min(parent.startPos.x, parent.endPos.x)
        y: Math.min(parent.startPos.y, parent.endPos.y)
        width: Math.abs(parent.startPos.x - parent.endPos.x)
        height: Math.abs(parent.startPos.y - parent.endPos.y)
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        drag.target: selectionBox

        onPressed: (mouse) => {
            parent.startPos = Qt.point(mouse.x, mouse.y);
            parent.endPos = Qt.point(mouse.x, mouse.y);
            parent.selecting = true;
        }

        onPositionChanged: (mouse) => {
            if (parent.selecting) {
                parent.endPos = Qt.point(mouse.x, mouse.y);
            }
        }

        onReleased: (mouse) => {
            parent.selecting = false;
            console.log("Selected area:", selectionBox.x, selectionBox.y, selectionBox.width, selectionBox.height);
        }
    }
}
