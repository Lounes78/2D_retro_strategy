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

- **Implemented:**
  - Fire vs Water: Damage halved, burn duration -2 ✅

- **To be implemented:**
  - Water vs Fire: Damage x2  
  - Water vs Ice: Heals Ice-type  
  - Water vs Thunder: Damage halved  
  - Fire vs Ice: Damage x2.5, burn duration +1  
  - Ice vs Ice: No freezing effect  
  - Ice vs Water: Damage x1.5, freeze duration +3  
  - Thunder vs Water: Paralysis duration +2  
  - Thunder vs Fire: Damage x0.75  