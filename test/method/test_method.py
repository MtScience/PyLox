import pytest as pt

too_many_settings = [("method/too_many_arguments.lox", "arguments"),
                     ("method/too_many_parameters.lox", "parameters")]
too_many_ids = ["arguments", "parameters"]

arguments_settings = [("method/extra_arguments.lox", (2, 4, 8)),
                      ("method/missing_arguments.lox", (2, 1, 5))]
arguments_ids = ["extra", "missing"]


class TestMethods:
    def test_arity(self, capsys, lox):
        lox.run_file("method/arity.lox")

        # This a Python way of doing what is known among Haskellers as "scanl". Rather ugly, might I say, when compared
        # to the Haskell way:
        # scanl (+) 1 [2 .. 8]
        acc = 0
        nums = [acc := acc + x for x in range(1, 9)]
        expected_val = ["no args"] + [str(n) for n in nums]

        capture = capsys.readouterr().out
        assert capture == "\n".join(expected_val) + "\n"

    def test_empty_method(self, capsys, lox):
        lox.run_file("method/empty_block.lox")
        capture = capsys.readouterr().out
        assert capture == "nil\n"

    def test_print_bound_method(self, capsys, lox):
        lox.run_file("method/print_bound_method.lox")
        capture = capsys.readouterr().out
        assert capture == "<fn method>\n"

    @pt.mark.parametrize("path,expected_numbers", arguments_settings, ids=arguments_ids)
    def test_wrong_arguments(self, capsys, lox, path, expected_numbers):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 70

        expected, got, line = expected_numbers
        capture = capsys.readouterr().err
        assert capture == f"Error: Expected {expected} arguments but got {got}.\n[line {line}]\n"

    @pt.mark.parametrize("path,typ", too_many_settings, ids=too_many_ids)
    def test_too_many(self, capsys, lox, path, typ):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == f"[line 259] Error at 'a': Can't have more than 255 {typ}.\n"

    def test_unknown_method(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("method/not_found.lox")
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == "Error: Undefined property 'unknown'.\n[line 3]\n"

    def test_refer_to_name(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("method/refer_to_name.lox")
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == "Error: Undefined variable 'method'.\n[line 3]\n"
