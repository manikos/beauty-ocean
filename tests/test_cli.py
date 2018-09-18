from unittest import mock

from click.testing import CliRunner

from beauty_ocean.cli import create_droplet_click


@mock.patch('beauty_ocean.cli.create_droplet')
def test_create_droplet_click(mock_create_droplet):
    runner = CliRunner()

    # Test with no arguments
    runner.invoke(create_droplet_click)
    mock_create_droplet.assert_called_once()
    mock_create_droplet.reset_mock()

    # Test with an argument
    runner.invoke(create_droplet_click, ['-t', 'ENV_VAR_TOKEN'])
    mock_create_droplet.assert_called_once_with(token='ENV_VAR_TOKEN')
    mock_create_droplet.reset_mock()

    # Test no echo
    res = runner.invoke(create_droplet_click)
    mock_create_droplet.return_value = None
    assert res.exit_code == 0
    mock_create_droplet.reset_mock()

    # Test help message
    help_result = runner.invoke(create_droplet_click, ['--help'])
    assert help_result.exit_code == 0
    assert '[env var name | path to file | token str]' in help_result.output
