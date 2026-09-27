import logging
import html
import random

from .opentdb_client import (
    OpenTriviaAPIQuestionFormat,
    OpenTriviaAPIResponseFormat,
    OpenTriviaClient,
)

logger = logging.getLogger(__name__)


class Question:
    """Data object for one quiz question and its scoring data."""
    
    def __init__(
            self, tp: str,
            difficulty: str,
            category: str,
            question: str,
            correct_answer: str,
            incorrect_answers: list[str],
            all_answers: list[str],
            points: int,
            ) -> None:
        self.tp = tp
        self.difficulty = difficulty
        self.category = category
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers
        self.points = points
        self.all_answers = all_answers


class Questions:
    """
    Store quiz loading parameters and loaded Question objects.

    Creating an instance only stores the selected quiz parameters.
    Call load() to fetch question data from OpenTDB through OpenTriviaClient
    and convert the response into Question objects stored in questions_list.

    Raises:
        OpenTriviaClientError: If load() fails because the API request fails
            or the response cannot be converted into valid quiz questions.
    """

    def __init__(
            self,
            amount: str | int = 1,
            category: str = '',
            difficulty: str = '',
            question_type: str = '',
            ) -> None:
        """
        Initialize quiz question parameters.

        Args:
            amount: Number of questions requested from OpenTDB.

            category: OpenTDB category id, or an empty string for any category.

            difficulty: OpenTDB difficulty value, or an empty string for any difficulty.

            question_type: OpenTDB question type, or an empty string for any type.
        """
        self.questions_list: list[Question] = []
        self._amount = amount
        self._category = category
        self._difficulty = difficulty
        self._question_type = question_type

    def _get_question_data_from_api_client(self) -> OpenTriviaAPIResponseFormat:
        api_client = OpenTriviaClient()
        questions_data = api_client.get_questions_data(
            self._amount,
            self._category,
            self._difficulty,
            self._question_type,
            )
        return questions_data

    def _questions_data_to_question_objects(
            self, questions_data: OpenTriviaAPIResponseFormat
            ) -> None:
        """Convert raw API question data into Question objects."""
        for question_params in questions_data["results"]:
            self.questions_list.append(self._build_question(question_params))

        logger.debug(
            "Converted %s questions into Question objects.",
            len(self.questions_list),
            )

    def _build_question(self, question_params: OpenTriviaAPIQuestionFormat) -> Question:
        """Convert one raw API question into a Question object."""
        question_type = question_params["type"]
        difficulty = question_params["difficulty"]
        category = html.unescape(question_params["category"])
        question = html.unescape(question_params["question"])
        correct_answer = html.unescape(question_params["correct_answer"])
        incorrect_answers = [
            html.unescape(answer)
            for answer in question_params["incorrect_answers"]
            ]

        return Question(
            question_type,
            difficulty,
            category,
            question,
            correct_answer,
            incorrect_answers,
            self._build_answers(question_type, correct_answer, incorrect_answers),
            self._get_points(difficulty),
            )

    @staticmethod
    def _build_answers(
            question_type: str,
            correct_answer: str,
            incorrect_answers: list[str],
            ) -> list[str]:
        """Build and randomize the answer choices for a question."""
        if question_type == "boolean":
            return ["True", "False"]
        if question_type == "multiple":
            all_answers = incorrect_answers.copy()
            all_answers.append(correct_answer)
            random.shuffle(all_answers)
            return all_answers
        return []

    @staticmethod
    def _get_points(difficulty: str) -> int:
        """Return the score value associated with a question difficulty."""
        points_by_difficulty = {"hard": 3, "medium": 2, "easy": 1}
        return points_by_difficulty.get(difficulty, 0)

    def load(self) -> None:
        """Fetch question data, build Question objects and store them into questions_list."""
        logger.info("Questions load initialized.")
        questions_data = self._get_question_data_from_api_client()
        self._questions_data_to_question_objects(questions_data)
