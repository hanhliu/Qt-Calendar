import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic

Rectangle {
    // anchors.fill: parent
    border.width: 2
    border.color: "blue"
    width: 880
    height: 450
    radius: 10
    
    Column { 
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: 10
        Layout.fillWidth: true
        spacing: 10
        
        Rectangle{
            width: parent.width
            height: 50
            RowLayout { 
                spacing: 2
                anchors.fill: parent

                Rectangle{
                    Layout.fillWidth: true  // 🔹 Expands to take available space
                    Layout.preferredWidth: 1  // Ensures equal expansion
                    height: parent.height
                    Row{ 
                        spacing: 30
                        // anchors.centerIn: parent
                        anchors.left: parent.left
                        anchors.verticalCenter: parent.verticalCenter
                        // 🟢 First Widget (Image + Text)
                        Row {
                            id: row_record
                            spacing: 8 
                            Layout.alignment: Qt.AlignVCenter
                            Rectangle {
                                id: rec_record
                                width: 160
                                height: 40
                                radius: 4
                                property bool is_select_record: true 
                                Layout.alignment: Qt.AlignCenter
                                MouseArea {
                                    anchors.fill: parent  
                                    onClicked: {
                                        rec_record.is_select_record = true
                                        rec_no_record.is_select_not_record = false
                                        selectionManager.setRecordMode(true);
                                        }
                                    Layout.alignment: Qt.AlignCenter
                                    Row{
                                        spacing: 8 
                                        anchors.centerIn: parent
                                        Rectangle {
                                            width: 16
                                            height: 16
                                            radius: width/2
                                            color: "#1CD1A1"
                                        }
                                        Text {
                                            text: "Record Always"
                                        }
                                    }
                                }
                                // Apply border effect when selected
                                border.width: rec_record.is_select_record ? 1 : 0
                                border.color: "#1CD1A1"
                            }
                        }

                        // 🔵 Second Widget (Image + Text)
                        Row {
                            id: row_no_record
                            spacing: 8 
                            Layout.alignment: Qt.AlignVCenter
                            Rectangle {
                                id: rec_no_record
                                width: 160
                                height: 40
                                radius: 4
                                property bool is_select_not_record: false 
                                Layout.alignment: Qt.AlignCenter
                                MouseArea {
                                    anchors.fill: parent  
                                    onClicked: {
                                        rec_no_record.is_select_not_record = true
                                        rec_record.is_select_record = false
                                        selectionManager.setRecordMode(false);
                                    }
                                    Layout.alignment: Qt.AlignCenter
                                    Row{
                                        spacing: 8 
                                        anchors.centerIn: parent
                                        Rectangle {
                                            width: 16
                                            height: 16
                                            radius: width/2
                                            color: "#525252"
                                        }
                                        Text {
                                            text: "Do Not Record"
                                        }
                                    }
                                }
                                // Apply border effect when selected
                                border.width: rec_no_record.is_select_not_record ? 1 : 0
                                border.color: "#1CD1A1"
                            }
                        }
                    }
                }
                
                Rectangle{
                    Layout.fillWidth: true  // 🔹 Expands to take available space
                    Layout.preferredWidth: 1  // Ensures equal expansion
                    height: parent.height
                    // 🔴 Third Widget (Button)
                    Button {
                        anchors.right: parent.right
                        anchors.verticalCenter: parent.verticalCenter
                        height: 40
                        text: "Copy Schedule to..."
                        background: Rectangle {
                            color: "#1CD1A1"  // Green button
                            radius: 4
                            border.color: "#0FA374"
                            border.width: 1
                        }

                        contentItem: Text {
                            text: parent.text
                            font.bold: true
                            color: "white"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                    }
                }
            }
        }

        ColumnLayout {
            spacing: 2
            Layout.alignment: Qt.AlignCenter
            // 🟢 Grid for Hour Selection (Columns)
            Rectangle {
                id: rec4
                Layout.preferredHeight: 32
                Grid {
                    id: grid_hour
                    columns: 25
                    spacing: 2

                    Repeater {
                        model: 25
                        Item {
                            width: 32
                            height: 32
                            Rectangle {
                                anchors.fill: parent
                                border.width: 1
                                color: "lightblue"
                                border.color: "black"
                                Text {
                                    anchors.centerIn: parent
                                    text: index === 0 ? qsTr("ALL") : (index - 1).toString().padStart(2, '0')
                                }
                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: {
                                        
                                        if (index === 0) {
                                            console.log("ALL Clicked");
                                            selectionManager.selectAll();
                                        } else {
                                            selectionManager.selectColumn(index - 1);
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            Row {
                spacing: 2
                Layout.alignment: Qt.AlignHCenter 
                // 🔵 Grid for Day Selection (Rows)
                Grid {
                    id: grid_day
                    columns: 1
                    spacing: 2

                    Repeater {
                        model: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                        Item {
                            width: 32
                            height: 32
                            Rectangle {
                                anchors.fill: parent
                                border.width: 1
                                color: "lightblue"
                                border.color: "black"
                                Text {
                                    anchors.centerIn: parent
                                    text: modelData
                                }
                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: selectionManager.selectRow(index)
                                }
                            }
                        }
                    }
                }

                Rectangle {
                    id: gridContainer
                    width: grid_option.width
                    height: grid_option.height
                    color: "transparent"

                    property bool selecting: false
                    property point startPos: Qt.point(0, 0)
                    property point endPos: Qt.point(0, 0)

                    // 🔴 Grid for Option Selection (Main Table)
                    Grid {
                        id: grid_option
                        columns: 24
                        spacing: 2

                        Repeater {
                            model: 168
                            Item {
                                width: 32
                                height: 32
                                property int row: Math.floor(index / 24)
                                property int col: index % 24
                                property bool isHovered: false
                                Rectangle {
                                    id: cell
                                    anchors.fill: parent
                                    border.width: 1
                                    color: selectionManager.isSelected(row, col) ? "orange" : "lightblue"
                                    border.color: "black"
                                    Text{
                                        id: text_fps
                                        visible: false
                                        anchors.top: parent.top
                                        anchors.left: parent.left
                                        anchors.margins: 4
                                        text: "20"
                                        font.pixelSize: 11

                                    }
                                    Text{
                                        id: text_quality
                                        visible: false
                                        anchors.right: parent.right
                                        anchors.bottom: parent.bottom
                                        anchors.margins: 4
                                        text: "Hi"
                                        font.pixelSize: 11

                                    }
                                }
                                MouseArea {
                                    anchors.fill: parent
                                    hoverEnabled: true
                                    onClicked: {
                                        selectionManager.selectCell(row, col);
                                        parent.isHovered = false;
                                    }
                                    onEntered: parent.isHovered = true;
                                    onExited: parent.isHovered = false;
                                    
                                }
                                Connections {
                                    target: selectionManager
                                    function onSelectionChanged() {
                                        let selected = selectionManager.isSelected(row, col);
                                        cell.color = selected ? "orange" : "lightblue";
                                        text_fps.visible = selected;
                                        text_quality.visible = selected;

                                        text_fps.text = selectionManager.fps_value;
                                        text_quality.text = selectionManager.quality_text_value; // For example
                                    }
                                }
                            }
                        }
                    }

                    // 🔴 Selection Rectangle (Visible while dragging)
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

                    // 🔴 MouseArea for Drag Selection
                    MouseArea {
                        id: dragArea
                        anchors.fill: parent

                        onPressed: (mouse) => {
                            let mappedStart = grid_option.mapFromItem(dragArea, mouse.x, mouse.y);
                            parent.startPos = Qt.point(mappedStart.x, mappedStart.y);
                            parent.endPos = Qt.point(mappedStart.x, mappedStart.y);
                            parent.selecting = true;
                            selectionManager.startDrag();
                            
                            // Handle single click (if the user does not drag)
                            
                        }

                        onPositionChanged: (mouse) => {
                            if (parent.selecting) {
                                let mappedEnd = grid_option.mapFromItem(dragArea, mouse.x, mouse.y);
                                parent.endPos = Qt.point(mappedEnd.x, mappedEnd.y);
                                selectionManager.selectInRange(grid_option, parent.startPos, parent.endPos);
                            }
                        }

                        onReleased: (mouse) => {
                            let gridX = Math.floor(mouse.x / 34); // 32px cell + 2px spacing
                            let gridY = Math.floor(mouse.y / 34);
                            selectionManager.selectCell(gridY, gridX);

                            parent.selecting = false;

                        }
                    }
                }
            }
        } 
        // 🔴 Horizontal Divider
        Rectangle {
            width: parent.width
            height: 2  // Adjust thickness
            color: "gray"  // Divider color
        }
        // Another section below the divider
        Rectangle {
            width: parent.width
            height: 72

            RowLayout { 
                spacing: 12
                anchors.fill: parent

                Rectangle {
                    Layout.fillWidth: true  // 🔹 Expands to take available space
                    Layout.preferredWidth: 1  // Ensures equal expansion
                    height: parent.height
                    radius: 4
                    Layout.alignment: Qt.AlignLeft
                    border.width: 2
                    border.color: "#1CD1A1"

                    ColumnLayout{
                        spacing: 10
                        anchors.centerIn: parent 
                        Layout.fillWidth: true

                        Text {
                            Layout.alignment: Qt.AlignCenter
                            text: "Keep Archive for..."
                            font.bold: true
                        }

                        RowLayout{
                            spacing: 10
                            Layout.alignment: Qt.AlignBottom

                            Text {
                                text: "Max"
                                Layout.preferredWidth: 40   // ✅ Set a preferred width
                            }

                            SpinBox {
                                id: archieve_time_spinbox
                                from: 1
                                to: 9999
                                height: 30
                                editable: true
                                enabled: true
                                leftPadding: topPadding
                                rightPadding: height
                                value: selectionManager.time_archieve

                                contentItem: Item {
                                    anchors.left: archieve_time_spinbox.left
                                    anchors.top: archieve_time_spinbox.top
                                    anchors.bottom: archieve_time_spinbox.bottom

                                    implicitWidth: archieve_time_input.implicitWidth
                                    implicitHeight: archieve_time_input.implicitHeight

                                    width: archieve_time_spinbox.width - archieve_time_spinbox.height
                                    height: archieve_time_spinbox.height

                                    TextInput {
                                        id: archieve_time_input
                                        anchors.fill: parent
                                        text: archieve_time_spinbox.textFromValue(archieve_time_spinbox.value)
                                        color: "black"
                                        horizontalAlignment: Qt.AlignHCenter
                                        verticalAlignment: Qt.AlignVCenter
                                        readOnly: !archieve_time_spinbox.editable
                                        validator: archieve_time_spinbox.validator
                                        inputMethodHints: Qt.ImhFormattedNumbersOnly
                                        onTextChanged: {
                                            var newValue = parseInt(text);
                                            selectionManager.time_archieve = newValue;
                                            console.log(newValue)
                                        }
                                    }
                                }

                                up.indicator: Rectangle {
                                    anchors.top: archieve_time_spinbox.top
                                    anchors.right: archieve_time_spinbox.right
                                    anchors.topMargin: 1
                                    anchors.rightMargin: 1
                                    height: archieve_time_spinbox.height* 0.5
                                    width: archieve_time_spinbox.height* 0.8
                                    color: "gold"
                                    Text {
                                        text: '+'
                                        anchors.centerIn: parent
                                    }
                                }

                                down.indicator: Rectangle {
                                    anchors.bottom: archieve_time_spinbox.bottom
                                    anchors.right: archieve_time_spinbox.right
                                    anchors.bottomMargin: 1
                                    anchors.rightMargin: 1
                                    height: archieve_time_spinbox.height* 0.5
                                    width: archieve_time_spinbox.height* 0.8
                                    color: "orange"
                                    Text {
                                        text: '-'
                                        anchors.centerIn: parent
                                    }
                                }

                                background: Rectangle {
                                    implicitWidth: 100
                                    implicitHeight: 30
                                    height: archieve_time_spinbox.height
                                    border.color: "red"
                                    border.width: 1
                                    radius: 2
                                    
                                }

                                
                            }

                            ComboBox {
                                id: unit_dropdown
                                width: 200
                                height: 30  // ✅ Set dropdown height
                                model: ["Minutes", "Hours", "Days"]  // ✅ Dropdown items
                                currentIndex: selectionManager.time_unit_index

                                onCurrentIndexChanged: {
                                    selectionManager.time_unit_index = currentIndex  // 🔹 Update Python variable
                                }

                                background: Rectangle {
                                    implicitWidth: 100
                                    implicitHeight: 30 // Light gray background
                                    border.color: "#1CD1A1"
                                    border.width: 1
                                    radius: 2
                                }

                                contentItem: Text {
                                    text: unit_dropdown.displayText
                                    verticalAlignment: Text.AlignVCenter
                                    horizontalAlignment: Text.AlignHCenter
                                }

                                popup: Popup {
                                    y: unit_dropdown.height
                                    width: unit_dropdown.width
                                    height: 150  // ✅ Set dropdown height

                                    background: Rectangle {
                                        color: "white"
                                        border.color: "gray"
                                        border.width: 1
                                        radius: 4
                                    }
                                    

                                    contentItem: ListView {
                                        clip: true
                                        model: unit_dropdown.model

                                        delegate: ItemDelegate {
                                            width: unit_dropdown.width
                                            height: 30  // ✅ Set dropdown item height
                                            highlighted: unit_dropdown.currentIndex === index

                                            contentItem: Text {
                                                text: modelData
                                                color: highlighted ? "white" : "black"
                                                verticalAlignment: Text.AlignVCenter
                                                horizontalAlignment: Text.AlignLeft
                                            }

                                            background: Rectangle {
                                                color: highlighted ? "#1CD1A1" : "transparent"  // Highlight selection
                                            }

                                            onClicked: {
                                                unit_dropdown.currentIndex = index;
                                                unit_dropdown.popup.close();  // 🔹 Manually close the popup
                                            }
                                        }
                                    }
                                }
                            }


                            RowLayout {
                                spacing: 4  // Adjust spacing as needed

                                CheckBox {
                                    id: checkBox
                                    checked: true
                                    onCheckedChanged: console.log("Checked:", checked)
                                }

                                Text {
                                    text: "Auto"
                                }
                            }

                        }
                    }
                    
                }
                

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredWidth: 1
                    height: parent.height
                    radius: 4
                    Layout.alignment: Qt.AlignRight
                    border.width: 2
                    border.color: "#1c95d1"
                    ColumnLayout{
                        spacing: 10
                        anchors.centerIn: parent 
                        Layout.fillWidth: true

                        Text {
                            Layout.alignment: Qt.AlignCenter
                            text: "Schedule Settings"
                            font.bold: true
                        }

                        RowLayout{
                            spacing: 24
                            Layout.alignment: Qt.AlignBottom

                            RowLayout{
                                Text{
                                    text: "FPS"
                                }
                                SpinBox{
                                    id: fps_spinbox
                                    from: 1
                                    to: 50
                                    height: 30
                                    editable: true
                                    enabled: true
                                    leftPadding: topPadding
                                    rightPadding: height
                                    value: selectionManager.fps_value
                                    
                                    contentItem: Item {
                                        anchors.left: fps_spinbox.left
                                        anchors.top: fps_spinbox.top
                                        anchors.bottom: fps_spinbox.bottom

                                        implicitWidth: fps_input.implicitWidth
                                        implicitHeight: fps_input.implicitHeight

                                        width: fps_spinbox.width - fps_spinbox.height
                                        height: fps_spinbox.height

                                        TextInput {
                                            id: fps_input
                                            anchors.fill: parent
                                            text: fps_spinbox.textFromValue(fps_spinbox.value, fps_spinbox.locale)
                                            color: "black"
                                            horizontalAlignment: Qt.AlignHCenter
                                            verticalAlignment: Qt.AlignVCenter
                                            readOnly: !fps_spinbox.editable
                                            validator: fps_spinbox.validator
                                            inputMethodHints: Qt.ImhFormattedNumbersOnly

                                            onTextChanged: {
                                                var newValue = parseInt(text);
                                                selectionManager.fps_value = newValue;
                                            }
                                        }
                                    }

                                    up.indicator: Rectangle {
                                        anchors.top: fps_spinbox.top
                                        anchors.right: fps_spinbox.right
                                        anchors.topMargin: 1
                                        anchors.rightMargin: 1
                                        height: fps_spinbox.height* 0.5
                                        width: fps_spinbox.height* 0.8
                                        color: "gold"
                                        Text {
                                            text: '+'
                                            anchors.centerIn: parent
                                        }
                                    }

                                    down.indicator: Rectangle {
                                        anchors.bottom: fps_spinbox.bottom
                                        anchors.right: fps_spinbox.right
                                        anchors.bottomMargin: 1
                                        anchors.rightMargin: 1
                                        height: fps_spinbox.height* 0.5
                                        width: fps_spinbox.height* 0.8
                                        color: "orange"
                                        Text {
                                            text: '-'
                                            anchors.centerIn: parent
                                        }
                                    }

                                    background: Rectangle {
                                        implicitWidth: 100
                                        implicitHeight: 30
                                        height: fps_spinbox.height
                                        border.color: "red"
                                        border.width: 1
                                        radius: 2
                                        
                                    }
                                }
                            }

                            RowLayout{
                                Text{
                                    text: "Quality"
                                }
                                ComboBox {
                                    id: qualitySelector
                                    width: 200
                                    height: 30  // ✅ Set dropdown height
                                    model: ["Low", "Medium", "High", "Best"]  // ✅ Dropdown items
                                    currentIndex: selectionManager.quality_index

                                    onCurrentIndexChanged: {
                                        selectionManager.quality_index = currentIndex  // 🔹 Update Python variable
                                    }

                                    background: Rectangle {
                                        implicitWidth: 100
                                        implicitHeight: 30 // Light gray background
                                        border.color: "#1CD1A1"
                                        border.width: 1
                                        radius: 2
                                    }

                                    contentItem: Text {
                                        text: qualitySelector.displayText
                                        verticalAlignment: Text.AlignVCenter
                                        horizontalAlignment: Text.AlignHCenter
                                    }

                                    popup: Popup {
                                        y: qualitySelector.height
                                        width: qualitySelector.width
                                        height: 150  // ✅ Set dropdown height

                                        background: Rectangle {
                                            color: "white"
                                            border.color: "gray"
                                            border.width: 1
                                            radius: 4
                                        }
                                        

                                        contentItem: ListView {
                                            clip: true
                                            model: qualitySelector.model

                                            delegate: ItemDelegate {
                                                width: qualitySelector.width
                                                height: 30  // ✅ Set dropdown item height
                                                highlighted: qualitySelector.currentIndex === index

                                                contentItem: Text {
                                                    text: modelData
                                                    color: highlighted ? "white" : "black"
                                                    verticalAlignment: Text.AlignVCenter
                                                    horizontalAlignment: Text.AlignLeft
                                                }

                                                background: Rectangle {
                                                    color: highlighted ? "#1CD1A1" : "transparent"  // Highlight selection
                                                }

                                                onClicked: qualitySelector.currentIndex = index
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
