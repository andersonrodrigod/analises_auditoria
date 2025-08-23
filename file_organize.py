import pandas as pd
import glob

arquivos = glob.glob("data/*.xlsx")

df_list = []

for arquivo in arquivos:
    df = pd.read_excel(arquivo)
    df_list.append(df)

df_final = pd.concat(df_list, ignore_index=False)


df_final.to_excel("dados_unificados.xlsx", index=False)











































