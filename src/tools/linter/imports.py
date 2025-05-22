import re

class ImportSummary:
    def __init__(self, imports, terms, bodylines, order_changed, errors):
        self.imports = imports
        self.terms = terms
        self.bodylines = bodylines
        self.order_changed = order_changed
        self.errors = errors

def get_import(filepath, alias=None, items=None, comment="None"):
    return { "filepath": filepath, "alias": alias, "items": items, "comment": comment }

def get_sort_key(imp):
    name = imp["filepath"]

    if imp["alias"] == None and imp["items"] == None:
        if "." not in name:
            imp_class = 0
        else:
            imp_class = 1
    elif imp["alias"] != None:
        imp_class = 2
    elif imp["items"] != None:
        imp_class = 3

    return [imp_class, name]

def write_import(_import):
    infodict = _import

    if infodict["items"] == None:
        output = "import " + infodict["filepath"]    
        if infodict["alias"] != None:
            output += " as " + infodict["alias"]
    else:
        output = "from " + infodict["filepath"] + " import " + ", ".join(infodict["items"])

    if infodict["comment"] != None:
        output += " # " + comment

    return output

def read_imports(file):
    with open(file, "r") as file_data:
        dotless_imports = []
        imports = []
        named_imports = []
        item_imports = []
        non_imports = []

        terms = []
        order_changed = False
        errors = []

        import_regex = re.compile("import ([\\w._]+)( as ([\\w.]+))?(\\s*#\\s*(.*))?")
        from_regex = re.compile("from ([\\w._]+) import ([\\w_,\\s]+)(\\s*#\\s*(.*))?")
        blank_regex = re.compile("^\\s*$")
        comment_regex = re.compile("\\s*#\\s*(.*)")

        last = None
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
                    terms.append([path, [path + "."]])
                elif alias != None:
                    named_imports.append(new_import)
                    terms.append([alias, [alias + "."]])
                else:
                    imports.append(new_import)
                    terms.append([path, [path]])

                if last != None and not order_changed and get_sort_key(new_import) < get_sort_key(last):
                    order_changed = True

                last = new_import

                # if len(non_imports) > 0:
                #     errors.append("ERROR: import in body: " + line.strip())

                continue

            elif from_match != None:
                path = from_match.group(1)
                items = [x.strip() for x in from_match.group(2).split(",")]
                comment = from_match.group(4)

                new_import = get_import(path, items=items, comment=comment)
                item_imports.append(new_import)
                terms += [[i, [i + ".", i + "("]] for i in items]

                if last != None and not order_changed and get_sort_key(new_import) < get_sort_key(last):
                    order_changed = True

                last = new_import

                # if len(non_imports) > 0:
                #     errors.append("ERROR: import in body:\n" + line.strip())

                continue

            elif not is_blank or len(non_imports) > 0:
                non_imports.append(line)

        all_imports = [
            sorted(dotless_imports, key=get_sort_key),
            sorted(imports, key=get_sort_key),
            sorted(named_imports, key=get_sort_key),
            sorted(item_imports, key=get_sort_key),
        ]

        return ImportSummary(all_imports, terms, non_imports, order_changed, errors)

def verify_imports(summary):
    errors = []

    found = []
    for line in summary.bodylines:
        for term in summary.terms:
            if term[0] in found:
                continue

            for form in term[1]:
                code = line.split("#")[0]
                if form in code:
                    found.append(term[0])
                    break

    if len(found) != len(summary.terms):
        diff = len(summary.terms) - len(found)
        errors.append("ERROR: " + str(diff) + " unused imports: " + ", ".join([x[0].strip() for x in summary.terms if x[0] not in found]))

    return errors

def write_ordered(file, summary):
    ordered = ""

    for import_type in summary.imports:
        if len(import_type) > 0:
            for imp in import_type:
                ordered += write_import(imp) + "\n"

            ordered += "\n"

    for line in summary.bodylines:
        ordered += line

    with open(file, "w") as f:
        f.write(ordered)

def lint_imports(file):
    ordered = ""
    errors = []

    summary = read_imports(file)

    errors = summary.errors
    errors += verify_imports(summary)

    if len(errors) > 0:
        print(str(len(errors)) + " errors found in file '" + file + "':")
        for error in errors:
            print("- " + error)
    elif summary.order_changed:
        write_ordered(file, summary)

    return len(errors) == 0
