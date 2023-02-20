import pytest as pt

recursion_settings = ["function/recursion.lox", "function/local_recursion.lox"]
recursion_ids = ["regular", "local"]

arguments_settings = [("function/extra_arguments.lox", (2, 4, 6)),
                      ("function/missing_arguments.lox", (2, 1, 3))]
arguments_ids = ["extra", "missing"]

too_many_settings = [("function/too_many_arguments.lox", "arguments"),
                     ("function/too_many_parameters.lox", "parameters")]
too_many_ids = ["arguments", "parameters"]


class TestFunctions:
    def test_empty_body(self, capsys, lox):
        lox.run_file("function/empty_body.lox")
        capture = capsys.readouterr().out
        assert capture == "nil\n"

    def test_parameters(self, capsys, lox):
        lox.run_file("function/parameters.lox")

        acc = 0
        nums = [acc := acc + x for x in range(9)]

        capture = capsys.readouterr().out
        assert capture == "\n".join([str(n) for n in nums]) + "\n"

    def test_print(self, capsys, lox):
        lox.run_file("function/print.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["<fn foo>", "<native fn>"]) + "\n"

    def test_nested_call_with_args(self, capsys, lox):
        lox.run_file("function/nested_call_with_arguments.lox")
        capture = capsys.readouterr().out
        assert capture == "hello world\n"

    @pt.mark.parametrize("path", recursion_settings, ids=recursion_ids)
    def test_recursion(self, capsys, lox, path):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == "21\n"

    def test_mutual_recursion(self, capsys, lox):
        lox.run_file("function/mutual_recursion.lox")
        capture = capsys.readouterr().out
        assert capture == "true\n" * 2

    def test_local_mutual_recursion(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("function/local_mutual_recursion.lox")
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == "Error: Undefined variable 'isOdd'.\n[line 4]\n"

    def test_body_must_be_block(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("function/body_must_be_block.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == "[line 3] Error at '123': Expect '{' before function body.\n"

    def test_missing_comma(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("function/missing_comma_in_parameters.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == "[line 3] Error at 'c': Expect ')' after parameters.\n"

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
        assert capture == f"[line 260] Error at 'a': Can't have more than 255 {typ}.\n"