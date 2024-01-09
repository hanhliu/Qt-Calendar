from PyQt5.QtWidgets import QApplication, QWidget
from pyqt_custom_titlebar_window import CustomTitlebarWindow

if __name__ == "__main__":
  import sys

  app = QApplication(sys.argv)
  window = QWidget()
  customTitlebarWindow = CustomTitlebarWindow(window)
  customTitlebarWindow.setTopTitleBar(title="HanhLT")
  customTitlebarWindow.setMenuAsTitleBar()
  # customTitlebarWindow.setButtonHint(['close'])
  customTitlebarWindow.setButtons()
  customTitlebarWindow.show()
  app.exec_()