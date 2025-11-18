from PyQt6 import QtCore, QtGui, QtWidgets


class NavigationButton(QtWidgets.QToolButton):
    """A simple navigation button that supports collapsed/expanded layouts."""

    def __init__(self, text: str, icon: QtGui.QIcon | None, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.full_text = text
        if icon is not None:
            self.setIcon(icon)
        self.setText(text)
        self.setCheckable(True)
        self.setToolButtonStyle(
            QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon
            if icon is not None
            else QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly
        )
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(42)

    def set_collapsed(self, collapsed: bool):
        if collapsed:
            if not self.icon().isNull():
                self.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
                self.setText("")
            else:
                self.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly)
                self.setText(self.full_text[:2])
        else:
            self.setToolButtonStyle(
                QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon
                if not self.icon().isNull()
                else QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly
            )
            self.setText(self.full_text)


class CommonContentWidget(QtWidgets.QWidget):
    """Shared three-column content area to host embedded pages."""

    def __init__(self, title: str, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        header = QtWidgets.QLabel(title)
        header.setObjectName("contentHeader")
        header.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(header)

        columns = QtWidgets.QHBoxLayout()
        columns.setSpacing(16)
        layout.addLayout(columns, 1)

        self.tx_group = self._build_group_box("发射")
        self.power_group = self._build_group_box("功率计")
        self.table_group = self._build_group_box("表格")

        columns.addWidget(self.tx_group)
        columns.addWidget(self.power_group)
        columns.addWidget(self.table_group)

    def _build_group_box(self, title: str) -> QtWidgets.QGroupBox:
        box = QtWidgets.QGroupBox(title)
        box.setObjectName("contentGroup")
        layout = QtWidgets.QVBoxLayout(box)
        placeholder = QtWidgets.QLabel("可插入其他页面或组件…")
        placeholder.setObjectName("placeholderLabel")
        placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        placeholder.setWordWrap(True)
        layout.addWidget(placeholder, 1)
        return box


class Ui_decoration_page(object):
    def setupUi(self, decoration_page: QtWidgets.QWidget):
        decoration_page.setObjectName("decoration_page")
        decoration_page.resize(1400, 900)

        self.main_layout = QtWidgets.QHBoxLayout(decoration_page)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QtWidgets.QFrame(parent=decoration_page)
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setMinimumWidth(78)
        self.sidebar.setMaximumWidth(320)
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(12, 16, 12, 16)
        self.sidebar_layout.setSpacing(12)

        # Toggle and branding row
        top_row = QtWidgets.QHBoxLayout()
        top_row.setSpacing(8)
        self.toggle_btn = QtWidgets.QToolButton(parent=self.sidebar)
        self.toggle_btn.setObjectName("toggleButton")
        self.toggle_btn.setAutoRaise(True)
        self.toggle_btn.setIcon(decoration_page.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowBack))
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        top_row.addWidget(self.toggle_btn, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        top_row.addStretch(1)
        self.sidebar_layout.addLayout(top_row)

        # Primary navigation
        self.nav_container = QtWidgets.QFrame(parent=self.sidebar)
        self.nav_container.setObjectName("navContainer")
        self.nav_layout = QtWidgets.QVBoxLayout(self.nav_container)
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_layout.setSpacing(6)

        style = decoration_page.style()
        nav_items = [
            ("开始装调", style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaPlay)),
            ("装调流程", style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_FileDialogListView)),
            ("配置信息", style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_FileDialogDetailedView)),
        ]
        self.nav_buttons: list[NavigationButton] = []
        for text, icon in nav_items:
            btn = NavigationButton(text, icon, self.nav_container)
            self.nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        self.nav_layout.addStretch(1)
        self.sidebar_layout.addWidget(self.nav_container, 1)

        # Main content stack
        self.content_container = QtWidgets.QFrame(parent=decoration_page)
        self.content_container.setObjectName("contentContainer")
        self.content_layout = QtWidgets.QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(12)

        self.header_bar = QtWidgets.QFrame(parent=self.content_container)
        self.header_bar.setObjectName("headerBar")
        header_layout = QtWidgets.QHBoxLayout(self.header_bar)
        header_layout.setContentsMargins(0, 0, 0, 0)
        self.title_label = QtWidgets.QLabel("开始装调", parent=self.header_bar)
        self.title_label.setObjectName("titleLabel")
        header_layout.addWidget(self.title_label, 1)

        self.prototype_tag = QtWidgets.QLabel("样机未选择", parent=self.header_bar)
        self.prototype_tag.setObjectName("prototypeTag")
        self.prototype_tag.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        header_layout.addWidget(self.prototype_tag, 0)

        self.content_layout.addWidget(self.header_bar)

        self.main_stack = QtWidgets.QStackedWidget(parent=self.content_container)
        self.main_stack.setObjectName("mainStack")
        self.content_layout.addWidget(self.main_stack, 1)

        self.log_panel = QtWidgets.QGroupBox("日志", parent=self.content_container)
        self.log_panel.setObjectName("logPanel")
        log_layout = QtWidgets.QVBoxLayout(self.log_panel)
        log_layout.setContentsMargins(12, 8, 12, 12)
        log_layout.setSpacing(8)
        self.log_view = QtWidgets.QPlainTextEdit(parent=self.log_panel)
        self.log_view.setObjectName("logView")
        self.log_view.setReadOnly(True)
        self.log_view.setPlaceholderText("在此处显示装调过程日志…")
        log_layout.addWidget(self.log_view)
        self.content_layout.addWidget(self.log_panel)

        # Start adjustment page with steps inside
        self.start_page = self._build_start_adjust_page()
        self.main_stack.addWidget(self.start_page)

        # Other primary pages
        self.flow_page = self._build_simple_page("装调流程", "这里展示装调流程相关内容。")
        self.config_page = self._build_simple_page("配置信息", "这里展示配置信息或配置表单。")
        self.main_stack.addWidget(self.flow_page)
        self.main_stack.addWidget(self.config_page)

        self.main_layout.addWidget(self.sidebar, 0)
        self.main_layout.addWidget(self.content_container, 1)

        QtCore.QMetaObject.connectSlotsByName(decoration_page)
        self._apply_style(decoration_page)

    def _build_start_adjust_page(self) -> QtWidgets.QWidget:
        page = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(page)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        left_panel = QtWidgets.QFrame(parent=page)
        left_panel.setObjectName("stepRail")
        left_panel.setMinimumWidth(200)
        left_panel.setMaximumWidth(280)
        left_layout = QtWidgets.QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)

        self.step_buttons: list[NavigationButton] = []
        step_names = [
            "信号发",
            "信号收",
            "二向色镜装调",
            "相机装调",
            "信标光",
            "同轴度",
            "功率测试",
            "样机总结",
            "样机交付",
        ]
        self.step_names = step_names
        for idx, name in enumerate(step_names):
            btn = NavigationButton(name, None, page)
            btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
            left_layout.addWidget(btn)
            self.step_buttons.append(btn)

            if name == "同轴度":
                self.substep_frame = QtWidgets.QFrame(parent=page)
                self.substep_frame.setObjectName("subStepFrame")
                substep_layout = QtWidgets.QVBoxLayout(self.substep_frame)
                substep_layout.setContentsMargins(18, 4, 0, 4)
                substep_layout.setSpacing(6)
                self.sub_step_buttons: list[NavigationButton] = []
                sub_step_names = ["信号收发同轴度", "信标收发同轴度"]
                self.sub_step_names = sub_step_names
                for sub_name in sub_step_names:
                    sub_btn = NavigationButton(sub_name, None, self.substep_frame)
                    sub_btn.setIcon(QtGui.QIcon())
                    sub_btn.setCheckable(True)
                    sub_btn.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly)
                    sub_btn.setSizePolicy(
                        QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
                    )
                    substep_layout.addWidget(sub_btn)
                    self.sub_step_buttons.append(sub_btn)
                self.substep_frame.hide()
                left_layout.addWidget(self.substep_frame)

        left_layout.addStretch(1)

        right_panel = QtWidgets.QWidget(parent=page)
        right_layout = QtWidgets.QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)

        self.step_stack = QtWidgets.QStackedWidget(parent=right_panel)
        self.step_stack.setObjectName("stepStack")
        right_layout.addWidget(self.step_stack, 1)

        layout.addWidget(left_panel)
        layout.addWidget(right_panel, 1)

        for idx, name in enumerate(step_names, start=1):
            if name == "同轴度":
                container = QtWidgets.QWidget()
                container_layout = QtWidgets.QVBoxLayout(container)
                container_layout.setSpacing(8)
                hint = QtWidgets.QLabel("选择具体的同轴度子步骤以展示对应的公共组件页面。")
                hint.setObjectName("hintLabel")
                hint.setWordWrap(True)
                container_layout.addWidget(hint)

                self.sub_step_stack = QtWidgets.QStackedWidget(parent=container)
                self.sub_step_stack.setObjectName("subStepStack")
                for sub_name in self.sub_step_names:
                    sub_page = CommonContentWidget(f"同轴度 - {sub_name}", parent=self.sub_step_stack)
                    self.sub_step_stack.addWidget(sub_page)
                container_layout.addWidget(self.sub_step_stack, 1)
                self.step_stack.addWidget(container)
            else:
                self.step_stack.addWidget(self._build_step_page(name))

        return page

    def _build_step_page(self, name: str) -> QtWidgets.QWidget:
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QtWidgets.QLabel(name)
        title.setObjectName("contentHeader")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(title)

        body = QtWidgets.QLabel(f"{name} 的独立页面内容区域，可在添加 UI 时嵌入具体组件。")
        body.setObjectName("placeholderLabel")
        body.setWordWrap(True)
        body.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(body, 1)

        return page

    def _build_simple_page(self, title: str, description: str) -> QtWidgets.QWidget:
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title_label = QtWidgets.QLabel(title)
        title_label.setObjectName("pageTitle")
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(title_label)

        body = QtWidgets.QLabel(description)
        body.setObjectName("placeholderLabel")
        body.setWordWrap(True)
        layout.addWidget(body, 1)

        return page

    def _apply_style(self, root: QtWidgets.QWidget):
        root.setStyleSheet(
            """
            QWidget#decoration_page { background: #f6f7fb; }
            #sidebar { background: #111827; color: #e5e7eb; }
            #navContainer QToolButton {
                border: none;
                color: #e5e7eb;
                padding: 10px 12px;
                border-radius: 10px;
                text-align: left;
            }
            #toggleButton {
                border: 1px solid rgba(255, 255, 255, 0.16);
                background: transparent;
                border-radius: 10px;
                padding: 8px;
            }
            #toggleButton:hover {
                background: rgba(255, 255, 255, 0.08);
                border-color: rgba(255, 255, 255, 0.24);
            }
            #toggleButton:checked {
                transform: rotate(180deg);
            }
            #navContainer QToolButton:checked {
                background: #2563eb;
            }
            #navContainer QToolButton:hover {
                background: #1f2937;
            }
            #subStepFrame QToolButton,
            #subStepFrame QLabel,
            #stepStack QToolButton {
                border: none;
                color: #1f2937;
                padding: 10px 12px;
                border-radius: 10px;
                background: #e5e7eb;
            }
            #stepRail {
                background: #fff;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 8px;
            }
            #subStepFrame QToolButton:checked,
            #stepStack QToolButton:checked {
                background: #2563eb;
                color: #ffffff;
            }
            #contentContainer { background: #f6f7fb; }
            #headerBar { background: #ffffff; border-radius: 12px; padding: 12px 16px; }
            #titleLabel { font-size: 22px; font-weight: 700; color: #111827; }
            #prototypeTag {
                background: #dbeafe;
                color: #1e3a8a;
                border-radius: 10px;
                padding: 6px 10px;
                font-weight: 700;
            }
            #contentHeader, #pageTitle { font-size: 18px; font-weight: 600; color: #1f2937; }
            #hintLabel { color: #4b5563; }
            #contentGroup { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; }
            #contentGroup > QWidget { border: none; }
            #placeholderLabel { color: #6b7280; padding: 12px; }
            #mainStack, #stepStack { border: none; }
            #logPanel {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }
            #logView {
                background: #0f172a;
                color: #d1d5db;
                font-family: "JetBrains Mono", "Consolas", monospace;
                border-radius: 8px;
                min-height: 160px;
            }
            """
        )

    def set_prototype_name(self, name: str):
        display_name = name or "样机未选择"
        self.prototype_tag.setText(display_name)


__all__ = ["Ui_decoration_page", "CommonContentWidget", "NavigationButton"]
