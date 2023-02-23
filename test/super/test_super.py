import pytest as pt

method_call_settings = [("super/call_same_method.lox", "foo"),
                        ("super/call_other_method.lox", "bar")]
method_call_ids = ["same", "other"]

arguments_settings = [("super/extra_arguments.lox", (2, 4, 10)),
                      ("super/missing_arguments.lox", (2, 1, 9))]
arguments_ids = ["extra", "missing"]

superclass_paths = ["super/no_superclass_bind.lox", "super/no_superclass_call.lox"]
superclass_ids = ["bind", "call"]

in_inherited_paths = ["super/super_in_inherited_method.lox", "super/super_in_closure_in_inherited_method.lox"]
in_inherited_ids = ["method", "closure in method"]

syntax_settings = [("super/super_without_dot.lox", "[line 5] Error at ';': Expect '.' after 'super'.\n"),
                   ("super/super_without_name.lox", "[line 5] Error at ';': Expect superclass method name.\n")]
syntax_ids = ["dot", "name"]


class TestSuper:
    @pt.mark.parametrize("path,expected_name", method_call_settings, ids=method_call_ids)
    def test_call_method(self, capsys, lox, path, expected_name):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == f"Derived.{expected_name}()\nBase.foo()\n"

    def test_constructor(self, capsys, lox):
        lox.run_file("super/constructor.lox")
        capture = capsys.readouterr().out
        assert capture == "Derived.init()\nBase.init(a, b)\n"

    def test_indirect_inheritance(self, capsys, lox):
        lox.run_file("super/indirectly_inherited.lox")
        capture = capsys.readouterr().out
        assert capture == "C.foo()\nA.foo()\n"

    def test_bound_method(self, capsys, lox):
        lox.run_file("super/bound_method.lox")
        capture = capsys.readouterr().out
        assert capture == "A.method(arg)\n"

    def test_closure(self, capsys, lox):
        lox.run_file("super/closure.lox")
        capture = capsys.readouterr().out
        assert capture == "Base\n"

    def test_reassign_superclass(self, capsys, lox):
        lox.run_file("super/reassign_superclass.lox")
        capture = capsys.readouterr().out
        assert capture == "Base.method()\n" * 2

    def test_parentheses(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("super/parenthesized.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == f"[line 7] Error at ')': Expect '.' after 'super'.\n"

    @pt.mark.parametrize("path", in_inherited_paths, ids=in_inherited_ids)
    def test_super_in_inherited(self, capsys, lox, path):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == f"A\n"

    def test_top_level(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("super/super_at_top_level.lox")
            assert exc.value == 65

        expected_val = [f"[line {l}] Error at 'super': Can't use 'super' outside of a class.\n" for l in (1, 2)]
        expected_val = "".join(expected_val)

        capture = capsys.readouterr().err
        assert capture == expected_val

    def test_this_in_superclass(self, capsys, lox):
        lox.run_file("super/this_in_superclass_method.lox")
        capture = capsys.readouterr().out
        assert capture == "a\nb\n"

    def test_function(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("super/super_in_top_level_function.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == "[line 2] Error at 'super': Can't use 'super' outside of a class.\n"

    @pt.mark.parametrize("path,msg", syntax_settings, ids=syntax_ids)
    def test_missing_syntax(self, capsys, lox, path, msg):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == msg

    @pt.mark.parametrize("path", superclass_paths, ids=superclass_ids)
    def test_no_superclass(self, capsys, lox, path):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == f"[line 3] Error at 'super': Can't use 'super' in a class with no superclass.\n"

    def test_no_superclass_method(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("super/no_superclass_method.lox")
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == "Error: Undefined property 'doesNotExist'.\n[line 5]\n"

    @pt.mark.parametrize("path,expected_numbers", arguments_settings, ids=arguments_ids)
    def test_wrong_arguments(self, capsys, lox, path, expected_numbers):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 70

        expected, got, line = expected_numbers
        capture = capsys.readouterr().err
        assert capture == f"Error: Expected {expected} arguments but got {got}.\n[line {line}]\n"