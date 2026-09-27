from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QTimer

from ....questions import OpenTriviaClientError


class ErrorOverlay(QWidget):
    """
    Transparent overlay, that shows error label temporarily.
    Used for API and thread error displaying.
    """
    
    def __init__(self) -> None:
        super().__init__()
        self._setup_overlay()
        self._setup_layout()
        self._setup_label()
        self._setup_timer()

    def _setup_overlay(self) -> None:
        self.setObjectName("errorOverlay")
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

    def _setup_layout(self) -> None:
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)

    def _setup_label(self) -> None:
        self._error_label = QLabel(
            alignment=Qt.AlignmentFlag.AlignCenter,
            wordWrap=True,
            )
        self._error_label.setObjectName('errorOverlayLabel')
        self._error_label.hide()

        self._main_layout.addWidget(
            self._error_label,
            alignment=Qt.AlignmentFlag.AlignTop
            )

    def _setup_timer(self) -> None:
        self._timer = QTimer(singleShot=True)
        self._timer.timeout.connect(self._hide_error_overlay)

    def show_error(
            self,
            error: Exception,
            for_seconds: int
            ) -> None:
        """
        Display a temporary user-facing error message.

        Args:
            error: Exception whose message should be shown to the user.
            for_seconds: Number of seconds before the overlay is hidden.

        Notes:
            Generic OpenTriviaClientError messages get an additional retry hint.
        """
        label_text = str(error)
        if isinstance(error, OpenTriviaClientError):
            label_text += " Try again in a few seconds."
        self._error_label.setText(label_text)
        self._error_label.update()
        self.raise_()
        self.show()
        self._error_label.show()
        if self._timer.isActive():
            self._timer.stop()
        self._timer.start(int(for_seconds*1000))

    def _hide_error_overlay(self) -> None:
        self.hide()
        self._error_label.hide()
