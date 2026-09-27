from typing import ClassVar, TypedDict

import logging
import requests

logger = logging.getLogger(__name__)


class OpenTriviaClientError(Exception):
    """Raised when fetching questions from OpenTDB fails."""


class NoQuestionsFoundError(OpenTriviaClientError):
    """Raised when OpenTDB returns no questions for the selected parameters."""


class NotEnoughQuestionsError(OpenTriviaClientError):
    """Raised when OpenTDB returns fewer questions than requested."""


class OpenTriviaAPIQuestionFormat(TypedDict):
    type: str
    difficulty: str
    category: str
    question: str
    correct_answer: str
    incorrect_answers: list[str]


class OpenTriviaAPIResponseFormat(TypedDict):
    response_code: int
    results: list[OpenTriviaAPIQuestionFormat]


class OpenTriviaClient:
    """HTTP client for fetching quiz questions from the OpenTDB API."""

    BASE_URL: ClassVar[str] = 'https://opentdb.com/api.php'

    def get_questions_data(
            self,
            amount: int | str = 1,
            category: str = '',
            difficulty: str = '',
            question_type: str = '',
            ) -> OpenTriviaAPIResponseFormat:
        """
        Request quiz question data from the OpenTDB API.

        Args:
            amount: Number of questions to request.
            category: Optional OpenTDB category id.
            difficulty: Optional difficulty value.
            question_type: Optional OpenTDB question type.

        Returns:
            Parsed OpenTDB response containing response_code and results.

        Raises:
            NoQuestionsFoundError: If OpenTDB returns an empty results list.
            NotEnoughQuestionsError: If OpenTDB returns fewer questions than requested.
            OpenTriviaClientError: If the request fails, times out, or returns 
            invalid/unexpected data.
        """
        params = {
            'amount' : amount
        }
        if category:
            params['category'] = category
        if difficulty:
            params['difficulty'] = difficulty
        if question_type:
            params['type'] = question_type

        logger.debug("Fetching questions from OpenTDB with params: %s", params)

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=3)
            logger.debug("OpenTDB response status: %s", response.status_code)
            response.raise_for_status()
            data = response.json()
            if not data['results']:
                raise NoQuestionsFoundError('No questions found for selected parameters. Try different category, difficulty or type.')
            if int(amount) > len(data['results']):
                raise NotEnoughQuestionsError('Not enough questions found for the selected parameters. Try lower number.')
            logger.debug(
                "OpenTDB response parsed: response_code=%s, results=%s",
                data.get("response_code"),
                len(data.get("results", [])),
                )
            return data
   
        except requests.exceptions.Timeout as error:
            raise OpenTriviaClientError('Request to OpenTDB timed out.') from error

        except requests.exceptions.ConnectionError as error:
            raise OpenTriviaClientError('Could not connect to OpenTDB.') from error

        except requests.exceptions.HTTPError as error:
            raise OpenTriviaClientError('OpenTDB returned HTTP error.') from error

        except ValueError as error:
            raise OpenTriviaClientError('OpenTDB returned invalid JSON.') from error

        except (KeyError, TypeError) as error:
            raise OpenTriviaClientError('OpenTDB returned unexpected format.') from error
        
        except OpenTriviaClientError:
            raise

        except Exception as error:
            raise OpenTriviaClientError('Unexpected error occurred.') from error
        