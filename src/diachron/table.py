class TableColumn:
    def __init__(self, title, elements):
        self.title = title
        self.elements = elements

def make_table(columns):
    output = "<body>\n"
    style = '"border: 1px solid black;"'
    if not style:
        output += "<table>\n"
    else:
        output += "<table style=" + style + ">\n"
    
    rows = 0
    for column in columns:
        rows = max(rows, len(column.elements) + 1)

    output += "<tr>"
    for column in columns:
        output += "<th style=\"border: 1px solid black; padding: 8px;\">" + column.title + "</th>"
    output += "</tr>"

    for r in range(0, rows):
        output += "<tr>"
        for column in columns:
            if r < len(column.elements):
                output += "<td style=\"border: 1px solid black; padding: 8px;\">"
                output += column.elements[r]
                output += "</td>"
        output += "</tr>"
    
    # Closing
    output += "</table>\n"
    output += "</body>\n"

    return output