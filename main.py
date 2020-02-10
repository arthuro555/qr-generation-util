import qrcode
import kivy
import os
from kivy.app import App as Application
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView as FileChooser
from kivy.uix.floatlayout import FloatLayout
from pathlib import Path


class MainWidget:
    def __init__(self, menu_widget, file_widget, folder_widget):
        self.widget = FloatLayout()
        self.menu = menu_widget()
        self.menu.mainParent = self
        self.fileView = file_widget()
        self.folderView = folder_widget()

        self.widget.add_widget(self.menu)

    def request_change(self, change):
        if change == "menu":
            self.widget.clear_widgets()
            self.widget.add_widget(self.menu)
        if change == "file":
            self.widget.clear_widgets()
            self.widget.add_widget(self.fileView)
        if change == "folder":
            self.widget.clear_widgets()
            self.widget.add_widget(self.folderView)

    def get_widget(self):
        return self.widget


class FileScreen(GridLayout):
    def __init__(self, **kwargs):
        super(FileScreen, self).__init__(**kwargs)
        self.fileLock = False
        self.rows = 2
        self.lab1 = Label(text="Cliquez sur un fichier:")

        self.file = FileChooser()
        self.file.path = str(Path().absolute())

        def on_submit(_, __):
            if not self.fileLock:
                self.fileLock = True
                path = [Path(x) for x in self.file.selection]
                for i in path:
                    # Get the filename
                    f = open(i, "r+")
                    filename = f.name
                    f.close()
                    qrcode.make(os.path.basename(filename)).save(Path(filename + ".png"), "png")
                self.fileLock = False

        self.file.on_submit = on_submit

        self.add_widget(self.lab1)
        self.add_widget(self.file)


class FolderScreen(GridLayout):
    def __init__(self, **kwargs):
        super(FolderScreen, self).__init__(**kwargs)
        self.fileLock = False
        self.rows = 3
        self.lab1 = Label(text="Choisisez un dossier:")

        self.file = FileChooser()
        self.file.path = str(Path().absolute())

        self.butt1 = Button()
        self.butt1.text = "Démarrer"

        def on_press():
            if not self.fileLock:
                self.fileLock = True
                path = self.file.path
                p = Path(path)
                for i in [x for x in p.iterdir() if not x.is_dir()]:
                    # Get the filename
                    f = open(i, "r+")
                    filename = f.name
                    f.close()
                    # If it is not a qr code generate
                    if filename.split(".")[-1] != "png":
                        qrcode.make(os.path.basename(filename)).save(Path(filename + ".png"), "png")
                self.fileLock = False

        self.butt1.on_press = on_press

        self.add_widget(self.lab1)
        self.add_widget(self.file)
        self.add_widget(self.butt1)


class Menu(GridLayout):
    def __init__(self):
        super(GridLayout, self).__init__()
        self.rows = 3
        self.label = Label(text="QR Code generation Tool")
        self.fileBtn = Button(text="File by File QR Code Generation")
        self.folderBtn = Button(text="Whole Folder QR Code Generation")

        def folderBtnPress():
            self.mainParent.request_change("folder")

        def fileBtnPress():
            self.mainParent.request_change("file")

        self.folderBtn.on_press = folderBtnPress
        self.fileBtn.on_press = fileBtnPress
        self.label.x += 200
        self.label.y += 200
        self.fileBtn.x += 400

        self.add_widget(self.label)
        self.add_widget(self.fileBtn)
        self.add_widget(self.folderBtn)


class App(Application):

    def build(self):
        mv = MainWidget(Menu, FileScreen, FolderScreen)
        # mv.request_change("file")
        return mv.get_widget()


if __name__ == '__main__':
    App().run()
