import re

class ImportSummary:
    def __init__(self, imports, terms, bodylines, errors):
        self.imports = imports
        self.terms = terms
        self.bodylines = bodylines
        self.errors = errors

def get_import(filepath, alias=None, items=None, comment="None"):
    return { "filepath": filepath, "alias": alias, "items": items, "comment": comment }

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
        errors = []

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
                    terms.append([path, [path + "."]])
                elif alias != None:
                    named_imports.append(new_import)
                    terms.append([alias, [alias + "."]])
                else:
                    imports.append(new_import)
                    terms.append([path, [path]])

                # if len(non_imports) > 0:
                #     errors.append("ERROR: import in body: " + line.strip())

                continue

            elif from_match != None:
                path = from_match.group(1)
                items = [x.strip() for x in from_match.group(2).split(",")]
                comment = from_match.group(4)
                item_imports.append(get_import(path, items=items, comment=comment))
                terms += [[i, [i + ".", i + "("]] for i in items]

                # if len(non_imports) > 0:
                #     errors.append("ERROR: import in body:\n" + line.strip())

                continue

            elif not is_blank or len(non_imports) > 0:
                non_imports.append(line)

        all_imports = [dotless_imports, imports, named_imports, item_imports]

        return ImportSummary(all_imports, terms, non_imports, errors)

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
    else:
        write_ordered(file, summary)

    return len(errors) == 0
