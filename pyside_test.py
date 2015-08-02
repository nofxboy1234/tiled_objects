from PySide.QtGui import *

import tiled_object

class TiledObjectsToGMS(QDialog):
    def __init__(self):
        super(TiledObjectsToGMS, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout_gms_project = QHBoxLayout()
        self.label_gms_project = QLabel('GMS project:')
        self.line_edit_gms_project = QLineEdit()
        self.btn_gms_project = QPushButton("...")
        layout_gms_project.addWidget(self.label_gms_project)
        layout_gms_project.addWidget(self.line_edit_gms_project)
        layout_gms_project.addWidget(self.btn_gms_project)

        layout.addLayout(layout_gms_project)

        layout_tiled_map = QHBoxLayout()
        self.label_tiled_project = QLabel('Tiled project:')
        self.line_edit_tiled_map = QLineEdit()
        self.btn_tiled_map = QPushButton("...")
        layout_tiled_map.addWidget(self.label_tiled_project)
        layout_tiled_map.addWidget(self.line_edit_tiled_map)
        layout_tiled_map.addWidget(self.btn_tiled_map)

        layout.addLayout(layout_tiled_map)

        layout_buttons_gms_to_tiled = QVBoxLayout()
        self.button_gms_to_tiled = QPushButton('GMS -> Tiled')
        layout_buttons_gms_to_tiled.addWidget(self.button_gms_to_tiled)

        layout.addLayout(layout_buttons_gms_to_tiled)

        layout_gmsTiled = QVBoxLayout()
        self.label_tiled_work = QLabel('Do work in Tiled with tilesets and objects')
        self.label_separator = QLabel('*******************************************')
        self.label_gmsTiled = QLabel('Run GMSTiled')
        layout_gmsTiled.addWidget(self.label_tiled_work)
        layout_gmsTiled.addWidget(self.label_separator)
        layout_gmsTiled.addWidget(self.label_gmsTiled)

        layout_tiled_tileset = QHBoxLayout()
        self.label_tiled_tileset = QLabel('Tiled tileset:')
        self.line_edit_tiled_tileset = QLineEdit()
        self.button_tiled_tileset = QPushButton("...")
        layout_tiled_tileset.addWidget(self.label_tiled_tileset)
        layout_tiled_tileset.addWidget(self.line_edit_tiled_tileset)
        layout_tiled_tileset.addWidget(self.button_tiled_tileset)

        layout_gms_background = QHBoxLayout()
        self.label_gms_background = QLabel('GMS background:')
        self.line_edit_gms_background = QLineEdit()
        self.button_gms_background = QPushButton("...")
        layout_gms_background.addWidget(self.label_gms_background)
        layout_gms_background.addWidget(self.line_edit_gms_background)
        layout_gms_background.addWidget(self.button_gms_background)

        layout_gms_room = QHBoxLayout()
        self.label_gms_room = QLabel('GMS room:')
        self.line_edit_gms_room = QLineEdit()
        self.button_gms_room = QPushButton("...")
        layout_gms_room.addWidget(self.label_gms_room)
        layout_gms_room.addWidget(self.line_edit_gms_room)
        layout_gms_room.addWidget(self.button_gms_room)

        layout_gmsTiled.addLayout(layout_tiled_tileset)
        layout_gmsTiled.addLayout(layout_gms_background)
        layout_gmsTiled.addLayout(layout_gms_room)

        layout.addLayout(layout_gmsTiled)

        layout_buttons_tiled_to_gms = QHBoxLayout()
        self.button_tiled_to_gms = QPushButton('GMS <- Tiled')
        layout_buttons_tiled_to_gms.addWidget(self.button_tiled_to_gms)

        layout.addLayout(layout_buttons_tiled_to_gms)

        self.set_connects()

    def set_connects(self):
        self.btn_gms_project.clicked.connect(self.select_gms_project)
        self.btn_tiled_map.clicked.connect(self.select_tiled_map)

        self.button_tiled_tileset.clicked.connect(self.select_tiled_tileset)
        self.button_gms_background.clicked.connect(self.select_gms_background)
        self.button_gms_room.clicked.connect(self.select_gms_room)

        self.button_gms_to_tiled.clicked.connect(self.gms_to_tiled)
        self.button_tiled_to_gms.clicked.connect(self.tiled_to_gms)

    def gms_to_tiled(self):
        gms_project_path = self.line_edit_gms_project.text()
        tiled_project_path = self.line_edit_tiled_map.text()
        tiled_object.gms_to_tiled(gms_project_path, tiled_project_path)

    def tiled_to_gms(self):
        tiled_project_path = self.line_edit_tiled_map.text()
        gms_project_path = self.line_edit_gms_project.text()
        gms_room_path = self.line_edit_gms_room.text()
        tiled_tileset_path = self.line_edit_tiled_tileset.text()
        gms_background_path = self.line_edit_gms_background.text()

        tiled_object.tiled_to_gms(tiled_project_path,
                                    gms_project_path,
                                    gms_room_path,
                                    tiled_tileset_path,
                                    gms_background_path)

    def select_gms_project(self):
        file_name = QFileDialog.getOpenFileName(self,
            "Select GMS project", "C:/", "GMS project files (*.project.gmx)")[0]
        if file_name != "":
            self.line_edit_gms_project.setText(file_name)

    def select_tiled_tileset(self):
        file_name = QFileDialog.getOpenFileName(self,
            "Select tiled tileset", "C:/")[0]
        if file_name != "":
            self.line_edit_tiled_tileset.setText(file_name)

    def select_gms_background(self):
        file_name = QFileDialog.getOpenFileName(self,
            "Select GMS background", "C:/", "GMS background files (*.background.gmx)")[0]
        if file_name != "":
            self.line_edit_gms_background.setText(file_name)

    def select_gms_room(self):
        file_name = QFileDialog.getOpenFileName(self,
            "Select GMS room", "C:/", "GMS room files (*.room.gmx)")[0]
        if file_name != "":
            self.line_edit_gms_room.setText(file_name)

    def select_tiled_map(self):
        file_name = QFileDialog.getOpenFileName(self,
            "Select Tiled map", "C:/", "Tiled map files (*.tmx)")[0]
        if file_name != "":
            self.line_edit_tiled_map.setText(file_name)

app = QApplication([])

dialog = TiledObjectsToGMS()
dialog.show()

app.exec_()
