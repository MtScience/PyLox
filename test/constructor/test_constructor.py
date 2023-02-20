import pytest as pt

arguments_settings = [("constructor/default_arguments.lox", (0, 3, 3)),
                      ("constructor/extra_arguments.lox", (2, 4, 8)),
                      ("constructor/missing_arguments.lox", (2, 1, 5))]
arguments_ids = ["default", "extra", "missing"]


class TestConstructor:
    def test_arguments(self, capsys, lox):
        lox.run_file("constructor/arguments.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["init", "1", "2"]) + "\n"

    def test_early_return_from_init_call(self, capsys, lox):
        lox.run_file("constructor/call_init_early_return.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["init", "init", "<Foo instance>"]) + "\n"

    def test_explicit_init_call(self, capsys, lox):
        lox.run_file("constructor/call_init_explicitly.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["Foo.init(one)", "Foo.init(two)", "<Foo instance>", "init"]) + "\n"

    def test_default(self, capsys, lox):
        lox.run_file("constructor/default.lox")
        capture = capsys.readouterr().out
        assert capture == "<Foo instance>\n"

    def test_early_return(self, capsys, lox):
        lox.run_file("constructor/early_return.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["init", "<Foo instance>"]) + "\n"

    def test_init_not_method(self, capsys, lox):
        lox.run_file("constructor/init_not_method.lox")
        capture = capsys.readouterr().out
        assert capture == "not initializer\n"

    def test_return_in_nested_function(self, capsys, lox):
        lox.run_file("constructor/return_in_nested_function.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["bar", "<Foo instance>"]) + "\n"

    def test_return_value(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("constructor/return_value.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == "[line 3] Error at 'return': Can't return a value from an initializer.\n"

    @pt.mark.parametrize("path, expected_numbers", arguments_settings, ids=arguments_ids)
    def test_wrong_arguments(self, capsys, lox, path, expected_numbers):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 70

        expected, got, line = expected_numbers
        capture = capsys.readouterr().err
        assert capture == f"Error: Expected {expected} arguments but got {got}.\n[line {line}]\n"
