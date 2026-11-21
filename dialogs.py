import os
import sys
from PyQt6 .QtWidgets import (QDialog ,QVBoxLayout ,QHBoxLayout ,QLabel ,
QLineEdit ,QPushButton ,QComboBox ,QCheckBox ,
QFileDialog ,QListWidget ,QListWidgetItem ,QMessageBox ,QStackedWidget ,QWidget )
from PyQt6 .QtCore import Qt ,QUrl
from PyQt6 .QtGui import QIcon ,QAction ,QPalette ,QColor
from utils import check_python_file
class BaseDialog (QDialog ):
    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        self .setWindowIcon (QIcon ("LauncherPY.ico"))
        self .setStyleSheet ("""            КДиалог {
                            цвет фона: #1e1e1e;
                            цвет: #ffffff;
                        }
                        QLabel {
                            цвет: #ffffff;
                            размер шрифта: 12 пикселей;
                        }
                        QLineEdit {
                            отступ: 8 пикселей;
                            граница: 2 пикселя, сплошная #666;
                            радиус границы: 5 пикселей;
                            цвет фона: #2d2d2d;
                            цвет: #ffffff;
                            размер шрифта: 12 пикселей;
                        }
                        QLineEdit: фокус {
                            цвет границы: #888;
                        }
                        QComboBox {
                            отступ: 8 пикселей;
                            граница: 2 пикселя, сплошная #666;
                            радиус границы: 5 пикселей;
                            цвет фона: #2d2d2d;
                            цвет: #ffffff;
                            размер шрифта: 12 пикселей;
                        }
                        QComboBox:наведите {
                            цвет границы: #888;
                        }
                        QComboBox::раскрывающийся список {
                            граница: нет;
                        }
                        QComboBox::стрелка вниз {
                            изображение: нет;
                            граница: нет;
                        }
                        QCheckBox {
                            цвет: #ffffff;
                            размер шрифта: 12 пикселей;
                        }
                        QCheckBox::indicator {
                            ширина: 18 пикселей;
                            высота: 18 пикселей;
                            граница: 2 пикселя, сплошная #666;
                            радиус границы: 3 пикселя;
                            цвет фона: #2d2d2d;
                        }
                        QCheckBox::indicator:checked {
                            цвет фона: #888;
                        }
                        QPushButton {
                            отступы: 8 пикселей 16 пикселей;
                            граница: 2 пикселя, сплошная #666;
                            радиус границы: 5 пикселей;
                            цвет фона: #2d2d2d;
                            цвет: #ffffff;
                            размер шрифта: 12 пикселей;
                            начертание шрифта: жирный;
                            минимальная ширина: 100 пикселей;
                        }
                        QPushButton: наведите {
                            цвет фона: #3d3d3d;
                            цвет границы: #888;
                        }
                        QPushButton: нажал {
                            цвет фона: #4d4d4d;
                        }
                        QListWidget {
                            граница: 2 пикселя, сплошная #666;
                            радиус границы: 5 пикселей;
                            цвет фона: #2d2d2d;
                            цвет: #ffffff;
                            размер шрифта: 12 пикселей;
                        }
                        QListWidget::item {
                            отступ: 8 пикселей;
                            нижняя граница: 1 пиксель, сплошной #666;
                        }
                        QListWidget::item:selected {
                            цвет фона: #3d3d3d;
                        }
                        QListWidget::item:hover {
                            цвет фона: #3d3d3d;
                        }""")
class PythonScriptDialog (BaseDialog ):
    def __init__ (self ,parent =None ,app_data =None ):
        super ().__init__ (parent )
        self .app_data =app_data
        self .setWindowTitle ("Добавить Python-скрипт"if not app_data else "Редактировать Python-скрипт")
        self .setMinimumWidth (500 )
        self .setup_ui ()
        if app_data :
            self .load_data (app_data )
    def setup_ui (self ):
        layout =QVBoxLayout (self )
        layout .setSpacing (10 )
        name_layout =QHBoxLayout ()
        name_label =QLabel ("Название:")
        self .name_input =QLineEdit ()
        name_layout .addWidget (name_label )
        name_layout .addWidget (self .name_input )
        layout .addLayout (name_layout )
        path_layout =QHBoxLayout ()
        path_label =QLabel ("Путь к Python-файлу:")
        self .path_input =QLineEdit ()
        browse_btn =QPushButton ("Обзор")
        browse_btn .clicked .connect (self .browse_file )
        path_layout .addWidget (path_label )
        path_layout .addWidget (self .path_input )
        path_layout .addWidget (browse_btn )
        layout .addLayout (path_layout )
        category_layout =QHBoxLayout ()
        category_label =QLabel ("Категория:")
        self .category_combo =QComboBox ()
        self .category_combo .addItems (["Скрипты","Веб-приложения","Утилиты","Другое"])
        category_layout .addWidget (category_label )
        category_layout .addWidget (self .category_combo )
        layout .addLayout (category_layout )
        icon_layout =QHBoxLayout ()
        icon_label =QLabel ("Иконка:")
        self .icon_input =QLineEdit ()
        icon_browse_btn =QPushButton ("Обзор")
        icon_browse_btn .clicked .connect (self .browse_icon )
        icon_layout .addWidget (icon_label )
        icon_layout .addWidget (self .icon_input )
        icon_layout .addWidget (icon_browse_btn )
        layout .addLayout (icon_layout )
        self .autostart_check =QCheckBox ("Запускать при старте")
        layout .addWidget (self .autostart_check )
        desc_layout =QHBoxLayout ()
        desc_label =QLabel ("Описание:")
        self .desc_input =QLineEdit ()
        desc_layout .addWidget (desc_label )
        desc_layout .addWidget (self .desc_input )
        layout .addLayout (desc_layout )
        buttons_layout =QHBoxLayout ()
        save_btn =QPushButton ("Сохранить")
        save_btn .clicked .connect (self .validate_and_accept )
        cancel_btn =QPushButton ("Отмена")
        cancel_btn .clicked .connect (self .reject )
        buttons_layout .addWidget (save_btn )
        buttons_layout .addWidget (cancel_btn )
        layout .addLayout (buttons_layout )
    def load_data (self ,app_data ):
        self .name_input .setText (app_data ["name"])
        self .path_input .setText (app_data ["path"])
        self .category_combo .setCurrentText (app_data ["category"])
        if "icon"in app_data :
            self .icon_input .setText (app_data ["icon"])
        self .autostart_check .setChecked (app_data .get ("autostart",False ))
        self .desc_input .setText (app_data .get ("description",""))
    def browse_file (self ):
        try :
            file_path ,_ =QFileDialog .getOpenFileName (
            self ,"Выберите Python-скрипт","",
            "Python файлы (*.py);;Все файлы (*.*)"
            )
            if file_path :
                self .path_input .setText (file_path )
                if not self .name_input .text ():
                    file_name =os .path .basename (file_path )
                    name =os .path .splitext (file_name )[0 ]
                    self .name_input .setText (name )
        except Exception as e :
            pass
    def browse_icon (self ):
        try :
            file_path ,_ =QFileDialog .getOpenFileName (
            self ,"Выберите иконку","",
            "Изображения (*.png *.jpg *.ico);;Все файлы (*.*)"
            )
            if file_path :
                self .icon_input .setText (file_path )
        except Exception as e :
            pass
    def validate_and_accept (self ):
        try :
            name =self .name_input .text ().strip ()
            path =self .path_input .text ().strip ()
            if not name or not path :
                QMessageBox .warning (self ,"Ошибка","Пожалуйста, заполните название и путь к файлу")
                return
            if not os .path .exists (path ):
                QMessageBox .warning (self ,"Ошибка","Указанный файл не существует")
                return
            if not check_python_file (path ):
                QMessageBox .warning (self ,"Ошибка","Выбранный файл не является Python-скриптом")
                return
            self .accept ()
        except Exception as e :
            pass
    def get_data (self ):
        return {
        "name":self .name_input .text ().strip (),
        "path":self .path_input .text ().strip (),
        "category":self .category_combo .currentText (),
        "icon":self .icon_input .text ().strip (),
        "autostart":self .autostart_check .isChecked (),
        "description":self .desc_input .text ().strip ()
        }
class AddScriptToGroupDialog (BaseDialog ):
    def __init__ (self ,parent =None ,script_data =None ):
        super ().__init__ (parent )
        self .script_data =script_data
        self .setWindowTitle ("Добавить скрипт в группу"if not script_data else "Редактировать скрипт в группе")
        self .setMinimumWidth (500 )
        self .setup_ui ()
        if script_data :
            self .load_data (script_data )
    def setup_ui (self ):
        layout =QVBoxLayout (self )
        layout .setSpacing (10 )
        name_layout =QHBoxLayout ()
        name_label =QLabel ("Название:")
        self .name_input =QLineEdit ()
        name_layout .addWidget (name_label )
        name_layout .addWidget (self .name_input )
        layout .addLayout (name_layout )
        path_layout =QHBoxLayout ()
        path_label =QLabel ("Путь к Python-файлу:")
        self .path_input =QLineEdit ()
        browse_btn =QPushButton ("Обзор")
        browse_btn .clicked .connect (self .browse_file )
        path_layout .addWidget (path_label )
        path_layout .addWidget (self .path_input )
        path_layout .addWidget (browse_btn )
        layout .addLayout (path_layout )
        buttons_layout =QHBoxLayout ()
        save_btn =QPushButton ("Сохранить")
        save_btn .clicked .connect (self .validate_and_accept )
        cancel_btn =QPushButton ("Отмена")
        cancel_btn .clicked .connect (self .reject )
        buttons_layout .addWidget (save_btn )
        buttons_layout .addWidget (cancel_btn )
        layout .addLayout (buttons_layout )
    def load_data (self ,script_data ):
        self .name_input .setText (script_data ["name"])
        self .path_input .setText (script_data ["path"])
    def browse_file (self ):
        try :
            file_path ,_ =QFileDialog .getOpenFileName (
            self ,"Выберите Python-скрипт","",
            "Python файлы (*.py);;Все файлы (*.*)"
            )
            if file_path :
                self .path_input .setText (file_path )
                if not self .name_input .text ():
                    file_name =os .path .basename (file_path )
                    name =os .path .splitext (file_name )[0 ]
                    self .name_input .setText (name )
        except Exception as e :
            pass
    def validate_and_accept (self ):
        try :
            name =self .name_input .text ().strip ()
            path =self .path_input .text ().strip ()
            if not name or not path :
                QMessageBox .warning (self ,"Ошибка","Пожалуйста, заполните название и путь к файлу")
                return
            if not os .path .exists (path ):
                QMessageBox .warning (self ,"Ошибка","Указанный файл не существует")
                return
            if not check_python_file (path ):
                QMessageBox .warning (self ,"Ошибка","Выбранный файл не является Python-скриптом")
                return
            self .accept ()
        except Exception as e :
            pass
    def get_data (self ):
        return {
        "type":"script",
        "name":self .name_input .text ().strip (),
        "path":self .path_input .text ().strip (),
        }
class AddUrlToGroupDialog (BaseDialog ):
    def __init__ (self ,parent =None ,url_data =None ):
        super ().__init__ (parent )
        self .url_data =url_data
        self .setWindowTitle ("Добавить URL в группу"if not url_data else "Редактировать URL в группе")
        self .setMinimumWidth (400 )
        self .setup_ui ()
        if url_data :
            self .load_data (url_data )
    def setup_ui (self ):
        layout =QVBoxLayout (self )
        layout .setSpacing (10 )
        name_layout =QHBoxLayout ()
        name_label =QLabel ("Название:")
        self .name_input =QLineEdit ()
        name_layout .addWidget (name_label )
        name_layout .addWidget (self .name_input )
        layout .addLayout (name_layout )
        url_layout =QHBoxLayout ()
        url_label =QLabel ("URL:")
        self .url_input =QLineEdit ()
        url_layout .addWidget (url_label )
        url_layout .addWidget (self .url_input )
        layout .addLayout (url_layout )
        buttons_layout =QHBoxLayout ()
        save_btn =QPushButton ("Сохранить")
        save_btn .clicked .connect (self .validate_and_accept )
        cancel_btn =QPushButton ("Отмена")
        cancel_btn .clicked .connect (self .reject )
        buttons_layout .addWidget (save_btn )
        buttons_layout .addWidget (cancel_btn )
        layout .addLayout (buttons_layout )
    def load_data (self ,url_data ):
        self .name_input .setText (url_data .get ("name",""))
        self .url_input .setText (url_data .get ("url",""))
    def validate_and_accept (self ):
        try :
            name =self .name_input .text ().strip ()
            url =self .url_input .text ().strip ()
            if not name or not url :
                QMessageBox .warning (self ,"Ошибка","Пожалуйста, заполните название и URL")
                return
            if not url .startswith (("http://","https://")):
                url ="https://"+url
                self .url_input .setText (url )
            self .accept ()
        except Exception as e :
            pass
    def get_data (self ):
        return {
        "type":"url",
        "name":self .name_input .text ().strip (),
        "url":self .url_input .text ().strip ()
        }
class GroupDialog (BaseDialog ):
    def __init__ (self ,parent =None ,group_data =None ,available_scripts =None ):
        super ().__init__ (parent )
        self .group_data =group_data
        self .available_scripts =available_scripts or []
        self .setWindowTitle ("Добавить группу"if not group_data else "Редактировать группу")
        self .setMinimumWidth (600 )
        self .setMinimumHeight (500 )
        self .setup_ui ()
        if group_data :
            self .load_data (group_data )
    def setup_ui (self ):
        layout =QVBoxLayout (self )
        layout .setSpacing (10 )
        name_layout =QHBoxLayout ()
        name_label =QLabel ("Название группы:")
        self .name_input =QLineEdit ()
        name_layout .addWidget (name_label )
        name_layout .addWidget (self .name_input )
        layout .addLayout (name_layout )
        icon_layout =QHBoxLayout ()
        icon_label =QLabel ("Иконка группы:")
        self .icon_input =QLineEdit ()
        icon_browse_btn =QPushButton ("Обзор")
        icon_browse_btn .clicked .connect (self .browse_icon )
        icon_layout .addWidget (icon_label )
        icon_layout .addWidget (self .icon_input )
        icon_layout .addWidget (icon_browse_btn )
        layout .addLayout (icon_layout )
        category_layout =QHBoxLayout ()
        category_label =QLabel ("Категория:")
        self .category_combo =QComboBox ()
        self .category_combo .addItems (["Скрипты","Веб-приложения","Утилиты","Другое"])
        category_layout .addWidget (category_label )
        category_layout .addWidget (self .category_combo )
        layout .addLayout (category_layout )
        self .autostart_check =QCheckBox ("Запускать при старте лаунчера")
        layout .addWidget (self .autostart_check )
        items_label =QLabel ("Элементы группы:")
        layout .addWidget (items_label )
        self .items_list =QListWidget ()
        layout .addWidget (self .items_list )
        items_buttons_layout =QHBoxLayout ()
        add_script_btn =QPushButton ("Добавить скрипт")
        add_url_btn =QPushButton ("Добавить URL")
        remove_item_btn =QPushButton ("Удалить элемент")
        add_script_btn .clicked .connect (self .add_script_to_group )
        add_url_btn .clicked .connect (self .add_url_to_group )
        remove_item_btn .clicked .connect (self .remove_item )
        items_buttons_layout .addWidget (add_script_btn )
        items_buttons_layout .addWidget (add_url_btn )
        items_buttons_layout .addWidget (remove_item_btn )
        layout .addLayout (items_buttons_layout )
        buttons_layout =QHBoxLayout ()
        save_btn =QPushButton ("Сохранить")
        save_btn .clicked .connect (self .validate_and_accept )
        cancel_btn =QPushButton ("Отмена")
        cancel_btn .clicked .connect (self .reject )
        buttons_layout .addWidget (save_btn )
        buttons_layout .addWidget (cancel_btn )
        layout .addLayout (buttons_layout )
    def load_data (self ,group_data ):
        self .name_input .setText (group_data ["name"])
        self .category_combo .setCurrentText (group_data ["category"])
        if "icon"in group_data :
            self .icon_input .setText (group_data ["icon"])
        self .autostart_check .setChecked (group_data .get ("autostart",False ))
        for item in group_data ["items"]:
            display_name =item ["name"]
            if item ["type"]=="url":
                display_name =f"🌐 {display_name }"
            elif item ["type"]=="script":
                display_name =f"🐍 {display_name }"
            list_item =QListWidgetItem (display_name )
            list_item .setData (Qt .ItemDataRole .UserRole ,item )
            self .items_list .addItem (list_item )
    def browse_icon (self ):
        try :
            file_path ,_ =QFileDialog .getOpenFileName (
            self ,"Выберите иконку","",
            "Изображения (*.png *.jpg *.ico);;Все файлы (*.*)"
            )
            if file_path :
                self .icon_input .setText (file_path )
        except Exception as e :
            pass
    def add_script_to_group (self ):
        try :
            dialog =AddScriptToGroupDialog (self )
            if dialog .exec ():
                item_data =dialog .get_data ()
                display_name =f"🐍 {item_data ['name']}"
                list_item =QListWidgetItem (display_name )
                list_item .setData (Qt .ItemDataRole .UserRole ,item_data )
                self .items_list .addItem (list_item )
        except Exception as e :
            pass
    def add_url_to_group (self ):
        try :
            dialog =AddUrlToGroupDialog (self )
            if dialog .exec ():
                item_data =dialog .get_data ()
                display_name =f"🌐 {item_data ['name']}"
                list_item =QListWidgetItem (display_name )
                list_item .setData (Qt .ItemDataRole .UserRole ,item_data )
                self .items_list .addItem (list_item )
        except Exception as e :
            pass
    def remove_item (self ):
        try :
            selected_items =self .items_list .selectedItems ()
            if not selected_items :
                return
            for item in selected_items :
                self .items_list .takeItem (self .items_list .row (item ))
        except Exception as e :
            pass
    def validate_and_accept (self ):
        try :
            name =self .name_input .text ().strip ()
            if not name :
                QMessageBox .warning (self ,"Ошибка","Пожалуйста, введите название группы")
                return
            if self .items_list .count ()==0 :
                QMessageBox .warning (self ,"Ошибка","Добавьте хотя бы один элемент в группу")
                return
            self .accept ()
        except Exception as e :
            pass
    def get_data (self ):
        items =[]
        for i in range (self .items_list .count ()):
            item =self .items_list .item (i ).data (Qt .ItemDataRole .UserRole )
            items .append (item )
        return {
        "name":self .name_input .text ().strip (),
        "category":self .category_combo .currentText (),
        "icon":self .icon_input .text ().strip (),
        "items":items ,
        "autostart":self .autostart_check .isChecked ()
        }
class SettingsDialog (BaseDialog ):
    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        self .setWindowTitle ("Настройки")
        self .setup_ui ()
    def setup_ui (self ):
        layout =QVBoxLayout (self )
        layout .setSpacing (10 )
        self .launcher_autostart =QCheckBox ("Запускать лаунчер при старте Windows")
        layout .addWidget (self .launcher_autostart )
        self .use_venv =QCheckBox ("Использовать виртуальное окружение при запуске скриптов")
        layout .addWidget (self .use_venv )
        self .venv_path_layout =QHBoxLayout ()
        venv_path_label =QLabel ("Путь к виртуальному окружению:")
        self .venv_path_input =QLineEdit ()
        venv_browse_btn =QPushButton ("Обзор")
        venv_browse_btn .clicked .connect (self .browse_venv )
        self .venv_path_layout .addWidget (venv_path_label )
        self .venv_path_layout .addWidget (self .venv_path_input )
        self .venv_path_layout .addWidget (venv_browse_btn )
        layout .addLayout (self .venv_path_layout )
        self .python_path_layout =QHBoxLayout ()
        python_path_label =QLabel ("Путь к Python-интерпретатору:")
        self .python_path_input =QLineEdit ()
        self .python_path_input .setText (sys .executable )
        python_browse_btn =QPushButton ("Обзор")
        python_browse_btn .clicked .connect (self .browse_python )
        self .python_path_layout .addWidget (python_path_label )
        self .python_path_layout .addWidget (self .python_path_input )
        self .python_path_layout .addWidget (python_browse_btn )
        layout .addLayout (self .python_path_layout )
        buttons_layout =QHBoxLayout ()
        save_btn =QPushButton ("Сохранить")
        save_btn .clicked .connect (self .accept )
        cancel_btn =QPushButton ("Отмена")
        cancel_btn .clicked .connect (self .reject )
        buttons_layout .addWidget (save_btn )
        buttons_layout .addWidget (cancel_btn )
        layout .addLayout (buttons_layout )
        self .use_venv .toggled .connect (self .toggle_venv_path )
        self .toggle_venv_path (self .use_venv .isChecked ())
    def toggle_venv_path (self ,checked ):
        self .venv_path_input .setEnabled (checked )
    def browse_venv (self ):
        try :
            dir_path =QFileDialog .getExistingDirectory (self ,"Выберите папку виртуального окружения")
            if dir_path :
                self .venv_path_input .setText (dir_path )
        except Exception as e :
            pass
    def browse_python (self ):
        try :
            file_path ,_ =QFileDialog .getOpenFileName (
            self ,"Выберите Python-интерпретатор","",
            "Исполняемые файлы (*.exe);;Все файлы (*.*)"
            )
            if file_path :
                self .python_path_input .setText (file_path )
        except Exception as e :
            pass
    def get_data (self ):
        return {
        "launcher_autostart":self .launcher_autostart .isChecked (),
        "use_venv":self .use_venv .isChecked (),
        "venv_path":self .venv_path_input .text ().strip (),
        "python_path":self .python_path_input .text ().strip ()
        }