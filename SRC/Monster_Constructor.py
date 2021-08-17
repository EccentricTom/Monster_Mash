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
                 monster_type="Monstrosity", damage_source="strength", magic_source=None, resistances=None,
                 immunities=None, cond_imm=None, is_flying=False, set_damage=True, is_spellcaster=False,
                 innate_caster=False):
        df_hp = pd.read_csv("Data/size_hp_chart.csv", index_col=0)
        df_cr = pd.read_csv("Data/CR_table.csv", index_col=0)
        self.target_CR = cr
        self.name = name
        self.legendary = legendary
        self.size = size
        self.weapon_multiplier = df_hp.loc[size, "Size dice multiplier"]
        self.type = monster_type
        self.damage_source = damage_source
        self.magic_source = magic_source
        self.dpr_target = df_cr.loc[str(self.target_CR), "Damage/Round"].split("-")
        self.attack_dice = {}
        if set_damage is False:
            self.average_dmg = sum(self.dpr_target) / 2
        else:
            self.average_dmg = {}
        self.damage_type = {}
        self.dpr_cr = cr
        if is_spellcaster:
            self.spellcaster_type = input("select from full caster, half caster, third caster")
            print("Choose spellcasting level?")
            if input() == "yes" or "y":
                self.spellcaster_level = int(input("What spellcasting level?"))
            else:
                self.spellcaster_level = int(self.hp/(self.hp_avg + self.con_mod))
        self.innate_casting = innate_caster
        self.dc_target = df_cr.loc[str(self.target_CR), "Save DC"]
        self.dc_cr = cr
        self.alignment = alignment
        self.resistances = resistances
        self.immunities = immunities
        self.condition_immunity = cond_imm
        self.flying = is_flying
        self.str = 10
        self.str_mod = self.modifier(self.str)
        self.dex = 10
        self.dex_mod = self.modifier(self.dex)
        self.con = 10
        self.con_mod = self.modifier(self.con)
        self.int = 10
        self.int_mod = self.modifier(self.int)
        self.wis = 10
        self.wis_mod = self.modifier(self.wis)
        self.cha = 10
        self.cha_mod = self.modifier(self.cha)
        self.prof = df_cr.loc[str(self.target_CR), "Prof. Bonus"]
        self.ac = df_cr.loc[str(self.target_CR), "Armor Class"]
        self.effective_AC = self.ac
        self.check_flying()
        self.AC_CR = cr
        self.hit_die = 1
        self.hit_die_type = df_hp.loc[size, 'Hit Die']
        self.hit_die_type_num = df_hp.loc[size, 'Hit Die number']
        self.hp_avg = df_hp.loc[size, 'Average HP per Die']
        self.hp_target_range = [int(i) for i in (df_cr.loc["5", "Hit Points"].split("-"))]
        self.hp = int(sum(self.hp_target_range) / 2)
        self.effective_hp = self.hp_adjust(self.hp)
        self.dc = df_cr["Save DC"].loc[df_cr.index == cr]
        self.DC_CR = cr
        del df_hp
        del df_cr

    def spellcasting_capabilities(self):
        pass

    def hp_from_dice(self, dice_num):
        hp = dice_num * (self.hp_avg + self.con_mod)
        return hp

    def hp_adjust(self, hp):
        multiplier = 1
        if self.resistances is not None:
            if self.immunities is not None:
                if self.target_CR <= 10:
                    multiplier = 2
                elif self.target_CR <= 16:
                    multiplier = 1.5
                else:
                    multiplier = 1.25
                return hp * multiplier
            elif self.target_CR < 17:
                if self.target_CR <= 4:
                    multiplier = 2
                elif self.target_CR <= 10:
                    multiplier = 1.5
                elif self.target_CR <= 16:
                    multiplier = 1.25

            return hp * multiplier

    @staticmethod
    def modifier(stat):
        mod = int((stat - 10) / 2)
        return mod

    def set_stats(self, strength=None, dexterity=None, constitution=None, intelligence=None, wisdom=None,
                  charisma=None):
        if strength is not None:
            self.str = strength
            self.str_mod = self.modifier(self.str)
        if dexterity is not None:
            self.dex = dexterity
            self.dex_mod = self.modifier(self.dex)
        if constitution is not None:
            self.con = constitution
            self.con_mod = self.modifier(self.con)
        if intelligence is not None:
            self.int = intelligence
            self.int_mod = self.modifier(self.int)
        if wisdom is not None:
            self.wis = wisdom
            self.wis_mod = self.modifier(self.wis)
        if charisma is not None:
            self.cha = charisma
            self.cha_mod = self.modifier(self.cha)

    def set_type(self, monster_type):
        self.type = monster_type

    def set_cr(self, cr):
        self.target_CR = cr

    def set_size(self, size):
        self.size = size
        df = pd.read_csv("Data/size_hp_chart.csv", index_col=0)
        self.hit_die = df.loc[size, 'Hit Die']
        self.hit_die_type_num = df.loc[size, 'Hit Die number']
        self.hp_avg = df.loc[size, 'Average HP per Die']
        del df

    def name_change(self, name):
        self.name = name

    def set_alignment(self, alignment):
        self.alignment = alignment

    def set_resistance(self, resistance):
        self.resistances = resistance
        self.effective_hp = self.hp_adjust(self.hp)

    def set_immunity(self, immunity):
        self.immunities = immunity
        self.effective_hp = self.hp_adjust(self.hp)

    def set_condition_immunity(self, cond_immunity):
        self.condition_immunity = cond_immunity

    def set_ac(self, ac):
        self.ac = ac
        self.check_flying()

    def check_flying(self):
        df = pd.read_csv('Data/CR_table.csv', index_col=0)
        if self.flying is True and self.target_CR <= 10:
            self.effective_AC = self.ac + 2
            self.AC_CR = int(df['CR as float'].loc[df['Armor Class'] == self.effective_AC].tolist()[0])
        else:
            self.AC_CR = self.ac
        del df

    @staticmethod
    def choose_dmg_die():
        dice = type(None)
        die_choice = input("choose die from d4 to d20 as damage die")
        if die_choice == "d4":
            dice = 4
        if die_choice == "d6":
            dice = 6
        if die_choice == "d8":
            dice = 8
        if die_choice == "d10":
            dice = 10
        if die_choice == "d12":
            dice = 12
        if die_choice == "d20":
            dice = 20

        return dice

    @staticmethod
    def dice_avg(dice):
        return sum(range(1, (dice + 1))) / dice

    def add_attack(self, is_physical=True, use_size=False, special_damage=False, num_of_attacks=1,
                   bonus=False):
        if isinstance(self.average_dmg, dict) is False:
            self.average_dmg = {}
        if is_physical is True:
            damage_source = input("What attribute does the monster use?")
            print(damage_source)
            mod = getattr(self, damage_source[:3] + "_mod")
            dice = self.choose_dmg_die()
            if use_size is False:
                dice_num = int(input("how many dice?"))
            else:
                dice_num = self.weapon_multiplier
            if special_damage is True:
                damage_dice = self.choose_dmg_die()
                special_dice_num = int(input("How many Dice?"))
                added_damage_die = str(special_dice_num) + "d" + str(damage_dice)
                added_damage = special_dice_num * self.dice_avg(damage_dice)
                self.attack_dice[len(self.attack_dice) + 1] = (
                        str(dice_num) + "d" + str(dice) + " + " + str(mod) + " + " + added_damage_die)
                self.average_dmg[len(self.average_dmg) + 1] = (
                        num_of_attacks * (dice_num * self.dice_avg(dice) + mod + added_damage))
            else:
                self.attack_dice[len(self.attack_dice) + 1] = (str(dice_num) + "d" + str(dice) + " + " + str(mod))
                self.average_dmg[len(self.average_dmg) + 1] = (num_of_attacks * (dice_num * self.dice_avg(dice) + mod))
        else:
            damage_dice = self.choose_dmg_die()
            dice_num = int(input("How many Dice?"))
            self.attack_dice[len(self.attack_dice) + 1] = str(dice_num) + "d" + str(damage_dice)
            self.average_dmg[len(self.average_dmg) + 1] = dice_num * damage_dice
        self.assess_damage_cr()

    def assess_damage_cr(self, spellr = False):
        checkpoint = input("Are you finished adding attacks?")
        if checkpoint.lower() == "no" or "n":
            print("Great, add some more attacks!")
            pass
        df_cr = pd.read_csv("Data/CR_table.csv", index_col=0)
        df_cr[["DPR Lower", "DPR Upper"]] = df_cr["Damage/Round"].str.split("-", expand=True).astype(int)
        checkpoint_2 = input("Will the most have varying damage per round?")
        if checkpoint_2.lower() == "no" or "n":
            checkpoint_3 = input("Can the monster use all its attacks in a round?")
            if checkpoint_3.lower() == "yes" or "y":
                total_damage = sum(self.average_dmg.values())
                self.dpr_cr = df_cr.index[
                    (df_cr["DPR Lower"] <= total_damage) & (df_cr["DPR Upper"] >= total_damage)].tolist()[0]
            else:
                print("Choose the most damage the Monster can do a round")
                print(self.attack_dice)
        del df_cr

    def assess_cr(self):
        effective_cr = (self.effective_AC + self.dpr_cr + self.target_CR + self.target_CR) / 4
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
