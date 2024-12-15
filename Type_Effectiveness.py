# Define the attribute interaction table
# Each element type interacts with others based on specific multipliers and effects:
# - "damage_multiplier": Adjusts the base damage (e.g., 2 for double damage, 0.5 for half damage)
# - "heal": Allows healing instead of damage (used in specific interactions) Achieved by inflicting negative damage.
# - "burn": Adjusts the burn duration (e.g., -2 to reduce burn turns)
# - "freeze": Adds freeze duration
# - "paralyze": Adds paralysis duration

ATTRIBUTE_EFFECTS = {
    "Water": {
        "Fire": {"damage_multiplier": 2 , "slow" : 2}, # Water deals double damage to Fire
        "Ice": {"heal": -50, "slow" : 1},             # Water heals Ice instead of damaging it
        "Thunder": {"damage_multiplier": 0.75, "slow" : -2}, # Water deals half damage to Thunder
    },
    "Fire": {
        "Ice": {"damage_multiplier": 2.5, "burn": 3}, # Fire deals 2.5x damage to Ice and adds 3 turns of burn
        "Water": {"damage_multiplier": 0.5, "burn": -2}, # Fire deals half damage to Water and reduces burn by 2 turns
    },
    "Ice": {
        "Water": {"damage_multiplier": 1.5, "freeze": 2}, # Ice deals 1.5x damage to Water and adds 2 turns of freeze
        "Thunder": {"damage_multiplier": 1.5}, # Ice deals 1.5x damage to Thunder
        "Fire": {"damage_multiplier": 0.5}, # Ice deals half damage to Fire
    },
    "Thunder": {
        "Water": {"damage_multiplier": 1.5, "paralyze": 2}, # Thunder deals double damage to Water and adds 2 turns of paralysis
    }
}

# Function to calculate damage and status effects based on attacker and target attributes
def calculate_damage_and_effect(attacker, target, base_damage,burn=0,freeze=0,paralyze=0,slow=0):
    # Get the element types of the attacker and target
    attacker_type = getattr(attacker, "element_type", None)
    target_type = getattr(target, "element_type", None)

    # Default: No adjustments to damage or effects
    damage = base_damage
    # Check attribute interactions and apply effects if both types are defined
    if attacker_type and target_type:
        effects = ATTRIBUTE_EFFECTS.get(attacker_type, {}).get(target_type, {})
        damage *= effects.get("damage_multiplier", 1)
        damage += effects.get("heal", 0)
        #heal += effects.get("heal", 0)
        burn += effects.get("burn", 0)
        freeze += effects.get("freeze", 0)
        paralyze += effects.get("paralyze", 0)
        slow += effects.get("slow", 0)

        # Ensure durations are not negative
        burn = max(0, burn)
        freeze = max(0, freeze)
        paralyze = max(0, paralyze)

    return damage, burn, freeze, paralyze,slow