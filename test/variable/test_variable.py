import pytest as pt

use_as_var_settings = [("variable/use_this_as_var.lox", "this"),
                       ("variable/use_nil_as_var.lox", "nil"),
                       ("variable/use_false_as_var.lox", "false")]

undefined_paths = ["variable/undefined_global.lox", "variable/undefined_local.lox"]
undefined_ids = ["global", "local"]

reset_settings = [("variable/redefine_global.lox", "2"),
                  ("variable/redeclare_global.lox", "nil")]
reset_ids = ["redefine", "redeclare"]

shadow_settings = [("variable/shadow_global.lox", ["shadow", "global"]),
                   ("variable/shadow_local.lox", ["shadow", "local"]),
                   ("variable/shadow_and_local.lox", ["outer", "inner"])]
shadow_ids = ["global", "local", "in block"]

duplicate_settings = [("variable/duplicate_local.lox", "a", 3),
                      ("variable/duplicate_parameter.lox", "arg", 2)]
duplicate_ids = ["local", "parameter"]


class TestVariables:
    def test_use_global_in_init(self, capsys, lox):
        lox.run_file("variable/use_global_in_initializer.lox")
        capture = capsys.readouterr().out
        assert capture == "value\n"

    def test_uninitialized(self, capsys, lox):
        lox.run_file("variable/uninitialized.lox")
        capture = capsys.readouterr().out
        assert capture == "nil\n"

    def test_unreachable(self, capsys, lox):
        lox.run_file("variable/unreached_undefined.lox")
        capture = capsys.readouterr().out
        assert capture == "ok\n"

    def test_scope_reuse(self, capsys, lox):
        lox.run_file("variable/scope_reuse_in_different_blocks.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["first", "second"]) + "\n"

    def test_local_from_method(self, capsys, lox):
        lox.run_file("variable/local_from_method.lox")
        capture = capsys.readouterr().out
        assert capture == "variable\n"

    def test_nested_block(self, capsys, lox):
        lox.run_file("variable/in_nested_block.lox")
        capture = capsys.readouterr().out
        assert capture == "outer\n"

    def test_in_the_middle_of_block(self, capsys, lox):
        lox.run_file("variable/in_middle_of_block.lox")
        capture = capsys.readouterr().out
        assert capture == "\n".join(["a", "a b", "a c", "a b d"]) + "\n"

    def test_early_bound(self, capsys, lox):
        lox.run_file("variable/early_bound.lox")
        capture = capsys.readouterr().out
        assert capture == "outer\n" * 2

    @pt.mark.parametrize("path,expected_val", reset_settings, ids=reset_ids)
    def test_reset_global(self, capsys, lox, path, expected_val):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == expected_val + "\n"

    @pt.mark.parametrize("path,expected_val", shadow_settings, ids=shadow_ids)
    def test_shadow(self, capsys, lox, path, expected_val):
        lox.run_file(path)
        capture = capsys.readouterr().out
        assert capture == "\n".join(expected_val) + "\n"

    def test_collide_with_parameter(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("variable/collide_with_parameter.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == "[line 2] Error at 'a': Already a variable with this name in this scope.\n"

    @pt.mark.parametrize("path,token,line", duplicate_settings, ids=duplicate_ids)
    def test_duplicate(self, capsys, lox, path, token, line):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == f"[line {line}] Error at '{token}': Already a variable with this name in this scope.\n"

    def test_use_local_in_init(self, capsys, lox):
        with pt.raises(SystemExit) as exc:
            lox.run_file("variable/use_local_in_initializer.lox")
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == "[line 3] Error at 'a': Can't read local variable in its own initializer.\n"

    @pt.mark.parametrize("path", undefined_paths, ids=undefined_ids)
    def test_undefined(self, capsys, lox, path):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 70

        capture = capsys.readouterr().err
        assert capture == "Error: Undefined variable 'notDefined'.\n[line 2]\n"

    @pt.mark.parametrize("path,token", use_as_var_settings, ids=[t for p, t in use_as_var_settings])
    def test_use_as_var(self, capsys, lox, path, token):
        with pt.raises(SystemExit) as exc:
            lox.run_file(path)
            assert exc.value == 65

        capture = capsys.readouterr().err
        assert capture == f"[line 2] Error at '{token}': Expect a variable name.\n"
