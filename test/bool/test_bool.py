class TestBoolean:
    def test_equality(self, capsys, lox):
        lox.run_file("bool/equality.lox")
        captured = capsys.readouterr().out

        expected_val = [True, False, False, True] + [False] * 5
        expected_val += [not v for v in expected_val]
        expected_val = "\n".join([str(v).lower() for v in expected_val]) + "\n"

        assert captured == expected_val

    def test_not(self, capsys, lox):
        lox.run_file("bool/not.lox")
        captured = capsys.readouterr().out

        expected_val = [False, True, True]
        expected_val = "\n".join([str(v).lower() for v in expected_val]) + "\n"

        assert captured == expected_val
