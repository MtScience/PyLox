import pytest as pt

add_incompatible_paths = ["operator/add_bool_nil.lox",
                          "operator/add_bool_num.lox",
                          "operator/add_bool_string.lox",
                          "operator/add_nil_nil.lox",
                          "operator/add_num_nil.lox",
                          "operator/add_string_nil.lox"]
add_incompatible_ids = ["bool + nil",
                        "bool + number",
                        "bool + string",
                        "2 nils",
                        "number + nil",
                        "string + nil"]

incompatible_paths = ["operator/divide_nonnum_num.lox",
                      "operator/divide_num_nonnum.lox",
                      "operator/multiply_nonnum_num.lox",
                      "operator/multiply_num_nonnum.lox",
                      "operator/subtract_nonnum_num.lox",
                      "operator/subtract_num_nonnum.lox",
                      "operator/power_nonnum_num.lox",
                      "operator/power_num_nonnum.lox",
                      "operator/modulo_nonnum_num.lox",
                      "operator/modulo_num_nonnum.lox",
                      "operator/greater_nonnum_num.lox",
                      "operator/greater_num_nonnum.lox",
                      "operator/greater_or_equal_nonnum_num.lox",
                      "operator/greater_or_equal_num_nonnum.lox",
                      "operator/less_nonnum_num.lox",
                      "operator/less_num_nonnum.lox",
                      "operator/less_or_equal_nonnum_num.lox",
                      "operator/less_or_equal_num_nonnum.lox"]
incompatible_ids = ["nonnum / num", "num / nonnum", "nonnum * num", "num * nonnum", "nonnum - num", "num - nonnum",
                    "nonnum ^ num", "num ^ nonnum", "nonnum % num", "num % nonnum",
                    "nonnum > num", "num > nonnum", "nonnum >= num", "num >= nonnum",
                    "nonnum < num", "num < nonnum", "nonnum <= num", "num <= nonnum"]


class TestOperators:
    def test_add(self, capsys, lox):
        lox.run_file("operator/add.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["579", "string"]) + "\n"

    def test_subtract(self, capsys, lox):
        lox.run_file("operator/subtract.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["1", "0"]) + "\n"

    def test_negate(self, capsys, lox):
        lox.run_file("operator/negate.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["-3", "3", "-3"]) + "\n"

    def test_modulo(self, capsys, lox):
        lox.run_file("operator/modulo.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["2", "0.33999999999999986", "10.100000000000001"]) + "\n"

    def test_divide(self, capsys, lox):
        lox.run_file("operator/divide.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["4", "1"]) + "\n"

    def test_multiply(self, capsys, lox):
        lox.run_file("operator/multiply.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["15", "3.702"]) + "\n"

    def test_power(self, capsys, lox):
        lox.run_file("operator/power.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["64", "28.9976173063065"]) + "\n"

    def test_compare(self, capsys, lox):
        lox.run_file("operator/comparison.lox")

        aux_1, aux_2 = [True, False, False], [True, True, False]
        aux_3, aux_4 = [not x for x in aux_1], [not x for x in aux_2]
        expected_val = aux_1 + aux_2 + aux_4 + aux_3 + [False] * 4 + [True] * 4
        expected_val = [str(x).lower() for x in expected_val]

        capture = capsys.readouterr().out
        assert capture == "\n".join(expected_val) + "\n"

    def test_not(self, capsys, lox):
        lox.run_file("operator/not.lox")

        aux_1 = [False, True, True]
        aux_2 = [not x for x in aux_1]
        expected_val = aux_1 + [False, False] + aux_2
        expected_val = [str(x).lower() for x in expected_val]

        capture = capsys.readouterr().out
        assert capture == "\n".join(expected_val) + "\n"

    def test_not_class(self, capsys, lox):
        lox.run_file("operator/not_class.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["false"] * 2) + "\n"

    def test_equals(self, capsys, lox):
        lox.run_file("operator/equals.lox")

        expected_val = [True] + [True, False] * 3 + [False] * 3
        expected_val = [str(x).lower() for x in expected_val]

        capture = capsys.readouterr().out
        assert capture == "\n".join(expected_val) + "\n"

    def test_not_equals(self, capsys, lox):
        lox.run_file("operator/not_equals.lox")

        expected_val = [False] + [False, True] * 3 + [True] * 3
        expected_val = [str(x).lower() for x in expected_val]

        capture = capsys.readouterr().out
        assert capture == "\n".join(expected_val) + "\n"

    def test_class_equals(self, capsys, lox):
        lox.run_file("operator/equals_class.lox")

        expected_val = [True, False, False, True] + [False] * 4
        expected_val = [str(x).lower() for x in expected_val]

        capture = capsys.readouterr().out
        assert capture == "\n".join(expected_val) + "\n"

    def test_method_equals(self, capsys, lox):
        lox.run_file("operator/equals_method.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["true", "false"]) + "\n"

    @pt.mark.parametrize("path", add_incompatible_paths, ids=add_incompatible_ids)
    def test_add_incompatible(self, capsys, lox, path):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == "Error: Operands must be two numbers or two strings.\n[line 1]\n"

    @pt.mark.parametrize("path", incompatible_paths, ids=incompatible_ids)
    def test_incompatible(self, capsys, lox, path):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == "Error: Operands must be numbers.\n[line 1]\n"

    def test_negate_nonnum(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("operator/negate_nonnum.lox")
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == "Error: Operand must be a number.\n[line 1]\n"
