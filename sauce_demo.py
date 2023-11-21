from file_manipulation import FileTools
from navigation import Browser, PageObjects


# Atribuição de Variaveis
site_sauce = "https://www.saucedemo.com/v1/"
user = 'standard_user'
password = 'secret_sauce'

site_fake_data = 'https://www.fakenamegenerator.com/gen-random-br-br.php'

csv_items = './assets/item_list.csv'
csv_contact = './assets/contact_list.csv'
csv_order = './assets/order_list.csv'


class E_Commerce:
    def fake_data():
        # Coleta contato para o processo de compra e Ordem Fakturama
        driver = Browser.chrome_browser(site_fake_data)
        FileTools.cria_csv(csv_contact, ['First Name', 'Last Name', 'Zip Code'])
        FileTools.escreve_csv(csv_contact, PageObjects.executa_fake_data(driver))
        driver.close()

    def sauce_demo():
        # Acessa o site de e-commerce e coleta a lista de compras, salvando para cadastro no Fakturama
        driver = Browser.chrome_browser(site_sauce)
        PageObjects.acessa_sauce_demo(user, password, driver)
        # time.sleep(2)

        FileTools.cria_csv(csv_items)

        for i in range(1, 7):
            FileTools.escreve_csv(csv_items, PageObjects.sauce_items(driver, i))
        driver.close()

        # Acessa o site de e-commerce e realiza a compra de 3 produtos aleatórios da lista
        driver = Browser.chrome_browser(site_sauce)
        PageObjects.acessa_sauce_demo(user, password, driver)

        for i, r in (FileTools.random_select_items()).iterrows():
            PageObjects.add_to_cart(driver, i+1)

        PageObjects.finish_order(driver, FileTools.le_dados_contato(csv_contact))
        driver.close()
