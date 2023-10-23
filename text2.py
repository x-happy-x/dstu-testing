from app.parser import gift

with open("./вопhhhhhhhhhhросы-ИТ в отрасли-top-20230518-1818.txt", "r", encoding="utf-8") as f:
    text = f.read()
    print(text)

g = gift.parse(text)
print(g)