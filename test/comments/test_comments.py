import pytest as pt

paths = ["comments/only_line_comment.lox", "comments/only_line_comment_and_line.lox"]
ids = ["only_line_comment", "only_line_comment_and_line"]


class TestComments:
    @pt.mark.parametrize("path", ["comments/line_at_eof.lox", "comments/unicode.lox"], ids=["line_at_EOF", "unicode"])
    def test_feature(self, capsys, lox, path):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == "ok\n"

    @pt.mark.parametrize("path", paths, ids=ids)
    def test_only_comments(self, capsys, lox, path):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == ""
