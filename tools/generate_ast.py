from io import StringIO
import sys
from typing import List, Literal

def define_type(writer: StringIO, base_name: str, class_name: str, field_names: List[str], field_types: List[str]):
    lines  = [
        "",
        "class %s(%s):" % (class_name, base_name),
        "    def __init__(self, %s):" % ", ".join(field_names)
    ]
    store_lines = ["        self.%s = %s" % (fname,fname) for fname in field_names]
    check_lines = ["        assert(isinstance(%s,%s))" % (fname, ftype) for fname, ftype in zip(field_names, field_types)]
    lines.extend(store_lines)
    lines.extend(check_lines)
    writer.write("\n".join(lines))




def define_ast(output_dir,  base_name: str, types: List[str]):
    path = output_dir+"/"+base_name.lower()+".py"

    writer = StringIO()
    writer.writelines(["from abc import ABC\n"])
    writer.writelines(["from tokens import Token\n"])
    writer.writelines(["\n"])
    writer.writelines(["class %s(ABC):\n" % base_name])
    writer.writelines([
        "    def accept(self, visitor):\n",
        "        return visitor.visit(self)\n"
    ])

    for type in types:
        class_name = type.split(':')[0].strip()
        fields = type.split(':')[1].strip().split(',')

        field_names = [x.strip().split(' ')[1].strip() for x in fields]
        field_types = [x.strip().split(' ')[0].strip() for x in fields]

        define_type(writer, base_name, class_name, field_names, field_types)

    with open(path, 'w') as f:
        f.write(writer.getvalue())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_ast.py <output directory>")
        exit(64)
    
    output_dir = sys.argv[1]

    define_ast(output_dir, "Expr", [
      "Binary   : Expr left, Token operator, Expr right",
      "Grouping : Expr expression",
      "Literal  : object value",
      "Unary    : Token operator, Expr right",
      "Variable : Token name"
    ])

    define_ast(output_dir, "Stmt", [
      "Expression : Expr expression",
      "Print      : Expr expression",
      "Var        : Token name, Expr initializer"
    ])


