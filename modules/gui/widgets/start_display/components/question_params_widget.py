from typing import TypedDict

from enum import StrEnum

from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QFrame
from PySide6.QtCore import Qt, Slot


from .....questions import QUESTION_AMOUNT, CATEGORIES, DIFFICULTIES, QUESTION_TYPES

class QuestionParams(TypedDict):
    amount: str
    difficulty: str
    category: str
    question_type: str


class QuestionParamsField(StrEnum):
    """Quiz parameter fields that can be reset and marked as invalid."""

    AMOUNT = "amount"
    DIFFICULTY = "difficulty"
    CATEGORY = "category"
    QUESTION_TYPE = "question_type"


class ParamFrame(QFrame):
    """Frame that groups a parameter label with its combo box."""
    def __init__(self, label_text: str) -> None:
        super().__init__()
        self._label_text = label_text
        self.setObjectName("paramFrame")
        self.setProperty("paramState", None)
        self._setup_layout()
        self._add_label()

    def _setup_layout(self) -> None:
        self._main_layout = QVBoxLayout()
        self._main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._main_layout)

    def _add_label(self) -> None:
        param_label = QLabel(self._label_text)
        self._main_layout.addWidget(
            param_label,
            alignment=Qt.AlignmentFlag.AlignBottom,
            )

    def add_combobox(self, combobox: QComboBox) -> None:
        self._main_layout.addWidget(
            combobox,
            alignment=Qt.AlignmentFlag.AlignTop,
            )


class QuestionParamsWidget(QWidget):
    """Widget for selecting OpenTDB quiz parameters."""

    def __init__(self) -> None:
        super().__init__()
        self._frame_list: list[ParamFrame] = []
        self._setup_layout()
        self._setup_question_params_comboboxes()
        self._add_question_param_frames()

    def _setup_layout(self) -> None:
        self._main_layout = QHBoxLayout()
        self._main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._main_layout)

    def _setup_question_params_comboboxes(self) -> None:
        # Gen question amount combobox data based on QUESTION_AMOUNT in API params
        # Did not used addItems with a list, in order to achive consecutive use of 
        # currentData for all comboboxes, to simplify tests and readability
        self._amount_cb = QComboBox()
        for amount, amount_id in {str(i): str(i) for i in range(1, QUESTION_AMOUNT + 1)}.items():
            self._amount_cb.addItem(amount, amount_id)

        # Add values to comboboxes from static variables in API params
        self._category_cb = QComboBox()
        for category, category_id in CATEGORIES.items():
            self._category_cb.addItem(category, category_id)

        self._difficulty_cb = QComboBox()
        for difficulty, difficulty_id in DIFFICULTIES.items():
            self._difficulty_cb.addItem(difficulty, difficulty_id)

        self._type_cb = QComboBox()
        for question_type, question_type_id in QUESTION_TYPES.items():
            self._type_cb.addItem(question_type, question_type_id)

    def _add_question_param_frames(self) -> None:
        """Create and add the four quiz parameter frames."""
        self._amount_frame = self._add_parameter_frame("Amount", self._amount_cb)
        self._difficulty_frame = self._add_parameter_frame(
            "Difficulty", self._difficulty_cb
            )
        self._category_frame = self._add_parameter_frame("Category", self._category_cb)
        self._type_frame = self._add_parameter_frame("Type", self._type_cb)

    def _add_parameter_frame(
            self, label: str, combobox: QComboBox
            ) -> ParamFrame:
        """Create one parameter frame and add it to the layout."""
        frame = ParamFrame(label)
        self._frame_list.append(frame)
        frame.add_combobox(combobox)
        self._main_layout.addWidget(frame)
        return frame

    def get_params(self) -> QuestionParams:
        """Return selected question params in comboboxes."""
        self._reset_error_frames() # Reset frame colors before another load attempt.
        params: QuestionParams = {
            "amount": str(self._amount_cb.currentData()),
            "difficulty": str(self._difficulty_cb.currentData()),
            "category": str(self._category_cb.currentData()),
            "question_type": str(self._type_cb.currentData()),
        }
        return params

    @Slot()
    def on_error_reset_combobox_to_default_values(
        self, *fields: QuestionParamsField
        ) -> None:
        """
        Reset selected combo boxes to default values.

        If no fields are provided, reset all fields. Mark reset fields as invalid
        to show which parameters caused the loading error.
        """
        fields_to_reset = list(fields) if fields else list(QuestionParamsField)

        for field in fields_to_reset:
            match field:
                case QuestionParamsField.AMOUNT:
                    self._amount_cb.setCurrentIndex(0)
                    self._color_error_param_frame(self._amount_frame)
                case QuestionParamsField.DIFFICULTY:
                    self._difficulty_cb.setCurrentIndex(0)
                    self._color_error_param_frame(self._difficulty_frame)
                case QuestionParamsField.CATEGORY:
                    self._category_cb.setCurrentIndex(0)
                    self._color_error_param_frame(self._category_frame)
                case QuestionParamsField.QUESTION_TYPE:
                    self._type_cb.setCurrentIndex(0)
                    self._color_error_param_frame(self._type_frame)

    def _color_error_param_frame(self, frame: QFrame) -> None:
        """Mark a parameter frame as invalid."""
        frame.setProperty("paramState", "error")
        frame.style().unpolish(frame)
        frame.style().polish(frame)
        frame.update()

    def _reset_error_frames(self) -> None:
        for frame in self._frame_list:
            frame.setProperty("paramState", None)
            frame.style().unpolish(frame)
            frame.style().polish(frame)
            frame.update()
