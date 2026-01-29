import random

player = {"name": "ゆうしゃ", "hp": 100, "max_hp": 100, "mp": 30, "atk": 20, "defense": False, "level": 1}
heal_amount = 50
enemies = [
    {"name": "スライム", "hp": 50, "atk": 10, "magic": False},
    {"name": "スライムナイト", "hp": 100, "atk": 20, "magic": True, "magic_atk": 25},
    {"name": "メタルスライム", "hp": 3, "atk": 18, "fast": True, "magic_resist": True},
    {"name": "キラーパンサー", "hp": 220, "atk": 45, "sometimes_fast": True, "weak_defense": True},
]
enemy = None
items = {"やくそう": 3}

def show_status():
    print(f"\n【{player['name']}】HP: {player['hp']}/{player['max_hp']}  MP: {player['mp']}  やくそう: {items['やくそう']}個")
    print(f"【{enemy['name']}】HP: {enemy['hp']}")

def player_turn():
    print("\n1:たたかう  2:まほう  3:ぼうぎょ  4:アイテム  5:にげる")
    choice = input("▶ ").replace("１","1").replace("２","2").replace("３","3").replace("４","4").replace("５","5")
    player["defense"] = False
    if choice == "1":
        print(f"\n{player['name']}のこうげき！")
        if enemy.get("magic_resist"):
            dmg = 1
        else:
            dmg = random.randint(15, 25)
            if enemy.get("weak_defense"):
                dmg = dmg * 2
        enemy["hp"] -= dmg
        print(f"→ {dmg}のダメージ！")
    elif choice == "2" and player["mp"] >= 10:
        if player["level"] >= 2:
            print(f"\n{player['name']}はメラゾーマをとなえた！")
            player["mp"] -= 10
            if enemy.get("magic_resist"):
                print("→ しかしまほうはきかなかった！")
            else:
                dmg = random.randint(64, 80)
                enemy["hp"] -= dmg
                print(f"→ {dmg}のダメージ！")
        else:
            print(f"\n{player['name']}はメラをとなえた！")
            player["mp"] -= 10
            if enemy.get("magic_resist"):
                print("→ しかしまほうはきかなかった！")
            else:
                dmg = random.randint(30, 40)
                enemy["hp"] -= dmg
                print(f"→ {dmg}のダメージ！")
    elif choice == "2":
        print("→ MPがたりない！")
    elif choice == "3":
        print(f"\n{player['name']}はみをまもっている！")
        player["defense"] = True
    elif choice == "4":
        if items["やくそう"] > 0:
            items["やくそう"] -= 1
            player["hp"] = min(player["hp"] + heal_amount, player["max_hp"])
            print(f"\n{player['name']}はやくそうをつかった！")
            print(f"→ HPが{heal_amount}かいふくした！")
        else:
            print("→ やくそうがない！")
    elif choice == "5":
        if random.random() < 0.5:
            return "escape"
        print("→ にげられなかった！")

def enemy_turn():
    if enemy["hp"] > 0:
        # 魔法を使える敵は50%の確率で魔法攻撃
        if enemy.get("magic") and random.random() < 0.5:
            dmg = random.randint(enemy["magic_atk"] - 5, enemy["magic_atk"] + 5)
            player["hp"] -= dmg
            print(f"\n{enemy['name']}はギラをとなえた！")
            print(f"→ {dmg}のダメージ！")
        else:
            base_dmg = random.randint(enemy["atk"] - 4, enemy["atk"] + 3)
            dmg = base_dmg // (2 if player["defense"] else 1)
            player["hp"] -= dmg
            print(f"\n{enemy['name']}のこうげき！")
            print(f"→ {dmg}のダメージ！")

for i, e in enumerate(enemies):
    enemy = e
    print(f"\n{enemy['name']}が あらわれた！")

    turn_count = 0
    while player["hp"] > 0 and enemy["hp"] > 0:
        turn_count += 1
        show_status()
        # 素早い敵は先に攻撃
        # sometimes_fastは3回に1回先制
        enemy_first = enemy.get("fast") or (enemy.get("sometimes_fast") and turn_count % 3 == 0)
        if enemy_first:
            if enemy.get("sometimes_fast") and turn_count % 3 == 0:
                print(f"\n{enemy['name']}はすばやくうごいた！")
            enemy_turn()
            if player["hp"] <= 0:
                break
            if player_turn() == "escape":
                print("にげだした！")
                break
        else:
            if player_turn() == "escape":
                print("にげだした！")
                break
            enemy_turn()

    if player["hp"] <= 0:
        print("\n負けた...")
        break
    elif enemy["hp"] <= 0:
        print(f"\n{enemy['name']}をたおした！")
        # メタルスライムを倒したらレベルアップ
        if enemy["name"] == "メタルスライム":
            player["level"] = 2
            player["max_hp"] = int(player["max_hp"] * 1.5)
            player["atk"] = player["atk"] * 2
            player["hp"] = player["max_hp"]
            player["mp"] = 50
            items["やくそう"] += 2
            heal_amount = 100
            print("\n★ レベルアップ！ ★")
            print(f"→ さいだいHPが{player['max_hp']}になった！")
            print(f"→ こうげき力が{player['atk']}になった！")
            print("→ HP・MPがかんぜんかいふくした！")
            print("→ メラがメラゾーマにしんかした！")
            print("→ やくそうを2つてにいれた！")
            print("→ やくそうの回復量が100になった！")
        if i < len(enemies) - 1:
            print("\nしかし、あたらしいてきがあらわれた！")
else:
    if player["hp"] > 0 and enemy["hp"] <= 0:
        print("\nすべてのてきをたおした！ゆうしゃのしょうり！")
