import time


def __get_col_by_name(row,col_name):
    for col,d in row.items():
        if col.name == col_name:
            return (col,d)


def matches(data,col):
    col_name = col.name
    output = {}
    for row in data:
        if row[col_name] in output:
            output[row[col_name]].append(row)
        else:
            output[row[col_name]] = [row]

    return output


def same_hour(data,col):
    col_name = col.name
    output = {}
    for row in data:
        _,col_data = __get_col_by_name(row,col_name)
        try:
            h = str(time.strptime(col_data,col.format).tm_hour)
        except ValueError as e:
            print("Value Error {}\nDoes {} match time format {} ?".format(e,col_data,col.format))
            continue

        if h in output:
            output[h].append(row)
        else:
            output[h] = [row]

    return output