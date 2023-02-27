import pytest as pt

dot_settings = [("number/leading_dot.lox", "[line 2] Error at '.': Expect expression.\n"),
                ("number/trailing_dot.lox", "[line 2] Error at ';': Expect property name after '.'.\n")]


class TestNumber:
    def test_literals(self, capsys, lox):
        lox.run_file("number/literals.lox")
        capture = capsys.readouterr().out

        expected_vals = [123, 987654, 0, "-0", 123.456, -0.001]
        expected_vals = [str(v) for v in expected_vals]

        assert capture == "\n".join(expected_vals) + "\n"

    def test_nan(self, capsys, lox):
        lox.run_file("number/nan_equality.lox")
        capture = capsys.readouterr().out

        expected_vals = [False, True] * 2
        expected_vals = [str(v).lower() for v in expected_vals]

        assert capture == "\n".join(expected_vals) + "\n"

    @pt.mark.parametrize("path,expected_val", dot_settings, ids=["leading", "trailing"])
    def test_dot(self, capsys, lox, path, expected_val):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == expected_val

    def test_dec_point_at_eof(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("number/decimal_point_at_eof.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == "[line 2] Error at end: Expect property name after '.'.\n"

