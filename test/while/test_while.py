import pytest as pt

definition_settings = [("while/class_in_body.lox", "class"),
                       ("while/fun_in_body.lox", "fun"),
                       ("while/var_in_body.lox", "var")]
definition_ids = ["class", "function", "variable"]

return_paths = ["while/return_inside.lox", "while/return_closure.lox"]
return_ids = ["inside", "closure"]


class TestWhile:
    def test_syntax(self, capsys, lox):
        lox.run_file("while/syntax.lox")

        expected_val = [str(i) for i in [1, 2, 3, 0, 1, 2]]
        expected_val = "\n".join(expected_val) + "\n"

        capture = capsys.readouterr().out
        assert capture == expected_val

    def test_closure_in_while(self, capsys, lox):
        lox.run_file("while/closure_in_body.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["1", "2", "3"]) + "\n"

    @pt.mark.parametrize("path", return_paths, ids=return_ids)
    def test_return(self, capsys, lox, path):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == "i\n"

    @pt.mark.parametrize("path,token", definition_settings, ids=definition_ids)
    def test_definition_in_body(self, capsys, lox, path, token):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == f"[line 2] Error at '{token}': Expect expression.\n"

