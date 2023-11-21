from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Browser:
    def chrome_browser(site):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--enable-chrome-browser-cloud-management")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.binary_location = "C:/Users/55549/Desktop/Python/chrome-win64 (118_0_5993_70)/chrome-win64/chrome.exe"
        chrome_driver_path = "C:/Users/55549/Desktop/Python/chromedriver-win64 (118_0_5993_70)/chromedriver-win64/chromedriver.exe"
        service_options = webdriver.ChromeService(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(options=chrome_options, service=service_options)

        driver.get(site)

        return driver


class PageObjects:
    def executa_fake_data(driver):
        first_name = Waits.visible(driver, By.XPATH, '//div[@class="address"]/h3[1]').text.split()[0]

        last_name = Waits.visible(driver, By.XPATH, '//div[@class="address"]/h3[1]').text.split()[-1]

        cep = Waits.visible(driver, By.XPATH, '//div[@class="adr"]').text.splitlines()[2]

        driver.refresh()

        return [first_name, last_name, cep]

    def acessa_sauce_demo(user, password, driver):

        textbox = Waits.visible(driver, By.ID, 'user-name')
        textbox.clear()
        textbox.send_keys(user)

        textbox = Waits.visible(driver, By.ID, 'password')
        textbox.clear()
        textbox.send_keys(password)

        textbox = Waits.visible(driver, By.ID, 'login-button')
        textbox.click()

        return True

    def sauce_items(driver, i):
        item_name = Waits.visible(driver, By.XPATH, f'/html/body/div/div[2]/div[2]/div/div[2]/div/div[{i}]/div[2]/a/div').text
        print(item_name)

        item_description = Waits.visible(driver, By.XPATH, f'/html/body/div/div[2]/div[2]/div/div[2]/div/div[{i}]/div[2]/div').text
        print(item_description)

        item_price = Waits.visible(driver, By.XPATH, f'/html/body/div/div[2]/div[2]/div/div[2]/div/div[{i}]/div[3]/div').text.replace('$', '').replace('.', ',')
        print(item_price)

        return [i, item_name, item_description, item_price]

    def add_to_cart(driver, i):
        add_item = Waits.clickable(driver, By.XPATH, f'/html/body/div/div[2]/div[2]/div/div[2]/div/div[{i}]/div[3]/button')
        add_item.click()

    def finish_order(driver, contato):
        cart_icon = Waits.clickable(driver, By.ID, 'shopping_cart_container')
        cart_icon.click()

        checkout_button = Waits.clickable(driver, By.XPATH, '//*[@class = "btn_action checkout_button"]')
        checkout_button.click()

        textbox = Waits.visible(driver, By.ID, 'first-name')
        textbox.clear()
        textbox.send_keys(contato[0])

        textbox = Waits.visible(driver, By.ID, 'last-name')
        textbox.clear()
        textbox.send_keys(contato[1])

        textbox = Waits.visible(driver, By.ID, 'postal-code')
        textbox.clear()
        textbox.send_keys(contato[2])

        continue_button = Waits.clickable(driver, By.XPATH, '//*[@class = "btn_primary cart_button"]')
        continue_button.click()

        order_value = Waits.visible(driver, By.XPATH, '//*[@id="checkout_summary_container"]/div/div[2]/div[5]')
        driver.execute_script("arguments[0].scrollIntoView();", order_value)

        driver.get_screenshot_as_file(f"./audit_files/screenshot1_{contato[0] + ' ' + contato[1]}.png")

        finish_button = Waits.clickable(driver, By.XPATH, '//*[@class = "btn_action cart_button"]')
        finish_button.click()

        driver.get_screenshot_as_file(f"./audit_files/screenshot2_{contato[0] + ' ' + contato[1]}.png")


class Waits:
    def clickable(driver, by_type, selector):
        return WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by_type, selector)))

    def visible(driver, by_type, selector):
        return WebDriverWait(driver, 10).until(EC.visibility_of_element_located((by_type, selector)))

    def url(driver, by_type, selector):
        return WebDriverWait(driver, 10).until(EC.url_to_be((by_type, selector)))
