import pytest as pt


class TestPrint:
    def test_missing_arg(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("print/missing_argument.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == "[line 2] Error at ';': Expect expression.\n"
