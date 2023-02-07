class TestBlock:
    def test_empty(self, capsys, lox):
        lox.run_file("block/empty.lox")
        capture = capsys.readouterr().out
        assert capture == "ok\n"

    def test_scope(self, capsys, lox):
        lox.run_file("block/scope.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["inner", "outer"]) + "\n"
