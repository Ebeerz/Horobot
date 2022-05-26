import config
while True:
    text = input()
    if text in config.SIGNS:
        print("Да")
    else:
        print("Нет")

