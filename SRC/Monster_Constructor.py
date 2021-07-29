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
    def __init__(self, CR, size="Medium", legendary=False, name='Monster', alignment="Unaligned",
                 type="Monstrosity", resistences=None, immunities=None, cond_immun=None, attacks=1):
        self.target_CR = CR
        self.name = name
        self.legendary = legendary
        self.size = size
        self.type = type
        self.alignment = alignment
        self.resistences = resistences
        self.immunities = immunities
        self.condition_immunity = cond_immun
        df = pd.read_csv("Data/size_hp_chart.csv", index_col=0)
        self.hit_die = df.loc[size, 'Hit Die']
        self.hp_avg = df.loc[size, 'Average HP per Die']
        self.attack_num = attacks
        del df
    def set_type(self, type):
        self.type = type
    def set_CR(self, CR):
        self.CR = CR
    def set_size(self, size):
        self.size = size
        df = pd.read_csv("Data/size_hp_chart.csv", index_col=0)
        self.hit_die = df.loc[size, 'Hit Die']
        self.hp_avg = df.loc[size, 'Average HP per Die']
        del df
    def name_change(self, name):
        self.name = name
    def set_alignment(self, alignment):
        self.alignment = alignment
    def set_resistence(self, resistence):
        self.resistences = resistence
    def set_immunity(self, immunity):
        self.immunities = immunity
    def set_condition_immunity(self, cond_immunity):
        self.condition_immunity = cond_immunity
    def set_AC(self, AC):
        self.AC = AC
        df = pd.read_csv('Data/CR_table.csv', index_col=0)
        self.AC_CR = df['CR as float'].loc[df['Armor Class']== AC].tolist()[0]
        del df
    def show(self):
        print("This is {name}, a CR{CR} {size} {type} of {alignment} alignment \n"
              "Tt has these resistances: {resistances} \n"
              "It has these immunities:  {immunities} \n"
              "It has these condition immunities: {cond_immun} \n"
              "Legendary Status: {legend}".format(name=self.name, CR = self.target_CR, size=self.size, type=self.type,
                                                  alignment = self.alignment, resistances=self.resistences,
                                                  immunities=self.immunities, legend = self.legendary,
                                                  cond_immun=self.condition_immunity))



test = MonsterFromCR(CR=5, size="Gargantuan")
test.show()
test.set_type("Humanoid")
test.name_change("David")
test.set_resistence(["Fire", "Cold"])
test.show()
test.set_AC(19)
print(test.AC_CR)
