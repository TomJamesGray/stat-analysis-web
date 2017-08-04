def sum(data,col_name):
    output = {}
    for key,value in data.items():
        for data_item in value:
            if key in output:
                output[key] += int(data_item[col_name])
            else:
                output[key] = int(data_item[col_name])

    return output