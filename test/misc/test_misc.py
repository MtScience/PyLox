import pytest as pt


def test_empty(capsys, lox):
    lox.run_file("misc/empty_file.lox")
    capture = capsys.readouterr().out
    assert capture == ""


def test_unexpected(capsys, lox):
    with pt.raises(SystemExit) as exc:
        lox.run_file("misc/unexpected_character.lox")
        assert exc.value == 65

    capture = capsys.readouterr().err

    expected_val = ["[line 3] Error: Unexpected character.",
                    "[line 3] Error at 'b': Expect ')' after arguments."]

    assert capture == "\n".join(expected_val) + "\n"


def test_precedence(capsys, lox):
    lox.run_file("misc/precedence.lox")
    capture = capsys.readouterr().out

    expected_val = [14, 8, 4, 0] + [True] * 4 + [0] * 4 + [4]
    expected_val = [str(v).lower() for v in expected_val]

    assert capture == "\n".join(expected_val) + "\n"
