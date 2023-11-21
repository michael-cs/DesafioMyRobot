import pandas as pd
import random
import csv
import os


class FileTools:
    def random_select_items(archive='./assets/item_list.csv'):
        df = pd.read_csv(archive)
        rows = (df.shape[0])
        ordered_items = df.iloc[(random.sample(range(rows), 3))]
        archive = './assets/order_list.csv'
        FileTools.cria_csv(archive)
        for i, r in ordered_items.iterrows():
            FileTools.escreve_csv(archive, r)

        return ordered_items

    def le_dados_contato(arquivo):
        df = pd.read_csv(arquivo, encoding='UTF8')

        first_name = df['First Name'][0]
        last_name = df['Last Name'][0]
        cpf = df['Zip Code'][0]
        contato = [first_name, last_name, cpf]

        return contato

    def cria_csv(file_path, header=['Item Number', 'Item Name', 'Description', 'Price']):
        if os.path.exists(file_path):
            os.remove(file_path)

        with open((file_path), 'w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)

    def escreve_csv(file_path, row):
        with open((file_path), 'a', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
