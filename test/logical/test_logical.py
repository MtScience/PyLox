import pytest as pt

op_and_setting = "logical/and.lox", [False, 1, False, True, 3, True, False]
op_or_setting = "logical/or.lox", [1, 1, True] + [False] * 3 + [True]

op_and_truth_setting = "logical/and_truth.lox", ["false", "nil"] + ["ok"] * 3
op_or_truth_setting = "logical/or_truth.lox", ["ok", "ok", "true", "0", "s"]


class TestLogical:
    @pt.mark.parametrize("path,expected_val", [op_and_setting, op_or_setting], ids=["and", "or"])
    def test_op(self, capsys, lox, path, expected_val):
        lox.run_file(path)
        capture = capsys.readouterr().out

        expected_val = [str(v).lower() for v in expected_val]

        assert capture == "\n".join(expected_val) + "\n"

    @pt.mark.parametrize("path,expected_val", [op_and_truth_setting, op_or_truth_setting], ids=["and", "or"])
    def test_op_truth(self, capsys, lox, path, expected_val):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == "\n".join(expected_val) + "\n"
