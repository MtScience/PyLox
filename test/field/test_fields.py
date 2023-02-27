import pytest as pt

get_settings = [("field/get_on_bool.lox", 1),
                ("field/get_on_class.lox", 2),
                ("field/get_on_function.lox", 2),
                ("field/get_on_nil.lox", 1),
                ("field/get_on_num.lox", 1),
                ("field/get_on_string.lox", 1)]
set_settings = [("field/set_on_bool.lox", 1),
                ("field/set_on_class.lox", 2),
                ("field/set_on_function.lox", 2),
                ("field/set_on_nil.lox", 1),
                ("field/set_on_num.lox", 1),
                ("field/set_on_string.lox", 1)]
get_set_ids = ["on bool", "on class", "on function", "on nil", "on number", "on string"]


class TestFields:
    def test_call_function_field(self, capsys, lox):
        lox.run_file("field/call_function_field.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["bar", "1", "2"]) + "\n"

    def test_get_set_method(self, capsys, lox):
        lox.run_file("field/get_and_set_method.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["other", "1", "method", "2"]) + "\n"

    def test_get_on_instance(self, capsys, lox):
        lox.run_file("field/on_instance.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["bar value", "baz value"] * 2) + "\n"

    def test_method(self, capsys, lox):
        lox.run_file("field/method.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["got method", "arg"]) + "\n"

    def test_this_binding(self, capsys, lox):
        lox.run_file("field/method_binds_this.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["foo1", "1"]) + "\n"

    def test_whole_lotta_fields(self, capsys, lox):
        lox.run_file("field/many.lox")

        expected_val = ['apple', 'apricot', 'avocado', 'banana', 'bilberry', 'blackberry', 'blackcurrant', 'blueberry',
                        'boysenberry', 'cantaloupe', 'cherimoya', 'cherry', 'clementine', 'cloudberry', 'coconut',
                        'cranberry', 'currant', 'damson', 'date', 'dragonfruit', 'durian', 'elderberry', 'feijoa',
                        'fig', 'gooseberry', 'grape', 'grapefruit', 'guava', 'honeydew', 'huckleberry', 'jabuticaba',
                        'jackfruit', 'jambul', 'jujube', 'juniper', 'kiwifruit', 'kumquat', 'lemon', 'lime', 'longan',
                        'loquat', 'lychee', 'mandarine', 'mango', 'marionberry', 'melon', 'miracle', 'mulberry',
                        'nance', 'nectarine', 'olive', 'orange', 'papaya', 'passionfruit', 'peach', 'pear', 'persimmon',
                        'physalis', 'pineapple', 'plantain', 'plum', 'plumcot', 'pomegranate', 'pomelo', 'quince',
                        'raisin', 'rambutan', 'raspberry', 'redcurrant', 'salak', 'salmonberry', 'satsuma',
                        'strawberry', 'tamarillo', 'tamarind', 'tangerine', 'tomato', 'watermelon', 'yuzu']

        capture = capsys.readouterr().out
        assert capture == "\n".join(expected_val) + "\n"

    @pt.mark.parametrize("path,line", get_settings, ids=get_set_ids)
    def test_get(self, capsys, lox, path, line):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == f"Error: Only instances have properties.\n[line {line}]\n"

    @pt.mark.parametrize("path,line", set_settings, ids=get_set_ids)
    def test_set(self, capsys, lox, path, line):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == f"Error: Only instances have fields.\n[line {line}]\n"

    def test_call_nonfunction_field(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("field/call_nonfunction_field.lox")
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == "Error: Can only call functions and classes.\n[line 6]\n"

    def test_set_eval_order(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("field/set_evaluation_order.lox")
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == "Error: Undefined variable 'undefined1'.\n[line 1]\n"

    def test_undefined(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("field/undefined.lox")
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == "Error: Undefined property 'bar'.\n[line 4]\n"
