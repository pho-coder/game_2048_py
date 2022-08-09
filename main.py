from game_manager import GameManager


def main():
    print("2048")
    gm = GameManager(4)
    gm.setup()
    while not gm.over and not gm.won:
        gm.run()


if __name__ == "__main__":
    main()