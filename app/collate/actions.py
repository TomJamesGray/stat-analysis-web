def __get_col_by_name(data,col_name):
    for col,d in data.items():
        if col.name == col_name:
            return (col,d)


def sum(data,col_name):
    output = {}
    for key,value in data.items():
        for data_item in value:
            # print(data_item)
            _,col_data = __get_col_by_name(data_item,col_name)
            if key in output:
                output[key] += int(col_data)
            else:
                output[key] = int(col_data)

    return output