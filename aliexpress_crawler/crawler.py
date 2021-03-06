from selenium import webdriver
import pandas as pd
import time
import signal
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv

# Config
shopee_field_names = [
    'ps_url',
    'ps_category_list_id',
    'ps_product_name',
    'ps_product_description',
    'ps_price',
    'ps_stock',
    'ps_product_weight',
    'ps_days_to_ship',
    'ps_sku_ref_no_parent',
    'ps_mass_upload_variation_help',
    'ps_variation 1 ps_variation_sku',
    'ps_variation 1 ps_variation_name',
    'ps_variation 1 ps_variation_price',
    'ps_variation 1 ps_variation_stock',
    'ps_variation 2 ps_variation_sku',
    'ps_variation 2 ps_variation_name',
    'ps_variation 2 ps_variation_price',
    'ps_variation 2 ps_variation_stock',
    'ps_variation 3 ps_variation_sku',
    'ps_variation 3 ps_variation_name',
    'ps_variation 3 ps_variation_price',
    'ps_variation 3 ps_variation_stock',
    'ps_variation 4 ps_variation_sku',
    'ps_variation 4 ps_variation_name',
    'ps_variation 4 ps_variation_price',
    'ps_variation 4 ps_variation_stock',
    'ps_variation 5 ps_variation_sku',
    'ps_variation 5 ps_variation_name',
    'ps_variation 5 ps_variation_price',
    'ps_variation 5 ps_variation_stock',
    'ps_variation 6 ps_variation_sku',
    'ps_variation 6 ps_variation_name',
    'ps_variation 6 ps_variation_price',
    'ps_variation 6 ps_variation_stock',
    'ps_variation 7 ps_variation_sku',
    'ps_variation 7 ps_variation_name',
    'ps_variation 7 ps_variation_price',
    'ps_variation 7 ps_variation_stock',
    'ps_variation 8 ps_variation_sku',
    'ps_variation 8 ps_variation_name',
    'ps_variation 8 ps_variation_price',
    'ps_variation 8 ps_variation_stock',
    'ps_variation 9 ps_variation_sku',
    'ps_variation 9 ps_variation_name',
    'ps_variation 9 ps_variation_price',
    'ps_variation 9 ps_variation_stock',
    'ps_variation 10 ps_variation_sku',
    'ps_variation 10 ps_variation_name',
    'ps_variation 10 ps_variation_price',
    'ps_variation 10 ps_variation_stock',
    'ps_variation 11 ps_variation_sku',
    'ps_variation 11 ps_variation_name',
    'ps_variation 11 ps_variation_price',
    'ps_variation 11 ps_variation_stock',
    'ps_variation 12 ps_variation_sku',
    'ps_variation 12 ps_variation_name',
    'ps_variation 12 ps_variation_price',
    'ps_variation 12 ps_variation_stock',
    'ps_variation 13 ps_variation_sku',
    'ps_variation 13 ps_variation_name',
    'ps_variation 13 ps_variation_price',
    'ps_variation 13 ps_variation_stock',
    'ps_variation 14 ps_variation_sku',
    'ps_variation 14 ps_variation_name',
    'ps_variation 14 ps_variation_price',
    'ps_variation 14 ps_variation_stock',
    'ps_variation 15 ps_variation_sku',
    'ps_variation 15 ps_variation_name',
    'ps_variation 15 ps_variation_price',
    'ps_variation 15 ps_variation_stock',
    'ps_img_1',
    'ps_img_2',
    'ps_img_3',
    'ps_img_4',
    'ps_img_5',
    'ps_img_6',
    'ps_img_7',
    'ps_img_8',
    'ps_img_9'
]
raw_field_names = [
    'ps_url',
    'ps_product_name',
    'ps_original_price',
    'ps_price',
    'ps_stock',
    'ps_product_weight',
    'ps_days_to_ship',
    "ps_shipping_fee",
    'ps_store_name',
    "ps_store_item_rating",
    "ps_store_communication_rating",
    "ps_store_speed_rating",
    'ps_size',
    'ps_num_bought',
    'ps_num_of_feedback',
    'ps_img_1',
    'ps_img_2',
    'ps_img_3',
    'ps_img_4',
    'ps_img_5',
    'ps_img_6',
    'ps_img_7',
    'ps_img_8',
    'ps_img_9'
]
no_of_images = 9
base_url = 'https://%s.aliexpress.com/store/all-wholesale-products/%s.html?spm=2114.12010608.0.0.5c74898bWMbaEw'
options = ChromeOptions()
options.add_argument('--disable-popup-blocking')
options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2,
                                          'profile.managed_default_content_settings.javascript': 2})

options_with_js = ChromeOptions()
options_with_js.add_argument('--disable-popup-blocking')
options_with_js.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})

options_with_js_image = ChromeOptions()
options_with_js_image.add_argument('--disable-popup-blocking')


def login(browser):
    """
    Function to let user login
    :param browser:
    :return:
    """

    print "User login...."
    frame = browser.find_element_by_tag_name('iframe')
    browser.switch_to.frame(frame)
    username = browser.find_element_by_name('loginId')
    password = browser.find_element_by_name("password")
    username.send_keys("ziao.chen@shopee.com")
    password.send_keys("ziaochen")
    browser.find_element_by_xpath("//input[@id='fm-login-submit']").click()
    time.sleep(6)
    print "Login finish."


def get_user_input():
    """
    Return user input value
    :return:
    """
    store_name = raw_input("Please input the store name: ")
    store_id = raw_input("Please input the store id: ")
    no_items = int(input("Please input the number of items to crawl: "))
    with_js = True
    # with_js = int(input("Please choose to crawl stock and shipping fee (1 for yes, 0 for no): "))
    # while with_js != 1 and with_js != 0:
    #     with_js = int(input("Please only reply 1 or 0: "))

    return (store_name, store_id, no_items, with_js)


def get_item_details(item, browser, with_js):
    """
    Fetch item details
    :param item:
    :return:
    """
    start = time.time()

    item_url = item.find_element_by_class_name("pic-rind").get_attribute('href')
    item_dict_raw = {}
    # browser = webdriver.PhantomJS()
    # browser = webdriver.Chrome('chromedriver')
    print "Getting item details from: %s" % item_url

    # browser.get(item_url)
    #
    # print "Web Page loaded"
    # if "Buy Products Online from China Wholesalers at Aliexpress" in browser.title:
    #     login(browser)
    while 1:
        try:
            browser.get(item_url)

            print "Web Page loaded"
            if "Buy Products Online from China Wholesalers at Aliexpress" in browser.title:
                login(browser)
            item_dict_raw["ps_url"] = item_url
            item_dict_raw["ps_product_name"] = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'product-name'))).text
            item_dict_raw["ps_original_price"] = float(WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.ID, "j-sku-price"))).text.split("-")[0])
            break
        except:
            print "Please do sliding or input captcha"
            time.sleep(10)

    # Some items may not have discount price
    try:
        item_dict_raw["ps_price"] = float(browser.find_element_by_id("j-sku-discount-price").text.split("-")[0])
    except:
        pass

    item_dict_raw['ps_product_description'] = browser.find_element_by_class_name('product-property-list').text.replace("\n"," ")

    # if with_js:
    item_dict_raw["ps_shipping_fee"] = browser.find_element_by_class_name("logistics-cost").text
    item_dict_raw["ps_days_to_ship"] = int(browser.find_element_by_class_name("shipping-days").text.split("-")[0])

    # Item may never be bought
    try:
        item_dict_raw["ps_num_bought"] = int(browser.find_element_by_class_name("order-num").text.split(" ")[0])
    except:
        pass

    if with_js:
        item_dict_raw["ps_stock"] = int(browser.find_element_by_id("j-sell-stock-num").text.split(" ")[0])
    item_dict_raw["ps_num_of_feedback"] = int(
        browser.find_element_by_xpath("//li[@data-trigger='feedback']/a").text.replace("Feedback (", "").replace(")",
                                                                                                                 ""))
    # Get property
    print "Getting item properties..."
    property_list = (browser.find_elements_by_class_name('p-property-item'))
    variation_list = []
    variation_count = 0
    variation_type = ""
    for property in property_list:
        property_name = property.find_element_by_class_name('p-item-title').text
        if "Size" in property_name or "size" in property_name:
            variation_list = property.find_elements_by_tag_name('a')
            variation_type = "size"
        elif "Color" in property_name or "color" in property_name:
            variation_list = property.find_elements_by_tag_name('a')
            variation_type = "color"

    for variation in variation_list:
        variation_count += 1
        if variation_count > 15:
            break
        if variation_type == "size":
            if variation.get_attribute('id') != 'sizing-info-btn':
                item_dict_raw['ps_variation %d ps_variation_name' % variation_count] = item_dict_raw[
                                                                                           "ps_product_name"] + "_" + variation.find_element_by_tag_name(
                    'span').text
            else:
                variation_count -= 1
        else:
            item_dict_raw['ps_variation %d ps_variation_name' % variation_count] = item_dict_raw[
                                                                                       "ps_product_name"] + "_" + variation.get_attribute(
                "title")
    # property_name_list = browser.find_elements_by_class_name("property-title")
    # property_value_list = browser.find_elements_by_class_name("property-des")
    # for i in range(len(property_name_list)):
    #     if property_name_list[i].text == "Weight:":
    #         item_dict_raw["ps_product_weight"] = property_value_list[i].text
    #     elif property_name_list[i].text == "Size:":
    #         item_dict_raw["ps_size"] = property_value_list[i].text

    img_list = browser.find_elements_by_class_name("img-thumb-item")
    for i in range(min(no_of_images, len(img_list))):
        item_dict_raw["ps_img_%s" % str(i + 1)] = img_list[i].find_element_by_tag_name("img").get_attribute(
            "src").replace('.jpg_50x50', "")

    print "Crawled data: %s" % str(item_dict_raw)
    print "Takes %ss" % str(int(time.time() - start))
    # browser.service.process.send_signal(signal.SIGTERM)
    # browser.quit()

    return item_dict_raw


def main():
    # Get user defined parameter
    store_name, store_id, no_items, with_js = get_user_input()
    pages_to_crawl = int(no_items / 50) + 1

    # Start the browser
    browser = webdriver.Chrome("chromedriver")
    # browser = webdriver.PhantomJS()
    while 1:
        try:
            browser.get(base_url % (store_name, store_id))

            # Check Login
            if "Buy Products Online from China Wholesalers at Aliexpress" in browser.title:
                login(browser)

            # Get maximum pages available
            available_pages = browser.find_elements_by_xpath("//div[@class='ui-pagination-navi util-left']/a")

            if len(available_pages) > 0:
                max_page = int(available_pages[-2].text)
            else:
                max_page = 1

            # Get seller name
            seller_name = browser.find_element_by_xpath("//span[@class='shop-name']/a").text
            break
        except:
            print "Please do sliding"
            time.sleep(10)
            pass

    # Hover the title bar to get ratings
    print "Get ratings..."
    ActionChains(browser).move_to_element(browser.find_element_by_class_name("store-rank")).perform()
    while True:
        time.sleep(1)
        rating_list = browser.find_elements_by_xpath("//dd[@class='dsr-above']/a/b")
        if rating_list:
            rating_list[0] = rating_list[0].text
            rating_list[1] = rating_list[1].text
            rating_list[2] = rating_list[2].text
            break
        elif "block" in browser.find_element_by_xpath("//div[@class='store-dsr-data']/p").get_attribute("style"):
            rating_list[0] = ""
            rating_list[1] = ""
            rating_list[2] = ""
            break
        else:
            print "Not hover yet. Waiting..."

    print "Ratings obtained"

    # Start to get data
    raw_dataframe = pd.DataFrame([])
    shopee_dataframe = pd.DataFrame([])
    raw_writer = csv.DictWriter(open("%s_temp.csv" % seller_name, "wb"), fieldnames=raw_field_names)
    raw_writer.writeheader()
    if with_js:
        item_browser = webdriver.Chrome("chromedriver")
    # browser = webdriver.PhantomJS())
    else:
        item_browser = webdriver.Chrome("chromedriver")
    # browser = webdriver.PhantomJS())

    counter = 0
    for page in range(1, min(max_page, pages_to_crawl) + 1):
        item_list = browser.find_elements_by_xpath("//li[@class='item']")
        for item in item_list:
            if counter == no_items:
                break

            item_details = get_item_details(item, item_browser, with_js)
            item_details["ps_store_name"] = seller_name
            item_details["ps_store_item_rating"] = rating_list[0]
            item_details["ps_store_communication_rating"] = rating_list[1]
            item_details["ps_store_speed_rating"] = rating_list[2]

            item_details_raw = {}
            for key in raw_field_names:
                if key in item_details:
                    item_details_raw[key] = item_details[key]
                else:
                    item_details_raw[key] = None

            item_details_shopee = {}
            for key in shopee_field_names:
                if key in item_details:
                    item_details_shopee[key] = item_details[key]
                else:
                    item_details_shopee[key] = None

            # Append each item to the whole dataframe
            raw_dataframe = pd.concat([raw_dataframe, pd.DataFrame.from_dict([item_details_raw])])
            shopee_dataframe = pd.concat([shopee_dataframe, pd.DataFrame.from_dict([item_details_shopee])])
            raw_writer.writerow(item_details_raw)
            counter = counter + 1

        # Go to next page
        if page < min(max_page, pages_to_crawl):
            browser.find_element_by_xpath(
                "//div[@class='ui-pagination-navi util-left']/a[text()='%s']" % str(page + 1)).click()

    raw_writer = pd.ExcelWriter("%s.xlsx" % seller_name)
    raw_dataframe = raw_dataframe[raw_field_names]
    raw_dataframe.to_excel(raw_writer, "Sheet1", index=False)
    raw_writer.save()

    shopee_writer = pd.ExcelWriter("%s_shopee_format.xlsx" % seller_name)
    shopee_dataframe = shopee_dataframe[shopee_field_names]
    shopee_dataframe.to_excel(shopee_writer, "Sheet1", index=False)
    shopee_writer.save()
    item_browser.close()
    browser.close()
    item_browser.service.process.send_signal(signal.SIGTERM)
    item_browser.quit()
    browser.service.process.send_signal(signal.SIGTERM)
    browser.quit()


main()
