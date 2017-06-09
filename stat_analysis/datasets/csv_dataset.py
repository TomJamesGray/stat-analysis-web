import csv
from stat_analysis.datasets.dataset import DataSet

class CSVDataset(DataSet):
    def __init__(self,fname,col_names):
        self.fname = fname
        self.col_names = col_names
        super(CSVDataset,self).__init__(col_names)

    def __iter__(self):
        with open(self.fname,'r') as f:
            reader = csv.reader(f)
            # TODO: Check if there is a title row, and exclude it
            for r in reader:
                yield r
