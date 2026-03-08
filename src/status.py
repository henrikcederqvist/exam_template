def print_status(game_grid, score, grace_steps):
    """
    Skriver ut spelvärlden, spelarens poäng och status för grace period.
    Anropas i början av varje tur.
    """
    print("--------------------------------------")
    print(f"You have {score} points.")
    #print(f"DEBUG: picked_items = {picked_items} / {total_items}")

    if grace_steps > 0:
        print(f"Grace period: {grace_steps} free steps left.")
    else:
        print("Grace period: inactive")

    print(game_grid)