import pytest as pt

definition_ids = ["class else", "class if",
                  "function else", "function if",
                  "variable else", "variable if"]
definition_settings = [("if/class_in_else.lox", "class"), ("if/class_in_then.lox", "class"),
                       ("if/fun_in_else.lox", "fun"), ("if/fun_in_then.lox", "fun"),
                       ("if/var_in_else.lox", "var"), ("if/var_in_then.lox", "var")]

conditionals_ids = ["dangling else", "if", "else"]
conditionals_settings = [("if/dangling_else.lox", "good\n"),
                         ("if/if.lox", "\n".join(["good", "block", "true"]) + "\n"),
                         ("if/else.lox", "\n".join(["good", "good", "block"]) + "\n")]


class TestIf:
    @pt.mark.parametrize("path,stmt_type", definition_settings, ids=definition_ids)
    def test_definition_in_conditional(self, capsys, lox, path, stmt_type):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == f"[line 2] Error at '{stmt_type}': Expect expression.\n"

    @pt.mark.parametrize("path,expected_out", conditionals_settings, ids=conditionals_ids)
    def test_conditionals(self, capsys, lox, path, expected_out):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == expected_out

    def test_truth(self, capsys, lox):
        lox.run_file("if/truth.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["false", "nil", "true", "0", "empty"]) + "\n"

