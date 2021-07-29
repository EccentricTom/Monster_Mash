# This will be the constructor that will be used as the backbone of the monster creator

# Import library
import pandas as pd
import numpy as np
import json
import os

# Set the working directory
os.chdir(os.path.split(os.getcwd())[0])

# This is the parent class when building around CR
class MonsterFromCR():
    def __init__(self, CR, size="Medium", legendary=False):
        self.CR = CR
        self.legendary = legendary
        self.size = size
        df = pd.read_csv("Data/size_hp_chart.csv", index_col=0)
        self.hit_die = df.loc[size, 'Hit Die']
        self.hp_avg = df.loc[size, 'Average HP per Die']
        del df
    def type(self, type):
        self.type = type


test = MonsterFromCR(5, size="Gargantuan")
print(test.hit_die)
