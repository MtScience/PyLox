import pytest as pt

ids = ["global", "local"]
reference_paths = ["class/reference_self.lox", "class/local_reference_self.lox"]
inherit_settings = [("class/inherit_self.lox", 1), ("class/local_inherit_self.lox", 2)]


class TestClass:
    def test_empty(self, capsys, lox):
        lox.run_file("class/empty.lox")
        capture = capsys.readouterr().out
        assert capture == "<class Foo>\n"

    def test_inherited_method(self, capsys, lox):
        lox.run_file("class/inherited_method.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["in foo", "in bar", "in baz"]) + "\n"

    @pt.mark.parametrize("path,line", inherit_settings, ids=ids)
    def test_inherit_self(self, capsys, lox, path, line):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == f"[line {line}] Error at 'Foo': A class can't inherit from itself.\n"

    @pt.mark.parametrize("path", reference_paths, ids=ids)
    def test_reference_self(self, capsys, lox, path):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == "<class Foo>\n"

    def test_local_inherit_other(self, capsys, lox):
        lox.run_file("class/local_inherit_other.lox")
        capture = capsys.readouterr().out
        assert capture == "<class B>\n"
