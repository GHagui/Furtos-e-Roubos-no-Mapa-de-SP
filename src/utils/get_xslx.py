import pandas as pd

def read_xlsx(data):
    roubos_outros = data[data["Natureza"] == "ROUBO - OUTROS"]["Total"].values[0]
    furtos_outros = data[data["Natureza"] == "FURTO - OUTROS"]["Total"].values[0]
    return roubos_outros, furtos_outros

def open_xlsx(file_path):
    file_path = "src/DP-2023/" + file_path
    data = pd.read_excel(file_path, thousands='.', decimal=',')
    return data

def get_data(zip_bairros):
    zip_bairros_data = []
    for file in zip_bairros:
        data = open_xlsx(file[0])
        roubos, furtos = read_xlsx(data)
        zip_bairros_data.append((file[1], roubos, furtos))
    df = pd.DataFrame(zip_bairros_data, columns=["Bairro", "Total de ROUBO - OUTROS", "Total de FURTO - OUTROS"])
    df.to_csv("src/data.csv", index=False, encoding='ISO-8859-1')
    return df