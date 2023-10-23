import numpy as np
with open("Z:/Desktop/Мобильные приложения2.txt", "r", encoding='utf-8') as f:
    txt = f.read()

lines = txt.split("\n\n")
print(len(lines))
indexes = [10, 15, 16, 20, 17, 21, 24, 25, 18, 23, 12, 13, 14, 11, 22, 9, 1, 2, 3, 4, 5, 6, 7, 8, 19]
for i in range(len(indexes)):
    indexes[i] -= 1
array = np.array(lines)
text = "\n\n".join(array[indexes])
with open("Z:/Desktop/Мобильные приложения4.txt", "w", encoding='utf-8') as f:
    f.write(text)