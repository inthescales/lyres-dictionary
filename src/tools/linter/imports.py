import re

def get_comment(text):
    return ["comment", text]

def get_import(filepath, alias=None, items=None, comment="None"):
    infodict = { "filepath": filepath, "alias": alias, "items": items, "comment": comment }
    return ["import", infodict]

def write_comment(comment):
    return comment[1]

def write_import(_import):
    infodict = _import[1]

    if infodict["items"] == None:
        edited = "import " + infodict["filepath"]    
        if infodict["alias"] != None:
            edited += " as " + infodict["alias"]
    else:
        edited = "from " + infodict["filepath"] + " import " + ", ".join(infodict["items"])

    if infodict["comment"] != None:
        edited += " # " + comment

    return edited

def order_error():
    print("ERROR: import after non-import:")
    print(line)
    exit(1)

def lint_imports(file):
    edited = ""

    with open(file, "r") as file_data:
        dotless_imports = []
        imports = []
        named_imports = []
        item_imports = []
        non_imports = []

        import_regex = re.compile("import ([\\w._]+)( as ([\\w.]+))?(\\s*#\\s*(.*))?")
        from_regex = re.compile("from ([\\w._]+) import ([\\w_,\\s]+)(\\s*#\\s*(.*))?")
        blank_regex = re.compile("^\\s*$")
        comment_regex = re.compile("\\s*#\\s*(.*)")

        for line in file_data.readlines():
            import_match = import_regex.match(line)
            from_match = from_regex.match(line)
            is_blank = blank_regex.match(line) != None

            if import_match != None:
                path = import_match.group(1)
                alias = import_match.group(3)
                comment = import_match.group(5)

                new_import = get_import(path, alias=alias, comment=comment)
                if "." not in path:
                    dotless_imports.append(new_import)
                elif alias != None:
                    named_imports.append(new_import)
                else:
                    imports.append(new_import)

                if len(non_imports) > 0:
                    order_error()
                continue

            elif from_match != None:
                path = from_match.group(1)
                items = [x.strip() for x in from_match.group(2).split(",")]
                comment = from_match.group(4)
                item_imports.append(get_import(path, items=items, comment=comment))
                if len(non_imports) > 0:
                    order_error()
                continue

            # comment_match = comment_regex.match(line)
            # elif comment_match != None:
            #     comments += get_comment(comment_match.group(1))
            #     continue

            elif not is_blank or len(non_imports) > 0:
                non_imports += line

        if len(dotless_imports) > 0:
            for dotless in dotless_imports:
                edited += write_import(dotless) + "\n"

            edited += "\n"

        if len(imports) > 0:
            for internal in imports:
                edited += write_import(internal) + "\n"

            edited += "\n"

        if len(named_imports) > 0:
            for named in named_imports:
                edited += write_import(named) + "\n"

            edited += "\n"

        if len(item_imports) > 0:
            for item in item_imports:
                edited += write_import(item) + "\n"

            edited += "\n"

        for non_import in non_imports:
            edited += non_import

    with open(file, "w") as f:
        f.write(edited)
