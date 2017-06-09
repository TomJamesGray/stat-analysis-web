class DataSet(object):
    """
    Basic class for a data set, defines column names and methods for accessing
    """
    def __init__(self,cols):
        """
        Initialisation method for base DataSet class
        :param cols: Column names, data type with __iter__ method
        """
        self.col_names = cols