def test_nil(capsys, lox):
    lox.run_file("nil/literal.lox")
    capture = capsys.readouterr().out
    assert capture == "nil\n"
