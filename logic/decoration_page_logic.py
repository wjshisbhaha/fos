from PyQt6 import QtCore, QtWidgets

from ui.decoration_page import NavigationButton, Ui_decoration_page


class DecorationPage(QtWidgets.QWidget):
    """装调主页面，包含侧边栏、步骤导航和公共组件区域。"""

    def __init__(self, prototype_name: str = "", parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.ui = Ui_decoration_page()
        self.ui.setupUi(self)
        self.ui.set_prototype_name(prototype_name)

        self._active_nav = 0
        self._active_step = 0
        self._active_sub_step = 0

        self._connect_signals()
        self._set_initial_state()

    def _connect_signals(self):
        for idx, btn in enumerate(self.ui.nav_buttons):
            btn.clicked.connect(lambda _, i=idx: self._on_nav_selected(i))

        for idx, btn in enumerate(self.ui.step_buttons):
            btn.clicked.connect(lambda _, i=idx: self._on_step_selected(i))

        for idx, btn in enumerate(self.ui.sub_step_buttons):
            btn.clicked.connect(lambda _, i=idx: self._on_sub_step_selected(i))

        self.ui.toggle_btn.toggled.connect(self._toggle_sidebar)

    def _set_initial_state(self):
        self._activate_button(self.ui.nav_buttons[self._active_nav], self.ui.nav_buttons)
        self.ui.main_stack.setCurrentIndex(self._active_nav)
        self._activate_button(self.ui.step_buttons[self._active_step], self.ui.step_buttons)
        self.ui.step_stack.setCurrentIndex(self._active_step)
        self._update_sub_steps_visibility(show=False)
        self._update_title()

    def _on_nav_selected(self, idx: int):
        self._active_nav = idx
        self.ui.main_stack.setCurrentIndex(idx)
        self._activate_button(self.ui.nav_buttons[idx], self.ui.nav_buttons)
        if idx == 0:
            # 回到开始装调时保持当前步骤状态
            self._update_title()
        else:
            # 切换到其他主页面时重置标题
            self.ui.title_label.setText(self.ui.nav_buttons[idx].full_text)
        coax_index = self.ui.step_names.index("同轴度")
        self.ui.substep_frame.setVisible(idx == 0 and self._active_step == coax_index)

    def _on_step_selected(self, idx: int):
        self._active_step = idx
        self._activate_button(self.ui.step_buttons[idx], self.ui.step_buttons)
        self.ui.step_stack.setCurrentIndex(idx)
        coax_index = self.ui.step_names.index("同轴度")
        if idx == coax_index:
            self._update_sub_steps_visibility(show=True)
            self._on_sub_step_selected(self._active_sub_step)
        else:
            self._update_sub_steps_visibility(show=False)
        self._update_title()

    def _on_sub_step_selected(self, idx: int):
        self._active_sub_step = idx
        self._activate_button(self.ui.sub_step_buttons[idx], self.ui.sub_step_buttons)
        self.ui.sub_step_stack.setCurrentIndex(idx)
        self._update_title(suffix=f"- {self.ui.sub_step_names[idx]}")

    def _update_sub_steps_visibility(self, show: bool):
        self.ui.substep_frame.setVisible(show)
        if show:
            self._activate_button(self.ui.sub_step_buttons[self._active_sub_step], self.ui.sub_step_buttons)
        else:
            for btn in self.ui.sub_step_buttons:
                btn.setChecked(False)

    def _toggle_sidebar(self, collapsed: bool):
        target_width = 78 if collapsed else 260
        for btn in self.ui.nav_buttons:
            if isinstance(btn, NavigationButton):
                btn.set_collapsed(collapsed)
        animation = QtCore.QPropertyAnimation(self.ui.sidebar, b"maximumWidth")
        animation.setDuration(150)
        animation.setStartValue(self.ui.sidebar.width())
        animation.setEndValue(target_width)
        animation.start()
        self._sidebar_animation = animation  # Keep reference

    def _activate_button(self, active_btn: QtWidgets.QAbstractButton, all_buttons: list[QtWidgets.QAbstractButton]):
        for btn in all_buttons:
            btn.setChecked(btn is active_btn)

    def _update_title(self, suffix: str | None = None):
        if self._active_nav != 0:
            self.ui.title_label.setText(self.ui.nav_buttons[self._active_nav].full_text)
            return

        base_title = f"开始装调 - {self.ui.step_names[self._active_step]}"
        if suffix:
            base_title += f" {suffix}"
        self.ui.title_label.setText(base_title)


__all__ = ["DecorationPage"]
