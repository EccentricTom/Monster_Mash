# This will be the constructor that will be used as the backbone of the monster creator

# Import library
import pandas as pd
import numpy as np
import json
import os

# Set the working directory
os.chdir(os.path.split(os.getcwd())[0])


# This is the parent class when building around CR

class MonsterFromCR:
    def __init__(self, cr, size="Medium", legendary=False, name='Monster', alignment="Unaligned",
                 monster_type="Monstrosity", resistances=None, immunities=None, cond_imm=None, attacks=1,
                 is_flying=False):
        self.target_CR = cr
        self.name = name
        self.legendary = legendary
        self.size = size
        self.type = monster_type
        self.alignment = alignment
        self.resistances = resistances
        self.immunities = immunities
        self.condition_immunity = cond_imm
        df_hp = pd.read_csv("Data/size_hp_chart.csv", index_col=0)
        df_cr = pd.read_csv("Data/CR_table.csv", index_col=0)
        self.hit_die = df_hp.loc[size, 'Hit Die']
        self.hp_avg = df_hp.loc[size, 'Average HP per Die']
        self.attack_num = attacks
        self.flying = is_flying
        self.str = 10
        self.dex = 10
        self.con = 10
        self.int = 10
        self.wis = 10
        self.cha = 10
        self.ac = df_cr["Armor Class"].loc[df_cr.index == cr]
        self.effective_AC = self.ac
        self.AC_CR = cr
        self.hit_die = df_hp.loc[size, 'Hit Die']
        self.hit_die_num = df_hp.loc[size, 'Hit Die number']
        self.hp_avg = df_hp.loc[size, 'Average HP per Die']
        if self.resistances is not None:
            # continue from here next
        self.dc = df_cr["Save DC"].loc[df_cr.index == cr]
        self.DC_CR = cr
        del df_hp

    def set_stats(self, strength=None, dexterity=None, constitution=None, intelligence=None, wisdom=None,
                  charisma=None):
        if strength is not None:
            self.str = strength
        if dexterity is not None:
            self.dex = dexterity
        if constitution is not None:
            self.con = constitution
        if intelligence is not None:
            self.int = intelligence
        if wisdom is not None:
            self.wis = wisdom
        if charisma is not None:
            self.cha = charisma

    def set_type(self, monster_type):
        self.type = monster_type

    def set_cr(self, cr):
        self.target_CR = cr

    def set_size(self, size):
        self.size = size
        df = pd.read_csv("Data/size_hp_chart.csv", index_col=0)
        self.hit_die = df.loc[size, 'Hit Die']
        self.hit_die_num = df.loc[size, 'Hit Die number']
        self.hp_avg = df.loc[size, 'Average HP per Die']
        del df

    def name_change(self, name):
        self.name = name

    def set_alignment(self, alignment):
        self.alignment = alignment

    def set_resistance(self, resistance):
        self.resistances = resistance

    def set_immunity(self, immunity):
        self.immunities = immunity

    def set_condition_immunity(self, cond_immunity):
        self.condition_immunity = cond_immunity

    def set_ac(self, ac):
        self.ac = ac
        df = pd.read_csv('Data/CR_table.csv', index_col=0)
        self.AC_CR = df['CR as float'].loc[df['Armor Class'] == ac].tolist()[0]
        if self.flying is True and self.target_CR <= 10:
            self.effective_AC = self.ac + 2
            self.AC_CR = df['CR as float'].loc[df['Armor Class'] == self.effective_AC].tolist()[0]
        del df

    def assess_cr(self):
        effective_cr = (self.effective_AC + 0) / 4
        return effective_cr == self.target_CR

    def show(self):
        print("This is {name}, a CR{cr} {size} {type} of {alignment} alignment \n"
              "Tt has these resistances: {resistances} \n"
              "It has these immunities:  {immunities} \n"
              "It has these condition immunities: {cond_imm} \n"
              "Legendary Status: {legend}".format(name=self.name, cr=self.target_CR, size=self.size, type=self.type,
                                                  alignment=self.alignment, resistances=self.resistances,
                                                  immunities=self.immunities, legend=self.legendary,
                                                  cond_imm=self.condition_immunity))


test = MonsterFromCR(cr=5, size="Gargantuan")
test.show()
test.set_type("Humanoid")
test.name_change("David")
test.set_resistance(["Fire", "Cold"])
test.show()
test.set_ac(19)
print(test.AC_CR)
