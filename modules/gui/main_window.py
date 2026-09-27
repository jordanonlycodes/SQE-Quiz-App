import logging

from PySide6.QtWidgets import QMainWindow, QWidget, QFrame, QMessageBox, QStackedLayout
from PySide6.QtCore import Slot

from .widgets import WelcomeLabel, StartDisplay, QuestionDisplay, QuestionParams, LoadingOverlay, ErrorOverlay
from .menu_bar import MenuBar, MenuActions
from .workers import QuestionLoader, WorkerThreadController
from ..questions import Questions

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window and top-level GUI coordinator.

    MainWindow owns the central stacked layout, menu bar, loading/error overlays,
    and the question-loading worker controller. It coordinates navigation between
    the welcome screen, start screen, and question display.

    Question loading is delegated to a worker thread. The OpenTDB request timeout
    is configured in OpenTriviaClient.
    """

    def __init__(self) -> None:
        super().__init__()
        self._ignored: list[QWidget] = []
        self._close_requested = False
        self._question_loader: QuestionLoader | None = None
        self._thread_controller: WorkerThreadController | None = None
        self._start_display: StartDisplay | None = None
        self._question_display: QuestionDisplay | None = None
        self._menu_bar: MenuBar | None = None
        self._error_overlay: ErrorOverlay | None = None
        self._loading_overlay: LoadingOverlay | None = None
        self._setup_window()
        self._setup_layout()
        self._setup_menu_bar()
        self._setup_error_overlay()
        self._setup_loading_overlay()
        self._setup_initial_widget()

    def _setup_window(self) -> None:
        self.setObjectName("mainWindow")
        self.setWindowTitle('Quiz')
        self.resize(896, 512)

    def _setup_layout(self) -> None:
        self._main_layout = QStackedLayout()
        self._main_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        self._central_widget = QWidget()
        self._central_widget.setLayout(self._main_layout)
        self.setCentralWidget(self._central_widget)
    
    def _setup_menu_bar(self) -> None:
        self._menu_bar = MenuBar()
        # Connects Signals from MenuBar to _handle method
        self._menu_bar.action_requested.connect(self._handle_menu_actions)
        self.setMenuBar(self._menu_bar)

    def _setup_error_overlay(self):
        self._error_overlay = ErrorOverlay()
        self._add_overlay(self._error_overlay)

    def _setup_loading_overlay(self):
        self._loading_overlay = LoadingOverlay()
        self._add_overlay(self._loading_overlay)

    def _setup_initial_widget(self):
        self._display_widget(WelcomeLabel())

    @Slot(object)
    def _handle_menu_actions(self, action: MenuActions) -> None:
        match action:
            case MenuActions.SHOW_START_DISPLAY:
                self._start_display_requested()
            case MenuActions.EXIT_APP:
                self.close()
            case MenuActions.ABOUT_APP:
                QMessageBox.about(self, 'About app', '''Simple quiz app built with PySide6.''')

    @Slot()
    def _start_display_requested(self) -> None:
        logger.debug("Displaying start display.")
        self._start_display = StartDisplay()
        # Connect start_quiz_requested signal to _load_questions method
        self._start_display.start_quiz_requested.connect(self._load_questions)
        self._display_widget(self._start_display)

    @Slot(object)
    def _on_error(self, error: Exception) -> None:
        if self._close_requested:
            logger.debug("Ignoring error callback because close was requested.")
            return # Do nothing if _close_requested

        logger.warning("Displaying loading error: %s: %s", type(error).__name__, error)
        self._start_display.start_error_returned.emit(error)
        self._error_overlay.show_error(error, for_seconds=5)

    @Slot(dict)
    def _load_questions(self, question_params: QuestionParams) -> None:
        """Start a background worker that loads quiz questions. Use WorkerThreadController."""
        logger.info("Question loading requested with params: %s", question_params)
        try:
            self._question_loader = QuestionLoader(question_params)
            self._thread_controller = WorkerThreadController(self._question_loader)

            self._connect_question_loading_signals()
            self._thread_controller.setup()
            self._thread_controller.run_thread()
        except Exception:
            logger.exception("Failed to start question loading.")
            self._on_error(RuntimeError("Unexpected application error. Please try again."))

    def _connect_question_loading_signals(self):
        """Connects signals for question loader and thread controller."""
        if self._question_loader is None or self._thread_controller is None:
            raise RuntimeError("Question loading objects are not initialized.")

        # Connect question loader signals
        self._question_loader.error.connect(self._on_error)
        self._question_loader.loaded.connect(self._on_questions_loaded)

        # Connect thread controller signals
        self._thread_controller.thread_error.connect(self._on_error)
        self._thread_controller.thread_started.connect(self._show_loading_screen)
        self._thread_controller.thread_finished.connect(self._hide_loading_screen)
        self._thread_controller.thread_finished.connect(self._on_thread_finished)

    @Slot()
    def _show_loading_screen(self) -> None:
        """Display loading screen overlay. Disable menu_bar control."""
        self._menu_bar.setEnabled(False)
        self._loading_overlay.show_loading()

    @Slot()
    def _hide_loading_screen(self) -> None:
        """Hide loading screen overlay. Enable menu_bar control."""
        self._menu_bar.setEnabled(True)
        self._loading_overlay.hide_loading()

    @Slot()
    def _on_thread_finished(self):
        """
        Remove reference from thread_controller and question_loader. 
        Close app if _close_requested.
        """
        logger.debug("Question loading thread finished. close_requested=%s", self._close_requested)
        self._question_loader = None
        self._thread_controller = None

        if self._close_requested:
            self.close()

    @Slot(Questions)
    def _on_questions_loaded(self, questions: Questions) -> None:
        """Display questions in QuestionDisplay."""
        if self._close_requested:
            logger.debug("Ignoring loaded questions callback because close was requested.")
            return # Do nothing if _close_requested
        
        self._question_display = QuestionDisplay(questions.questions_list)
        self._question_display.repeat_button_clicked.connect(self._start_display_requested)
        self._display_widget(self._question_display)
        logger.debug("Questions loaded successfully. Number of questions: %s", len(questions.questions_list))

    def _add_overlay(self, overlay: ErrorOverlay | LoadingOverlay) -> None:
        """
        Method used to add overlay widgets. Automatically hide overlay.
        Widgets added by this method are ignored by MainWindow cleanup methods.
        """
        self._ignored.append(overlay)
        overlay.hide()
        self._main_layout.addWidget(overlay)

    def _hide_overlays(self) -> None:
        """
        Used when displaying new widgets. Due to QStackedLayout.StackingMode.StackAll
        some, previously hidden, widgets may be visible again.
        """
        for overlay in self._ignored:
            if isinstance(overlay, LoadingOverlay):
                overlay.hide_loading()
            else:
                overlay.hide()

    def _display_widget(self, widget: QWidget | QFrame) -> None:
        """Display external Widget in MainWindow."""
        self._clear_window()
        self._main_layout.addWidget(widget)
        self._main_layout.setCurrentWidget(widget)
        self._hide_overlays()

    def _clear_window(self) -> None:
        """Delete all widgets from MainWindow."""
        deleted_widgets = 0
        widget_count = self._main_layout.count()
        if widget_count:
            for i in reversed(range(widget_count)):
                item = self._main_layout.itemAt(i)
                widget = item.widget() if item is not None else None
                if widget is not None and widget not in self._ignored:
                    self._main_layout.removeWidget(widget)
                    widget.deleteLater()
                    deleted_widgets +=1
        logger.debug("Deleted widget count: %s", deleted_widgets)

    def closeEvent(self, event):
        """
        Replaces MainWindow closeEvent. Function set _close_requested flag True.

        Delay closing while the question loader thread is still running.

        The first close request asks the thread to stop and ignores the event.
        When the thread emits finished, _on_thread_finished calls close() again.
        The second close request is accepted because the thread is no longer running.
        """
        if self._thread_controller is not None and self._thread_controller.is_running:
            logger.info("Close requested while question loader is running. Waiting for thread cleanup.")
            self._close_requested = True
            self._thread_controller.stop()
            # Cancel close event, it is required due to thread cleanup
            event.ignore() 
            return
        logger.debug("Close accepted. No running question loader thread.")
        super().closeEvent(event) # Use closeEvent from QMainWindow to close event=MainWindow
