from typing import Union, Type, Callable
from functools import partial

from yaspin import yaspin
from yaspin.spinners import Spinners
from colored import fore, fg, stylize
from inquirer import List, Checkbox, Text, Confirm, Password, prompt
from inquirer.themes import GreenPassion, term


DEFAULT_ENV_NAME = "DO_TOKEN"
DEFAULT_QUESTION_NAME = "choice"
SORRY = "¯\_(ツ)_/¯"
TEXT_BASE_COLOR = fore.GREY_82
CYAN_COLOR = "cyan"
GREEN_COLOR = "green"
PRINT_COLOR = "medium_orchid_1a"


class DropletTheme(GreenPassion):
    def __init__(self):
        super().__init__()
        self.Question.mark_color = term.bold_white
        self.Question.brackets_color = term.bold_cyan
        self.Question.default_color = term.bold_white
        self.Checkbox.unselected_color = TEXT_BASE_COLOR
        self.Checkbox.selected_color = term.bold_cyan
        self.Checkbox.selection_color = term.italic_black_on_bright_cyan
        self.List.unselected_color = TEXT_BASE_COLOR
        self.List.selection_color = term.italic_black_on_bright_cyan


def question(
    name: str = DEFAULT_QUESTION_NAME,
    message: str = "",
    choices: list = None,
    default: Union[str, int, bool] = None,
    validate: Union[bool, Callable] = True,
    kind: Type[Union[List, Checkbox, Text, Confirm, Password]] = Text,
    **kwargs,
) -> list:
    """
    Given a kind of question, builds a question to be asked to the prompt.
    :param str name: the name for the question (does not change)
    :param str message: the actual question string
    :param list choices: a list of choices to select (applies to List/Checkbox)
    :param default: the default text/choice
    :param func validate: validation function on the provided answer
    :param kind: kind of question to ask
    :param kwargs: any extra kwargs to be passed to the inquirer constructor
    :return: 1-length list of <kind> question
    """
    if choices and not default:
        default = choices[0]
    if kind.kind == "checkbox" and message:
        message = f"{message.strip()} (Up/Down: move, Space: (de)select, " \
                  f"Enter: submit)"
    message = stylize(message, TEXT_BASE_COLOR)
    return [
        kind(
            name=name,
            message=message,
            choices=choices,
            default=default,
            validate=validate,
            **kwargs,
        )
    ]


# Partials
q_radio = partial(question, kind=List, carousel=True)
q_multiple = partial(question, kind=Checkbox)
q_confirm = partial(question, kind=Confirm)
q_pwd = partial(question, kind=Password)
do_prompt = partial(prompt, theme=DropletTheme())
pong = partial(yaspin, spinner=Spinners.pong, color=CYAN_COLOR, attrs=["bold"])
cyan_text = partial(stylize, styles=fg(CYAN_COLOR))
green_text = partial(stylize, styles=fg(GREEN_COLOR))
p_text = partial(stylize, styles=fg(PRINT_COLOR))


def answer(q: list, func: Callable = None):
    """
    Given an inquirer question list, build the prompt for the user to
    enter/select.
    :param list q: the inquirer question
    :param func func: func that'll be applied to the given answer before return
    :return: str/int/list/bool
    """
    ans = do_prompt(q).get(DEFAULT_QUESTION_NAME)
    # if q[0].kind == "checkbox":
    #     while not ans:
    #         ans = green_prompt(q).get(default_question_name)
    if func:
        return func(ans)
    return ans


tag_answer = partial(answer, func=lambda x: x.split(", "))
