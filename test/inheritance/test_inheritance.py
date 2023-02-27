import pytest as pt

inherit_from_settings = [("inheritance/inherit_from_function.lox", 3),
                         ("inheritance/inherit_from_nil.lox", 2),
                         ("inheritance/inherit_from_number.lox", 2)]
inherit_from_ids = ["function", "nil", "number"]


class TestInheritance:
    def test_constructor(self, capsys, lox):
        lox.run_file("inheritance/constructor.lox")
        capture = capsys.readouterr().out
        assert capture == "value\n"

    def test_inherit_methods(self, capsys, lox):
        lox.run_file("inheritance/inherit_methods.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["foo", "bar", "bar"]) + "\n"

    def test_fields_from_base_class(self, capsys, lox):
        lox.run_file("inheritance/set_fields_from_base_class.lox")

        expected_val = ["foo 1", "foo 2"] + ["bar 1", "bar 2"] * 2
        expected_val = "\n".join(expected_val) + "\n"

        capture = capsys.readouterr().out
        assert capture == expected_val

    @pt.mark.parametrize("path,line", inherit_from_settings, ids=inherit_from_ids)
    def test_inherit_from(self, capsys, lox, path, line):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == f"Error: Superclass must be a class.\n[line {line}]\n"

    def test_parenthesized_superclass(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("inheritance/parenthesized_superclass.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == "[line 4] Error at '(': Expect superclass name.\n"
