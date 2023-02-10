import pytest as pt

closure_paths = ["this/closure.lox", "this/nested_closure.lox"]
top_level_settings = [("this/this_at_top_level.lox", 1), ("this/this_in_top_level_function.lox", 2)]


class TestThis:
    @pt.mark.parametrize("path", closure_paths, ids=["normal", "nested"])
    def test_closure(self, capsys, lox, path):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == "Foo\n"

    @pt.mark.parametrize("path,line", top_level_settings, ids=["script", "function"])
    def test_top_level(self, capsys, lox, path, line):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == f"[line {line}] Error at 'this': Can't use 'this' outside of a class.\n"

    def test_nested_class(self, capsys, lox):
        lox.run_file("this/nested_class.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["<Outer instance>", "<Outer instance>", "<Inner instance>"]) + "\n"

    def test_method(self, capsys, lox):
        lox.run_file("this/this_in_method.lox")
        capture = capsys.readouterr().out
        assert capture == "baz\n"
