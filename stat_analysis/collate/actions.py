def sum(data,col_name):
    output = {}
    for key,value in data.items():
        for data_item in value:
            try:
                if key in output:
                    output[key] += int(data_item[col_name])
                else:
                    output[key] = int(data_item[col_name])
            except Exception as e:
                print("Exception : {} raised at {}".format(e,data_item))


    return output