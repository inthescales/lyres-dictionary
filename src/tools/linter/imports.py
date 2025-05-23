import re

# Summary of import reading process
class ImportSummary:
    def __init__(self, imports, bodylines, changes_made, errors):
        self.imports = imports
        self.bodylines = bodylines
        self.changes_made = changes_made
        self.errors = errors

# Returns a dictionary representing an import found in the file
def get_import(filepath, alias=None, items=None, terms=None, comment="None"):
    return { "filepath": filepath, "alias": alias, "items": items, "terms": terms, "comment": comment}

# Returns the name that should be used for the import, e.g. when looking for usages or printing errors
def get_imp_name(imp):
    return get_name(imp["filepath"], imp["alias"])

# Returns the name that should be used based on the given path and alias
def get_name(path, alias):
    if alias != None:
        return alias

    return path

# Returns the category of the import, for ordering and formatting
def get_category(imp):
    if imp["alias"] == None and imp["items"] == None:
        if "." not in get_imp_name(imp):
            return 0
        else:
            return 1
    elif imp["alias"] != None:
        return 2
    elif imp["items"] != None:
        return 3

    return 1_000_000

# Returns a sort key for the given import
def get_sort_key(imp):
    return [get_category(imp), imp["filepath"]]

# Returns a string for the import as it should appear in code
def write_import(imp):
    if imp["items"] == None:
        output = "import " + imp["filepath"]    
        if imp["alias"] != None:
            output += " as " + imp["alias"]
    else:
        output = "from " + imp["filepath"] + " import " + ", ".join(imp["items"])

    if imp["comment"] != None:
        output += " # " + comment

    return output

# Read and categorize the import statements in the file
def read_imports(file):
    with open(file, "r") as file_data:
        imports = []
        non_imports = []
        changes_made = False
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

                terms = [(get_name(path, alias), [get_name(path, alias) + "."])]
                new_import = get_import(path, alias=alias, terms=terms, comment=comment)

            elif from_match != None:
                path = from_match.group(1)
                items = [x.strip() for x in from_match.group(2).split(",")]
                comment = from_match.group(4)

                terms = [(i, [i + ".", i + "("]) for i in items]
                new_import = get_import(path, items=items, terms=terms, comment=comment)

            elif not is_blank or len(non_imports) > 0:
                new_import = None
                non_imports.append(line)
            else:
                new_import = None

            # Process new import
            if new_import != None:
                if new_import not in imports:
                    imports.append(new_import)
                else:
                    changes_made = True

                if last != None and not changes_made and get_sort_key(new_import) < get_sort_key(last):
                    changes_made = True

                # if len(non_imports) > 0:
                #     errors.append("ERROR: import in body:\n" + line.strip())

                last = new_import

        imports = sorted(imports, key=get_sort_key)
        unused = find_unused(imports, non_imports)

        if len(unused) > 0:
            names = "\n  - ".join([x for x in unused])
            errors.append("ERROR: " + str(len(unused)) + " unused imports:\n  - " + names)

        return ImportSummary(imports, non_imports, changes_made, errors)

# Verify that all imports are used at least once
def find_unused(imports, lines):
    errors = []

    found = {}
    for imp in imports:
        found[imp["filepath"]] = set()

    for line in lines:
        for imp in imports:
            items = imp["terms"]
            for item in items:
                for term in item[1]:
                    code = line.split("#")[0]
                    if term in code:
                        found[imp["filepath"]].add(item[0])
                        break

    unused = []
    for imp in imports:
        if imp["items"] == None and found[imp["filepath"]] == set():
            unused.append(get_imp_name(imp))
        if imp["items"] != None and set(imp["items"]) - found[imp["filepath"]] != set():
            unused += list(set(imp["items"]) - found[imp["filepath"]])

    return unused

# Rewrite the file with its imports in order, per the summary
def write_ordered(file, summary):
    ordered = ""
    last = None

    for i in range(0, len(summary.imports)):
        imp = summary.imports[i]

        if last != None and get_category(imp) != get_category(last):
            ordered += "\n"

        ordered += write_import(imp) + "\n"

        last = imp

    ordered += "\n"

    for line in summary.bodylines:
        ordered += line

    with open(file, "w") as f:
        f.write(ordered)

# Performs linting actions related to imports
def lint_imports(file):
    ordered = ""
    errors = []

    summary = read_imports(file)
    errors = summary.errors

    if len(errors) > 0:
        print(str(len(errors)) + " errors found in file '" + file + "':")
        for error in errors:
            print("- " + error)
    elif summary.changes_made:
        write_ordered(file, summary)

    return len(errors) == 0
