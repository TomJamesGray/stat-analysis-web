import csv
from stat_analysis.datasets.dataset import DataSet

class CSVDataset(DataSet):
    def __init__(self,fname):
        self.fname = fname

    def __iter__(self):
        with open(self.fname,'r') as f:
            reader = csv.reader(f)
            # TODO: Check if there is a title row, and exclude it
            for r in reader:
                yield r
