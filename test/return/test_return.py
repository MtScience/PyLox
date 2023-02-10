import pytest as pt

control_flow_paths = ["return/after_if.lox", "return/after_else.lox", "return/after_while.lox"]
control_flow_ids = ["if", "else", "while"]

function_paths = ["return/in_function.lox", "return/in_method.lox"]
function_ids = ["function", "method"]


class TestReturn:
    @pt.mark.parametrize("path", control_flow_paths, ids=control_flow_ids)
    def test_control_flow(self, capsys, lox, path):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == "ok\n"

    @pt.mark.parametrize("path", function_paths, ids=function_ids)
    def test_in_functions(self, capsys, lox, path):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == "ok\n"

    def test_default_value(self, capsys, lox):
        lox.run_file("return/return_nil_if_no_value.lox")
        capture = capsys.readouterr().out
        assert capture == "nil\n"

    def test_top_level(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("return/at_top_level.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == "[line 1] Error at 'return': Can't return from top-level code.\n"
