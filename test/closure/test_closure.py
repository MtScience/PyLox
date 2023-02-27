import pytest as pt

close_over_param_paths = ["closure/close_over_function_parameter.lox", "closure/close_over_method_parameter.lox"]
closure_in_func_paths = ["closure/closed_closure_in_function.lox", "closure/open_closure_in_function.lox"]


class TestClosure:
    def test_assign_to_closure(self, capsys, lox):
        lox.run_file("closure/assign_to_closure.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["local", "after f", "after f", "after g"]) + "\n"

    def test_assign_to_shadowed(self, capsys, lox):
        lox.run_file("closure/assign_to_shadowed_later.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["inner", "assigned"]) + "\n"

    @pt.mark.parametrize("path", close_over_param_paths, ids=["function", "method"])
    def test_close_over_param(self, capsys, lox, path):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == "param\n"

    def test_close_over_later_variable(self, capsys, lox):
        lox.run_file("closure/close_over_later_variable.lox")
        capture = capsys.readouterr().out
        assert capture == "b\na\n"

    @pt.mark.parametrize("path", closure_in_func_paths, ids=["closed", "open"])
    def test_in_function(self, capsys, lox, path):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == "local\n"

    def test_nested(self, capsys, lox):
        lox.run_file("closure/nested_closure.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["a", "b", "c"]) + "\n"

    def test_multiple_ref(self, capsys, lox):
        lox.run_file("closure/reference_closure_multiple_times.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["a", "a"]) + "\n"

    def test_reuse_slot(self, capsys, lox):
        lox.run_file("closure/reuse_closure_slot.lox")
        capture = capsys.readouterr().out
        assert capture == "a\n"

    def test_shadow_with_local(self, capsys, lox):
        lox.run_file("closure/shadow_closure_with_local.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["closure", "shadow", "closure"]) + "\n"

    def test_unused(self, capsys, lox):
        lox.run_file("closure/unused_closure.lox")
        capture = capsys.readouterr().out
        assert capture == "ok\n"

    def test_unused_later(self, capsys, lox):
        lox.run_file("closure/unused_later_closure.lox")
        capture = capsys.readouterr().out
        assert capture == "a\n"
