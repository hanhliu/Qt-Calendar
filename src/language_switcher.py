from PySide6.QtCore import Signal, QObject

class LanguageSwitcher(QObject):
    languageChanged = Signal(str)

    def switchLanguage(self, locale):
        print("HanhLT: locale  ", locale)
        self.languageChanged.emit(locale)
