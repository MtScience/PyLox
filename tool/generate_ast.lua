function define_type(file, base_name, class_name, fields)
    file:write("class ", class_name, base_name, "(", base_name, "):\n")
    file:write("    def __init__(self, ", fields, "):\n")

    for field in fields:gmatch "([%a_]+: [%[%]%a%s|]+)" do
        local val = field:match "([%a_]+):"
        file:write("        self.", field, " = ", val, "\n")
    end

    file:write("\n    def accept(self, visitor: ", base_name, "Visitor", "):\n")
    file:write("        return visitor.visit_", class_name:lower(), "_", base_name:lower(), "(self)\n")
    file:write "\n\n"
end

function define_visitor(file, base_name, class_name)
    local base = base_name:lower()
    file:write "    @abstractmethod\n"
    file:write("    def visit_", class_name:lower(), "_", base, "(self, ", base, ": ", base_name, "): ...\n\n")
end

function define_all(file, exprtypes)
    for i, exprtype in ipairs(exprtypes) do
        exprtypes[i] = "\"" .. exprtype .. "\""
    end

    file:write("__all__ = [", table.concat(exprtypes, ", "), "]\n")
end

function define_ast(out_dir, base_name, exprtypes, imports)
    local path = out_dir .. "/" .. base_name:lower() .. ".py"

    -- Open/create the file
    local file = io.open(path, "w")

    -- Actual writing: imports and main class
    file:write "from abc import ABC, abstractmethod\n\n"
    for _, import in ipairs(imports) do
        file:write("from ", import.from, " import ", import.what, "\n")
    end
    file:write "\n\n"
    file:write("class ", base_name, "(ABC):\n")
    file:write "    @abstractmethod\n"
    file:write "    def accept(self, visitor): ...\n\n\n"

    -- Defining a visitor interface
    file:write("class " .. base_name .. "Visitor(ABC):\n")
    local types = {base_name}
    for _, exprtype in ipairs(exprtypes) do
        local class_name = exprtype:match "(%a+)%s+:%s+[%g%s]+"
        types[#types + 1] = class_name .. base_name
        define_visitor(file, base_name, class_name)
    end

    file:write "\n"

    for _, exprtype in ipairs(exprtypes) do
        local class_name, fields = string.match(exprtype, "(%a+)%s+:%s+([%g%s]+)")
        define_type(file, base_name, class_name, fields)
    end

    table.insert(types, 2, base_name .. "Visitor")

    define_all(file, types)

    -- Close the file
    file:close()
end

exprs = {"Assign   : name: Token, value: Expr",
         "Binary   : left: Expr, operator: Token, right: Expr",
         "Call     : callee: Expr, paren: Token, arguments: list[Expr]",
         --"Get      : obj: Expr, name: Token",
         "Grouping : expr: Expr",
         "Literal  : value: object",
         "Logical  : left: Expr, operator: Token, right: Expr",
         --"Set      : obj: Expr, name: Token, value: Expr",
         --"This     : keyword: Token",
         "Unary    : operator: Token, right: Expr",
         "Variable : name: Token"}
define_ast("../src", "Expr", exprs, {{from = "tokenclass", what = "Token"}})

stmts = {"Block      : statements: list[Stmt]",
         "Expression : expression: Expr",
         "Function   : name: Token, params: list[Token], body: list[Stmt]",
         "If         : condition: Expr, if_clause: Stmt, else_clause: Stmt | None",
         "Print      : expression: Expr",
         --"Return     : keyword: Token, value: Expr | None",
         "Var        : name: Token, initializer: Expr",
         "While      : condition: Expr, body: Stmt",
         --"Class      : name: Token, methods: list[FunctionStmt]"
}
define_ast("../src", "Stmt", stmts, {{from = "expr", what = "Expr"}, {from = "tokenclass", what = "Token"}})
