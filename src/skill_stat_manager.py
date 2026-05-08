CHAR_TABLE = {
    'Zan': {
        'Stats': {
            'MP': 5, 'HP': 60, 'Str': 5, 'Atk': 9, 'Def': 7,
            'Mag': 0, 'Spr': 6, 'Acc': 65, 'Spd': 25, 'Evs': 25, 'Lvl': 1
        },

        'Atributes': {
            'Steal': [1, 0],
            'Mug':   [30, 0],
            'Taunt': [15, 0],
            'Cheer': [21, 0],
            'Fire':      [1, 4],
            'Fira':      [15, 10],
            'Firaga':    [30, 20],
            'Blizzard':  [1, 4],
            'Blizzara':  [17, 10],
            'Blizzarga': [35, 20],
            'Thunder':   [1, 4],
            'Thundera':  [18, 10],
            'Thunderga': [40, 20],
            'Attack': [1, 0],
        }
    },
}


def get_stats_for_class(name, level=1):
    base = CHAR_TABLE[name]['Stats']
    final = {}
    for stat, value in base.items():
        if stat == 'Lvl':
            final['Lvl'] = base['Lvl'] + (int(level) - 1)
        else:
            increase = int(value * 0.1 * (int(level) - 1))
            final[stat] = value + increase
    return final


def make_stat_modifier(modifiers):
    def modifier(base_stats):
        result = dict(base_stats)
        for key, amount in modifiers.items():
            result[key] = result.get(key, 0) + amount
        return result
    return modifier


def setup_char_value(characters, target_name=None):
    level_dic = {
        'Stats': {'MP': 0, 'HP': 0, 'Str': 0, 'Atk': 0, 'Def': 0,
                  'Mag': 0, 'Spr': 0, 'Acc': 0, 'Spd': 0, 'Evs': 0}
    }

    while True:
        char = characters
        if target_name:
            name = target_name
            if name not in char:
                print("Character not found.")
                return char
        else:
            name = input('Who are you editing? \n>')
            if name not in char:
                print("Character not found.")
                continue

        clas = char[name]['class']
        choice = input('Do you want to: \n1. Edit single stat\n2. Edit level\n3. Edit attributes\n> ')

        def mult_level():
            new_level = int(input("What is the character Level?\n> "))
            base_stats = CHAR_TABLE[clas]['Stats']
            for stat, value in base_stats.items():
                if stat == 'Lvl':
                    continue
                increase = int(value * 0.1 * (new_level - 1))
                level_dic['Stats'][stat] = increase

            print("\nChecking for new skills...")
            for skill, data in CHAR_TABLE[clas]['Atributes'].items():
                required_level = data[0]
                if new_level >= required_level:
                    print(f"Unlocked: {skill} (requires Lvl {required_level})")

        def edit_attributes():
            print("Current skills:")
            for skill in CHAR_TABLE[clas]['Atributes']:
                print("-", skill)

            action = input("Add or remove?\n> ").lower()
            if action == "add":
                new_skill = input("Skill name?\n> ")
                req = int(input("Required level?\n> "))
                mp = int(input("MP cost?\n> "))
                CHAR_TABLE[clas]['Atributes'][new_skill] = [req, mp]
            elif action == "remove":
                remove_skill = input("Which skill?\n> ")
                if remove_skill in CHAR_TABLE[clas]['Atributes']:
                    del CHAR_TABLE[clas]['Atributes'][remove_skill]

        if choice == "2":
            mult_level()
        elif choice == "3":
            edit_attributes()

        base = CHAR_TABLE[clas]['Stats']
        level_modifier = make_stat_modifier(level_dic['Stats'])
        final_stats = level_modifier(base)
        final_stats['Lvl'] = base['Lvl']

        char[name]['atributtes'] = final_stats

        editing = input("Still editing? (y/n)\n> ").lower()
        if editing != "y":
            break

    return char
