import pytest as pt

definition_settings = [("for/class_in_body.lox", "class"), ("for/fun_in_body.lox", "fun")]
definition_ids = ["class", "function"]

return_paths = ["for/return_closure.lox", "for/return_inside.lox"]
return_ids = ["closure", "inside"]

stmt_settings = [("for/statement_condition.lox",
                  "[line 3] Error at '{': Expect expression.\n[line 3] Error at ')': Expect ';' after expression.\n"),
                 ("for/statement_initializer.lox",
                  "[line 3] Error at '{': Expect expression.\n[line 3] Error at ')': Expect ';' after expression.\n"),
                 ("for/statement_increment.lox",
                  "[line 2] Error at '{': Expect expression.\n")]
stmt_ids = ["condition", "initializer", "increment"]


class TestFor:
    @pt.mark.parametrize("path,typ", definition_settings, ids=definition_ids)
    def test_definition_in_body(self, capsys, lox, path, typ):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == f"[line 2] Error at '{typ}': Expect expression.\n"

    def test_closure_in_body(self, capsys, lox):
        lox.run_file("for/closure_in_body.lox")

        expected_val = "\n".join([str(i) for i in (4, 1, 4, 2, 4, 3)]) + "\n"

        capture = capsys.readouterr().out
        assert capture == expected_val

    @pt.mark.parametrize("path", return_paths, ids=return_ids)
    def test_return(self, capsys, lox, path):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == "i\n"

    def test_scope(self, capsys, lox):
        lox.run_file("for/scope.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["0", "-1", "after", "0"]) + "\n"

    @pt.mark.parametrize("path,expected_val", stmt_settings, ids=stmt_ids)
    def test_statement(self, capsys, lox, path, expected_val):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == expected_val

    def test_syntax(self, capsys, lox):
        lox.run_file("for/syntax.lox")

        expected_val = [1, 2, 3, 0, 1, 2, "done", 0, 1, 0, 1, 2, 0, 1]
        expected_val = "\n".join([str(i) for i in expected_val]) + "\n"

        capture = capsys.readouterr().out
        assert capture == expected_val

    def test_variable_in_body(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("for/var_in_body.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == "[line 2] Error at 'var': Expect expression.\n"
