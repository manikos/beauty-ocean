from unittest import mock

from yaspin.spinners import Spinners
from inquirer import Text, List, Checkbox, Password, Confirm

from beauty_ocean.core import config


def test_config_constants():
    assert config.DEFAULT_ENV_NAME == "DO_TOKEN"
    assert config.DEFAULT_QUESTION_NAME == "choice"
    assert config.SORRY == "¯\_(ツ)_/¯"
    assert type(config.TEXT_BASE_COLOR) is str
    assert config.CYAN_COLOR == "cyan"


def test_do_prompt():
    assert callable(config.do_prompt.func)
    assert type(config.do_prompt.keywords["theme"]) is config.DropletTheme


def test_question_kind():
    assert type(config.question()) is list
    assert len(config.question(kind=Text)) == 1
    assert type(config.question(kind=Text)[0]) is Text
    assert type(config.question(kind=List)[0]) is List
    assert type(config.question(kind=Checkbox)[0]) is Checkbox
    assert type(config.question(kind=Password)[0]) is Password
    assert type(config.question(kind=Confirm)[0]) is Confirm


@mock.patch('beauty_ocean.core.config.stylize')
def test_question_message_color(m_stylize):
    config.question()
    m_stylize.assert_called_once_with("", config.TEXT_BASE_COLOR)


def test_question_message_string():
    q = config.question()[0]
    assert type(q.message) is str

    q = config.question(message="Hello")[0]
    assert "Hello" in q.message

    q = config.question(message="Hello ", kind=Checkbox)[0]
    m = f"Hello (Up/Down: move, Space: (de)select, Enter: submit)"
    assert m in q.message


def test_question_choices_default():
    choices = [1, 2, 3]

    q = config.question(choices=choices)[0]
    assert q.choices == choices
    assert q.default == 1

    q = config.question(choices=choices, default=3)[0]
    assert q.default == 3


def test_q_partials():
    assert config.q_radio.keywords["kind"] is List
    assert config.q_radio.keywords["carousel"] is True
    assert config.q_multiple.keywords["kind"] is Checkbox
    assert config.q_confirm.keywords["kind"] is Confirm
    assert config.q_pwd.keywords["kind"] is Password
    assert config.pong.keywords["spinner"] is Spinners.pong
    assert config.pong.keywords["color"] == config.CYAN_COLOR
    assert config.pong.keywords["attrs"] == ["bold"]
    assert type(config.cyan_text.keywords["styles"]) is str
    assert type(config.green_text.keywords["styles"]) is str
    assert type(config.p_text.keywords["styles"]) is str


@mock.patch("beauty_ocean.core.config.do_prompt")
def test_answer(m_do_prompt):
    q = config.question()
    config.answer(q)
    m_do_prompt.assert_called_once_with(q)

    m_do_prompt.reset_mock()
    f = mock.Mock()
    config.answer(q, func=f)
    f.assert_called()


def test_tag_answer():
    assert callable(config.tag_answer.keywords["func"])
