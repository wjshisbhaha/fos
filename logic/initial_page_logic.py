# initial_page_page.py
# 这个文件负责封装 initial_page 的逻辑

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox

from logic.decoration_page_logic import DecorationPage


from ui.initial_page import Ui_start_to_adjust   # <-- 这里换成你 pyuic6 生成的那个文件名


class InitialPage(QtWidgets.QWidget):
    """开始装调页面：封装 Ui_widget + 逻辑"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建 UI 对象并在当前 QWidget 上布置界面
        self.ui = Ui_start_to_adjust()
        self.ui.setupUi(self)

        # 做一些初始化逻辑
        self.init_logic()

    def init_logic(self):
        """信号连接 + 默认状态设置"""
        # 默认选中样机A
        self.ui.prototype_rd_A.setChecked(True)

        # 按钮点击逻辑
        self.ui.start_to_adjust_btn.clicked.connect(self.on_start_clicked)

    def on_start_clicked(self):
        """点击“开始装调”后的逻辑"""
        name = self.ui.prototype_name.text().strip()

        if not name:
            QMessageBox.warning(self, "提示", "请先输入样机名称！")
            return

        self._open_decoration_page(name)

    def _open_decoration_page(self, name: str):
        """打开装调主页面并传递样机信息，只在顶部展示一次样机名。"""

        self.decoration_window = DecorationPage(prototype_name=name)
        self.decoration_window.setWindowTitle("装调主页面")
        self.decoration_window.resize(1400, 900)
        self.decoration_window.show()
        self.close()
