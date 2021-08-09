# This code with create the data needed for building monster for DnD 5th Edition.

# Import necessary packages
import numpy as np
import pandas as pd
import os

# Change Working directory for ease of access
os.chdir(os.path.split(os.getcwd())[0])

# Damage Resistances
Damage = np.array(['Acid', 'Bludgeoning', 'Cold', 'Fire', 'Force', 'Lightning', 'Necrotic', 'Piercing', 'Poison',
                   'Psychic', 'Radiant', 'Slashing', 'Thunder'])
np.save('Data/Damage_types.npy', Damage)

# Condition Immunities
Cond_im = np.array(['Blinded', 'Charmed', 'Deafened', 'Frightened', 'Grappled', 'Paralyzed', 'Poisoned', 'Prone',
                    'Restrained'])
np.save('Data/condition_imms.npy', Cond_im)

# Type of monster
type = np.array(['Aberration', 'Beast', 'Celestial', 'Construct', 'Dragon', 'Elemental', 'Fey', 'Fiend', 'Giant',
                 'Humanoid', 'Monstrosity', 'Ooze', 'Plant', 'Undead'])
np.save('Data/monster_type.npy', type)

# Alignment, including unaligned if it doesn't matter
alignment = np.array(["Chaotic Evil", "Chaotic Good", "Chaotic Neutral", "Lawful Evil", "Lawful Good", "Lawful Neutral",
                      "Neutral Evil", "Neutral Good", "True Neutral", "Unaligned"])
np.save("Data/alignment.npy", alignment)

# Size and Hit die
data = {"Monster Size": ['Tiny', 'Small', 'Medium', 'Large', 'Huge', 'Gargantuan'],
        "Size dice multiplier": [1, 1, 1, 2, 3, 4],
        "Hit Die": ['d4', 'd6', 'd8', 'd10', 'd12', 'd20'],
        "Hit Die number": [4, 6, 8, 10, 12, 20],
        "Average HP per Die": [2.5, 3.5, 4.5, 5.5, 6.5, 10.5]}
size_hp_df = pd.DataFrame(data)
size_hp_df.set_index('Monster Size', inplace=True)
size_hp_df.to_csv("Data/size_hp_chart.csv")

# Effective Hit Points
cr_range = [*range(1, 18, 1)]
res_multi = [2] * 4 + [1.5] * 6 + [1.25] * 6 + [1]
imm_multi = [2] * 10 + [1.5] * 6 + [1.25]
data = {'Expected Challenge Rating': cr_range, 'HP Multiplier by Resistances': res_multi,
        "HP Multiplier for Immunities": imm_multi}
effective_hp = pd.DataFrame(data)
effective_hp.set_index('Expected Challenge Rating', inplace=True)
effective_hp.to_csv("Data/effective_hp_calc.csv")

# Attacks and damage types
attack_types = {"weapons": {
    "slashing": {
        "Handaxe": "d6",
        "Sickle": "d4",
        "Battleaxe": {
            "one-handed": "d8",
            "two-handed": "d10"
        },
        "Glaive": ["d10", "+5ft"],
        "Greataxe": "d12",
        "Greatsword": "2d6",
        "Halberd": ["d10", "+5ft"],
        "Longsword": {
            "one-handed": "d8",
            "two-handed": "d10"
        },
        "Scimitar": "d6",
        "Shortsword": "d6",
        "Whip": ["d4", "+5ft"]
    },
    "piercing": {
        "dagger": "d4",

    }
}
                }