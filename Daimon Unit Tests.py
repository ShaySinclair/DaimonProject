import Daimon

Daimon.load_all_data()

def test_update_player_money():
    print("\n=== TEST update_player_money ===")

    # Get Player
    player = Daimon.get_player_by_id(1)

    # Reset Player money to 0.
    player.player_money = 0
    print(f"\nPlayer starts with ${player.player_money} (expected: $0)")
    if player.player_money == 0:
        print(f"SUCCESS. Actual: ${player.player_money}")
    else:
        print(f"FAILURE. Actual: ${player.player_money}")

    print("\nPlayer adds $1,000,000 (expected: $1,000,000)")
    player.update_player_money(1000000)
    if player.player_money == 1000000:
        print(f"SUCCESS. Actual: ${player.player_money}")
    else:
        print(f"FAILURE. Actual: ${player.player_money}")

    print("\nPlayer subtracts $200 (expected: $999,800)")
    player.update_player_money(-200)
    if player.player_money == 999800:
        print(f"SUCCESS. Actual: ${player.player_money}")
    else:
        print(f"FAILURE. Actual: ${player.player_money}")

    print("\nPlayer pays $999,800 (expected: $999,800)")
    player.update_player_money(-999800)
    if player.player_money == 0:
        print(f"SUCCESS. Actual: ${player.player_money}")
    else:
        print(f"FAILURE. Actual: ${player.player_money}")

    print("\nPlayer pays $30 (expected: $0)")
    player.update_player_money(-30)
    if player.player_money == 0:
        print(f"SUCCESS. Actual: ${player.player_money}")
    else:
        print(f"FAILURE. Actual: ${player.player_money}")

def test_update_npc_money():
    print("\n=== TEST update_npc_money ===")

    # Get Player
    npc = Daimon.get_npc_by_id(1)

    # Reset Player money to 0.
    npc.npc_money = 0
    print(f"\nPlayer starts with ${npc.npc_money} (expected: $0)")
    if npc.npc_money == 0:
        print(f"SUCCESS. Actual: ${npc.npc_money}")
    else:
        print(f"FAILURE. Actual: ${npc.npc_money}")

    print("\nPlayer adds $1,000,000 (expected: $1,000,000)")
    npc.update_npc_money(1000000)
    if npc.npc_money == 1000000:
        print(f"SUCCESS. Actual: ${npc.npc_money}")
    else:
        print(f"FAILURE. Actual: ${npc.npc_money}")

    print("\nPlayer subtracts $200 (expected: $999,800)")
    npc.update_npc_money(-200)
    if npc.npc_money == 999800:
        print(f"SUCCESS. Actual: ${npc.npc_money}")
    else:
        print(f"FAILURE. Actual: ${npc.npc_money}")

    print("\nPlayer pays $999,800 (expected: $999,800)")
    npc.update_npc_money(-999800)
    if npc.npc_money == 0:
        print(f"SUCCESS. Actual: ${npc.npc_money}")
    else:
        print(f"FAILURE. Actual: ${npc.npc_money}")

    print("\nPlayer pays $30 (expected: $0)")
    npc.update_npc_money(-30)
    if npc.npc_money == 0:
        print(f"SUCCESS. Actual: ${npc.npc_money}")
    else:
        print(f"FAILURE. Actual: ${npc.npc_money}")

def test_update_player_generic_item():
    # Get Player
    player = Daimon.get_player_by_id(1)
    print(f"PLAYER LOCATION {player.player_location}")

    print("\n=== TEST add_item_to_player_inventory and subtract_item_from_player_inventory  ===")
    random_generic = Daimon.generate_random_item_generic(player)
    print(f"RANDOMINGO GENERICO {random_generic}")
    if random_generic:
        random_generic.item_quantity = 5
        print(f"Generated random generic item '{random_generic.item_name}' with quantity 5 (expected: 5)")

        print("Player picks up 5 of the random generic item (expected: quantity = 5)")
        player.add_item_to_player_item_inventory(random_generic)

        print("Player loses 1 of the generic item (expected: quantity = 4)")
        player.subtract_item_from_player_item_inventory(random_generic, 1)

        print("Player loses 5 of the generic item (expected: fail, only 4 remaining)")
        player.subtract_item_from_player_item_inventory(random_generic, 5)

def test_update_player_unique_item():
    # Get Player
    player = Daimon.get_player_by_id(1)

    print("\n-- UNIQUE ITEM OPERATIONS --")
    random_unique = Daimon.generate_random_item_unique(player)
    if random_unique:
        random_unique.item_quantity = 5
        print(f"Generated random unique item '{random_unique.item_name}' with quantity 5 (expected: 5)")

        print("Player picks up 5 of the random unique item (expected: all 5 added individually)")
        for _ in range(5):
            player.add_item_to_player_item_inventory(random_unique)

        print("Player loses 1 of the unique item (expected: 1 removed)")
        player.subtract_item_from_player_item_inventory(random_unique, 1)

        print("Player loses 5 of the unique item (expected: 4 remaining, fail if try to remove 5)")
        player.subtract_item_from_player_item_inventory(random_unique, 5)

def test_daimon_operations_player():
    # Get Player
    player = Daimon.get_player_by_id(1)
    location = Daimon.get_location_by_id(8)

    print("\n-- DAIMON OPERATIONS --")
    random_daimon_1 = Daimon.generate_random_daimon_unbonded(location)
    if random_daimon_1:
        print(f"Generated random unbonded Daimon '{random_daimon_1.daimon_unbonded_species}'")
        player.catch_daimon_unbonded(random_daimon_1)
        print(f"Player catches Daimon (expected: added to team)")

        print("Player sets follower (expected: success)")
        player.player_daimon_inventory.set_follower(random_daimon_1)

        print("Player removes follower (expected: success)")
        player.player_daimon_inventory.remove_follower()

        print("Player removes follower again (expected: fail, no follower)")
        player.player_daimon_inventory.remove_follower()

        print("Player sets follower again (expected: success)")
        player.player_daimon_inventory.set_follower(random_daimon_1)

        print("Player nicknames caught Daimon (expected: nickname set)")
        player.player_daimon_inventory.set_daimon_nickname(random_daimon_1.daimon_unbonded_id, "Flare")

    random_daimon_2 = Daimon.generate_random_daimon_unbonded(location)
    if random_daimon_2:
        print(f"\nGenerated another random unbonded Daimon '{random_daimon_2.daimon_unbonded_species}'")
        player.catch_daimon_unbonded(random_daimon_2)

        print("Move Daimon from team to storage (expected: moved)")
        player.player_daimon_inventory.move_daimon_to_storage_from_team(random_daimon_2)

        print("Move Daimon from storage back to team (expected: moved)")
        player.player_daimon_inventory.move_daimon_to_team_from_storage(random_daimon_2)

        print("Move Daimon to storage again (expected: moved)")
        player.player_daimon_inventory.move_daimon_to_storage_from_team(random_daimon_2)

        if player.player_daimon_inventory.player_daimon_inventory_team:
            print("Switch Daimon in team with storage (expected: swap successful)")
            player.player_daimon_inventory.switch_daimon_in_team_and_storage(
                player.player_daimon_inventory.player_daimon_inventory_team[0],
                player.player_daimon_inventory.player_daimon_inventory_storage[0]
            )

        print("Get all Daimons (expected: list of all caught Daimons)")
        all_daimons = player.player_daimon_inventory.get_all_daimons()
        print(f"Actual: {[d.daimon_bonded_species for d in all_daimons]}")

        print("Get index of first Daimon in team (expected: index 0)")
        index = player.player_daimon_inventory.get_daimon_index_in_team(player.player_daimon_inventory.player_daimon_inventory_team[0])
        print(f"Actual: {index}")

    print("\n✅ TEST CASE COMPLETED")

def test_player_daimon_catch():
    # ============================================
    # Daimon Encounter + Catch Test
    # ============================================
    print("\n=== Daimon Encounter + Catch Test ===")
    player = Daimon.get_player_by_id(1)
    location = player.player_location

    # --- Generate first unbonded Daimon ---
    wild_daimon = Daimon.generate_random_daimon_unbonded(location)

    if len(Daimon.daimon_unbonded_global) > 0:
        wild_daimon = Daimon.daimon_unbonded_global[-1]

        print("\n✅ Wild Daimon Spawned:")
        for attr, value in vars(wild_daimon).items():
            print(f"  {attr}: {value}")

        # --- PLAYER CATCH TEST ---
        print("\n🎯 Testing catch with Player...")
        player.catch_daimon_unbonded(wild_daimon)

        print("\nPlayer Daimon Inventory:")
        print("Team:")
        for daimon in player.player_daimon_inventory.player_daimon_inventory_team:
            print(f"  {daimon.daimon_bonded_species} (Level {daimon.daimon_bonded_level})")
        print("Storage:")
        for daimon in player.player_daimon_inventory.player_daimon_inventory_storage:
            print(f"  {daimon.daimon_bonded_species} (Level {daimon.daimon_bonded_level})")
    else:
        print("⚠️ No Daimon spawned for Player test.")

def test_npc_daimon_catch():
    # ============================================
    # Daimon Encounter + Catch Test
    # ============================================
    print("\n=== Daimon Encounter + Catch Test ===")
    npc = Daimon.get_npc_by_id(1)
    location = npc.npc_location

    # --- Generate first unbonded Daimon ---
    Daimon.generate_random_daimon_unbonded(location)

    if len(Daimon.daimon_unbonded_global) > 0:
        wild_daimon = Daimon.daimon_unbonded_global[-1]

        print("\n✅ Wild Daimon Spawned:")
        for attr, value in vars(wild_daimon).items():
            print(f"  {attr}: {value}")

        # --- NPC CATCH TEST ---
        print("\n🎯 Testing catch with NPC...")
        npc.catch_daimon_unbonded(wild_daimon)

        print("\nNPC Daimon Inventory:")
        print("Team:")
        for daimon in npc.npc_daimon_inventory.npc_daimon_inventory_team:
            print(f"  {daimon.daimon_bonded_species} (Level {daimon.daimon_bonded_level})")
        print("Storage:")
        for daimon in npc.npc_daimon_inventory.npc_daimon_inventory_storage:
            print(f"  {daimon.daimon_bonded_species} (Level {daimon.daimon_bonded_level})")
    else:
        print("⚠️ No Daimon spawned for NPC test.")

def test_add_random_side_quest_to_player():
    """
    Test: Generate a random QuestSide and assign it to a Player's side quest inventory.
    """
    # 1️⃣ Get or create a test player
    player = Daimon.player_global[0]

    # 2️⃣ Generate a random QuestSide
    quest_side = Daimon.generate_random_quest_side()
    print(f"🎲 Generated QuestSide: {quest_side.quest_side_name}")

    # 3️⃣ Add the quest to the player's side quest inventory
    success = player.add_quest_side_to_player_quest_side_inventory(quest_side)
    if success:
        print(f"✅ {quest_side.quest_side_name} added to {player.player_name}'s inventory.")
    else:
        print(f"⚠️ Failed to add {quest_side.quest_side_name} (duplicate or error).")

    # 4️⃣ Display player’s updated side quest inventory
    print("\n📜 Current Side Quests for Player:")
    for q in player.player_quest_side_inventory.player_quest_side_inventory_storage:
        print(f"   • {q.quest_side_name} (ID: {q.quest_side_id}, Status: {q.quest_side_status})")

    # 5️⃣ Confirm quest removed from global pool
    if quest_side not in Daimon.quest_side_global:
        print("🗑️ Quest successfully removed from global pool.")
    else:
        print("⚠️ Quest still exists in global pool (check logic).")





def test_full_inventory_and_daimon_operations():
    print("\n=== PLAYER INVENTORY, MONEY, AND DAIMON EDGE CASE TEST ===")

    # Get player and location
    player = Daimon.get_player_by_id(1)
    location = Daimon.get_location_by_id(8)

    # MONEY OPERATIONS
    # Reset player money to 0
    player.player_money = 0
    print(f"\nPlayer starts with ${player.player_money} (expected: $0)")

    print("\n-- MONEY OPERATIONS --")
    print("Player picks up $1,000,000 (expected: $1,000,000)")
    player.update_player_money(1000000)
    print(f"Actual: ${player.player_money}")

    print("Player pays $200 (expected: $999,800)")
    player.update_player_money(-200)
    print(f"Actual: ${player.player_money}")

    print("Player pays $50 (expected: $999,750)")
    player.update_player_money(50)
    print(f"Actual: ${player.player_money}")

    # GENERIC ITEM OPERATIONS
    print("\n-- GENERIC ITEM OPERATIONS --")
    random_generic = Daimon.generate_random_item_generic(player)
    print(f"RANDOMINGO GENERICO {random_generic}")
    if random_generic:
        random_generic.item_quantity = 5
        print(f"Generated random generic item '{random_generic.item_name}' with quantity 5 (expected: 5)")

        print("Player picks up 5 of the random generic item (expected: quantity = 5)")
        player.add_item_to_player_item_inventory(random_generic)

        print("Player loses 1 of the generic item (expected: quantity = 4)")
        player.subtract_item_from_player_item_inventory(random_generic, 1)

        print("Player loses 5 of the generic item (expected: fail, only 4 remaining)")
        player.subtract_item_from_player_item_inventory(random_generic, 5)

    # UNIQUE ITEM OPERATIONS
    print("\n-- UNIQUE ITEM OPERATIONS --")
    random_unique = Daimon.generate_random_item_unique(player)
    if random_unique:
        random_unique.item_quantity = 5
        print(f"Generated random unique item '{random_unique.item_name}' with quantity 5 (expected: 5)")

        print("Player picks up 5 of the random unique item (expected: all 5 added individually)")
        for _ in range(5):
            player.add_item_to_player_item_inventory(random_unique)

        print("Player loses 1 of the unique item (expected: 1 removed)")
        player.subtract_item_from_player_item_inventory(random_unique, 1)

        print("Player loses 5 of the unique item (expected: 4 remaining, fail if try to remove 5)")
        player.subtract_item_from_player_item_inventory(random_unique, 5)

    # DAIMON OPERATIONS
    print("\n-- DAIMON OPERATIONS --")
    random_daimon_1 = Daimon.generate_random_daimon_unbonded(location)
    if random_daimon_1:
        print(f"Generated random unbonded Daimon '{random_daimon_1.daimon_unbonded_species}'")
        player.catch_daimon_unbonded(random_daimon_1)
        print(f"Player catches Daimon (expected: added to team)")

        print("Player sets follower (expected: success)")
        player.player_daimon_inventory.set_follower(random_daimon_1)

        print("Player removes follower (expected: success)")
        player.player_daimon_inventory.remove_follower()

        print("Player removes follower again (expected: fail, no follower)")
        player.player_daimon_inventory.remove_follower()

        print("Player sets follower again (expected: success)")
        player.player_daimon_inventory.set_follower(random_daimon_1)

        print("Player nicknames caught Daimon (expected: nickname set)")
        player.player_daimon_inventory.set_daimon_nickname(random_daimon_1.daimon_unbonded_id, "Flare")

    random_daimon_2 = Daimon.generate_random_daimon_unbonded(location)
    if random_daimon_2:
        print(f"\nGenerated another random unbonded Daimon '{random_daimon_2.daimon_unbonded_species}'")
        player.catch_daimon_unbonded(random_daimon_2)

        print("Move Daimon from team to storage (expected: moved)")
        player.player_daimon_inventory.move_daimon_to_storage_from_team(random_daimon_2)

        print("Move Daimon from storage back to team (expected: moved)")
        player.player_daimon_inventory.move_daimon_to_team_from_storage(random_daimon_2)

        print("Move Daimon to storage again (expected: moved)")
        player.player_daimon_inventory.move_daimon_to_storage_from_team(random_daimon_2)

        if player.player_daimon_inventory.player_daimon_inventory_team:
            print("Switch Daimon in team with storage (expected: swap successful)")
            player.player_daimon_inventory.switch_daimon_in_team_and_storage(
                player.player_daimon_inventory.player_daimon_inventory_team[0],
                player.player_daimon_inventory.player_daimon_inventory_storage[0]
            )

        print("Get all Daimons (expected: list of all caught Daimons)")
        all_daimons = player.player_daimon_inventory.get_all_daimons()
        print(f"Actual: {[d.daimon_bonded_species for d in all_daimons]}")

        print("Get index of first Daimon in team (expected: index 0)")
        index = player.player_daimon_inventory.get_daimon_index_in_team(player.player_daimon_inventory.player_daimon_inventory_team[0])
        print(f"Actual: {index}")

    print("\n✅ TEST CASE COMPLETED")

def test_player_vs_npc_battle():
    """
    Exhaustive test case:
    - Load Player (ID 1)
    - Load NPC (ID 1)
    - Initialize SystemDaimonBattle
    - Run a simulated battle loop
    """

    # --------------------------------------------------------
    # 1️⃣ Load participants
    # --------------------------------------------------------
    player = Daimon.get_player_by_id(1)
    npc = Daimon.get_npc_by_id(1)

    if not player or not npc:
        print("❌ Player or NPC not found. Check your database or init functions.")
        return

    print(f"✅ Loaded Player: {player.player_name}")
    print(f"✅ Loaded NPC: {npc.npc_name}")

    # --------------------------------------------------------
    # 2️⃣ Create the battle
    # --------------------------------------------------------
    battle = Daimon.SystemDaimonBattle(
        system_daimon_battle_id=Daimon.random.randint(1, 9999),
        system_daimon_battle_side_a=[player],
        system_daimon_battle_side_b=[npc],
    )

    # --------------------------------------------------------
    # 3️⃣ Initialize battle (set active Daimons + turn order)
    # --------------------------------------------------------
    print("\n🚀 Initializing battle...")
    battle.initialize_battle()

    print("\n🎯 Turn order:")
    for d in battle.system_daimon_turn_order:
        daimon_nickname = getattr(d, "daimon_bonded_nickname", getattr(d, "daimon_unbonded_name", "Unknown"))
        daimon_speed = getattr(d, "daimon_bonded_stat_speed", getattr(d, "daimon_unbonded_stat_speed", "?"))

        # Check each participant to see who owns this Daimon
        for participant in battle.system_daimon_battle_side_a + battle.system_daimon_battle_side_b:
            active_daimons = battle._extract_daimons(participant)

            if d in active_daimons:
                if hasattr(participant, "player_name"):
                    owner_name = participant.player_name
                elif hasattr(participant, "npc_name"):
                    owner_name = participant.npc_name
                else:
                    owner_name = "Wild"
                break  # Stop checking after finding the owner

        # Print the turn order entry
        print(f" - {daimon_nickname} ({owner_name}) (Speed: {daimon_speed})")

    # --------------------------------------------------------
    # 4️⃣ Battle loop
    # --------------------------------------------------------
    print("\n🔥 Battle begins! 🔥")
    round_count = 1
    while True:
        print(f"""
            ============================)
            🕓 ROUND {round_count}")
            ============================
            """)

        # Run one turn per daimon in the turn order
        for _ in range(len(battle.system_daimon_turn_order)):
            battle.next_turn()
            Daimon.time.sleep(1.0)

        # TODO: implement faint/death checks once HP mechanics exist
        # For now, just limit to 3 rounds for demo
        round_count += 1
        if round_count > 3:
            print("\n⏹️ Battle test complete after 3 rounds.")
            break

    # --------------------------------------------------------
    # 5️⃣ Print battle log
    # --------------------------------------------------------
    print("\n📜 Battle Log:")
    for log in battle.battle_log:
        print(" -", log)

def test_player_vs_wild_daimon_battle():
    """Simulate a battle between the Player and a wild Daimon."""
    
    player = Daimon.get_player_by_id(1)
    location = player.player_location

    # --------------------------------------------------
    # GENERATE WILD DAIMON
    # --------------------------------------------------
    wild_daimon = Daimon.generate_random_daimon_unbonded(location)
    print(f"🌿 A wild Lv.{wild_daimon.daimon_unbonded_level} {wild_daimon.daimon_unbonded_species} appeared!")

    # --------------------------------------------------
    # SET UP BATTLE
    # --------------------------------------------------
    battle = Daimon.SystemDaimonBattle(
        system_daimon_battle_id=2,
        system_daimon_battle_side_a=[player],
        system_daimon_battle_side_b=[wild_daimon],
    )

    # Initialize and run the full automated battle
    battle.initialize_battle()
    battle.run_full_battle()

    print("\n🏁 Wild battle complete!")







#test_update_player_money()
#test_update_npc_money()
test_update_player_generic_item()