# TO DO

--- Limiter un mouvement à un carreau par tour  ✅

--- remove the Unit class ✅

--- add health barre ✅

--- basic attacks mechanics ✅

--- Details about the attacks etc

--- Update current_unit_index when a unit gets eleminated ✅

--- attack animations

--- domination process

--- Bug a corriger (ou pas, on peut fermer les yeux): lorsque on move une fois avec un peros puis on change de perso. 
Les highlighted tiles se comportent mal

--- N'arrive pas (ou plus ?) à lancer une attaque si on a deja bougé


--- debuff system :
- **Burning**: Take small damage over time.✅
- **Frozen**: Cannot move or attack.  ✅
- **Paralysis**: probable inability to move

--- All statements outputting monsters' position information (e.g., `print(f"Monster {self.name} moving from {self.mapPosition} to [{new_row}, {new_col}]")`) have been commented out to ensure that the debugging process remains clear and easy to read.


### Attribute Resistance System
| **Element** | **Strong Against** | **Weak Against** | **Damage Multiplier** | **Special Effect**                                                              |
|-------------|--------------------|------------------|-----------------------|---------------------------------------------------------------------------------|
| **Water**   | Fire               | Thunder          | Fire x2               | Against Ice: Heal (dmg -50, when it's negative will heal the target), no damage |
| **Fire**    | Ice                | Water            | Ice x2.5              | Causes Burn on target                                                           |
| **Ice**     | Thunder, Water     | Fire             | Thunder, Water x1.5   | Causes Freeze on target                                                         |
| **Thunder** | Water              | Ice              | Water x2              | Causes Paralysis on target                                                      |

