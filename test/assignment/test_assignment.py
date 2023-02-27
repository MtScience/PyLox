import pytest as pt


class TestAssignment:
    def test_associativity(self, capsys, lox):
        lox.run_file("assignment/associativity.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["c"] * 3) + "\n"

    def test_global(self, capsys, lox):
        lox.run_file("assignment/global.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["before", "after", "arg", "arg"]) + "\n"

    def test_grouping(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("assignment/grouping.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == "[line 2] Error at '=': Invalid assignment target.\n"

    def test_infix_operator(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("assignment/infix_operator.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == "[line 3] Error at '=': Invalid assignment target.\n"

    def test_local(self, capsys, lox):
        lox.run_file("assignment/local.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["before", "after", "arg", "arg"]) + "\n"

    def test_prefix_operator(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("assignment/prefix_operator.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == "[line 2] Error at '=': Invalid assignment target.\n"

    def test_syntax(self, capsys, lox):
        lox.run_file("assignment/syntax.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["var", "var"]) + "\n"

    def test_to_this(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("assignment/to_this.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == "[line 3] Error at '=': Invalid assignment target.\n"

    def test_undefined(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("assignment/undefined.lox")
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == "Error: Undefined variable 'unknown'.\n[line 1]\n"
