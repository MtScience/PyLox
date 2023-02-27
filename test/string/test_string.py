import pytest as pt


class TestString:
    def test_literals(self, capsys, lox):
        lox.run_file("string/literals.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["()", "a string", "A~¶Þॐஃ"]) + "\n"

    def test_multiline(self, capsys, lox):
        lox.run_file("string/multiline.lox")
        capture = capsys.readouterr().out
        assert capture == "1\n2\n3\n"

    def test_unterminated(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("string/unterminated.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == "[line 2] Error: Unterminated string.\n"

    def test_error_after_multiline(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("string/error_after_multiline.lox")
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == "Error: Undefined variable 'err'.\n[line 4]\n"