import argparse
from food_tpk import get_food


def main():
    parser = argparse.ArgumentParser(
        description="Get today's food for Karlsruhe (Joels Cantina)."
    )
    # You can add more arguments here if needed in the future
    _ = parser.parse_args()
    food = get_food()
    print(food)


if __name__ == "__main__":
    main()
