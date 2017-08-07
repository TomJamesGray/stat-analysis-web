def matches(data,col_name):
    output = {}
    for row in data:
        if row[col_name] in output:
            output[row[col_name]].append(row)
        else:
            output[row[col_name]] = [row]

    return output