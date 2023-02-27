import pytest as pt

ids = ["bool", "num", "nil", "string", "object"]
settings = [("call/bool.lox", 1),
            ("call/num.lox", 1),
            ("call/nil.lox", 1),
            ("call/string.lox", 1),
            ("call/object.lox", 4)]


class TestCall:
    @pt.mark.parametrize("path,line", settings, ids=ids)
    def test_call(self, capsys, lox, path, line):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == f"Error: Can only call functions and classes.\n[line {line}]\n"
