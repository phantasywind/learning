import random


def main() -> None:
    target = random.randint(1, 100)
    attempts = 0

    while True:
        raw = input("请输入 1~100 的整数：").strip()
        try:
            guess = int(raw)
        except ValueError:
            print("请输入有效的整数。")
            continue

        attempts += 1
        if guess < target:
            print("太小")
        elif guess > target:
            print("太大")
        else:
            print(f"猜对了！一共猜了 {attempts} 次。")
            break


if __name__ == "__main__":
    main()
