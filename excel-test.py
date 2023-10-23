import pandas as pd

excel = pd.ExcelFile("./file.xlsx")

df = excel.parse(excel.sheet_names[0])

scores = df['Баллы']
subjects = df['Дисциплина']
names = df['Фамилия'] + " " + df['Имя'] + " " + df['Отчество']

data = {
    k: {} for k in subjects
}

for i in range(len(names)):
    data[subjects[i]][names[i]] = scores[i]

df_out = pd.DataFrame(data)

writer = pd.ExcelWriter('file2.xlsx', engine='xlsxwriter')
df_out.to_excel(writer, 'Sheet')
writer.close()
