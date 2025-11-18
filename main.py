# main.py
import sys
from PyQt6.QtWidgets import QApplication

from logic.initial_page_logic import InitialPage   # 导入刚才写的逻辑页面


def main():
    app = QApplication(sys.argv)

    # 创建“开始装调”页面
    window = InitialPage()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
