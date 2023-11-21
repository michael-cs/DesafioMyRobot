import pyautogui as pg
import pandas as pd
import psutil
import time
import sys
import os
import logging
import logging.config
import pyperclip


class DesktopTools:
    def inicialize_software():
        for process in psutil.process_iter(["name"]):
            if process.info["name"] == "Fakturama.exe":
                return True
        return False

    def try_locate_image(imagePath, try_count=0, tries=5):
        while try_count >= 0:
            position = pg.locateOnScreen(imagePath, grayscale=True, confidence=0.7)
            time.sleep(1)
            try_count += 1
            if try_count >= tries or position is not None:
                break
        try:
            if position is not None:
                print(f"position = {position}")
                return position
            else:
                raise Exception(f'Imagem: "{imagePath}", não localizada')
        except Exception:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            pg.screenshot(f"./logs/screenshots/ERROR_{timestr}.png")
            sys.exit()

    def product_validation(produto):
        products_db = DesktopTools.try_locate_image(r"assets\images\label_products.PNG")
        pg.click(products_db, interval=2)
        search_products_db = DesktopTools.try_locate_image(
            r"assets\images\field_search_product.PNG"
        )
        pg.click(search_products_db, interval=2)
        pg.move(100, 0)
        pg.click()
        pg.typewrite(produto)
        listed_item = DesktopTools.try_locate_image(
            r"assets\images\label_item_number.PNG"
        )
        pg.click(listed_item, interval=2)
        pg.move(0, 15)
        pg.click()
        pg.click(search_products_db, interval=2)
        pg.move(160, 0)
        pg.click()
        print('campo limpo')
        pg.hotkey('ctrl', 'd')
        pg.hotkey('enter')

        return True


class FakturamaActivities:
    def cadastra_produtos():
        if not DesktopTools.inicialize_software():
            os.startfile(r"C:\Program Files\Fakturama2\Fakturama.exe")

        df = pd.read_csv(r".\assets\item_list.csv")

        new_product = DesktopTools.try_locate_image(
            r".\assets\images\btn_new_product.PNG", tries=30
        )

        for i, r in df.iterrows():
            item_number = str(r.iloc[0])
            item_name = r.iloc[1]
            description = r.iloc[2]
            price = str(r.iloc[3])

            validation = DesktopTools.product_validation(item_name)

            if validation:
                pg.click(new_product, interval=2)
                label = DesktopTools.try_locate_image(
                    r".\assets\images\label_new_product.PNG"
                )
                pg.click(label, interval=2)
                pg.press("tab", 2, interval=0.5)
                pg.typewrite(item_number)
                logging.info(item_number)
                pg.press("tab", 1, interval=0.5)
                pg.typewrite(item_name)
                logging.info(item_name)
                pg.press("tab", 1, interval=0.5)
                pg.typewrite("Shop")
                pg.press("tab", 3, interval=0.5)
                pg.typewrite(description)
                logging.info(description)
                pg.press("tab", 1, interval=0.5)
                pg.typewrite(price)
                pg.hotkey("ctrl", "s")
                pg.hotkey("ctrl", "w")

    def cadastra_contato():
        if not DesktopTools.inicialize_software():
            os.startfile(r"C:\Program Files\Fakturama2\Fakturama.exe")

        df = pd.read_csv(r".\assets\contact_list.csv", encoding='UTF8')
        print(df.head())

        new_contact = DesktopTools.try_locate_image(
            r".\assets\images\btn_new_contact.PNG", tries=30
        )

        for i, r in df.iterrows():
            first_name = str(r.iloc[0])
            last_name = str(r.iloc[1])
            cep = str(r.iloc[2])
            if new_contact is not None:
                pg.click(new_contact, interval=2)
                pg.press("tab", 4, interval=0.5)
                pyperclip.copy(first_name)
                pg.hotkey('ctrl', 'v', interval=0.1)
                print(first_name)
                pg.press("tab")
                pyperclip.copy(last_name)
                pg.hotkey('ctrl', 'v', interval=0.1)
                print(last_name)
                pg.press("tab", 8, interval=0.5)
                pg.typewrite(cep)
                print(cep)
                pg.hotkey("ctrl", "s")
                pg.hotkey("ctrl", "w")

    def preenche_ordem():
        if not DesktopTools.inicialize_software():
            os.startfile(r"C:\Program Files\Fakturama2\Fakturama.exe")

        df = pd.read_csv(r".\assets\contact_list.csv")
        contato = str(df.iloc[0, 0])

        new_order = DesktopTools.try_locate_image(
            r".\assets\images\btn_new_order.PNG", tries=30
        )
        if new_order is not None:
            pg.click(new_order, interval=2)
            contact_list = DesktopTools.try_locate_image(
                r".\assets\images\btn_contact_list.PNG"
            )
            pg.click(contact_list, interval=2)
            pyperclip.copy(contato)
            pg.hotkey('ctrl', 'v', interval=0.1)
            first_item_select = DesktopTools.try_locate_image(
                r".\assets\images\btn_first_item.PNG"
            )
            pg.click(first_item_select, interval=2)
            pg.move(40, 0)
            pg.doubleClick()
            df = pd.read_csv(r".\assets\order_list.csv")
            for i, r in df.iterrows():
                produto = r.iloc[1]
                product_list = DesktopTools.try_locate_image(
                    r".\assets\images\btn_product_list.PNG"
                )
                pg.click(product_list, interval=2)
                pg.typewrite(produto, interval=0.1)
            pg.hotkey("ctrl", "s")
            pg.hotkey("ctrl", "p", interval=0.5)
            pg.hotkey("ctrl", "w", interval=0.5)
            pg.hotkey("alt", "F4", interval=0.5)
