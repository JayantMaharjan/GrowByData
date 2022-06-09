from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd

options = Options()
options.headless = True

driver = webdriver.Chrome(executable_path='/home/jayant/Downloads/selenium/chromedriver', options=options)
only_title = []
only_links = []
only_content = []
header = ['Title', 'Value']
xpath = "//h3/parent::a/ancestor::div[@data-hveid and @data-ved and @class='g tF2Cxc'] | " \
        "//h3//parent::a/ancestor::div[@data-hveid and @data-ved]/parent::div[contains(@class,'g')][not(" \
        "./ancestor::ul)]/parent::div[not(@id) or @id='rso']/div[contains(@class,'g')][not(./ancestor::ul)][not(" \
        "@data-md)][not(descendant::table)][not(./g-card)][not(parent::div[contains(@class,'V3FYCf')])] | " \
        "//h3//parent::a/ancestor::div[@data-hveid and @data-ved]/ancestor::div[@class='g']/parent::div[" \
        "@data-hveid]//div[@data-hveid and @data-ved][not(./ancestor::ul)][not(parent::div[contains(@class," \
        "'g ')])] | //h3/parent::a/ancestor::div[contains(@class,'ZINbbc') and contains(@class,'uUPGi')]/parent::div " \
        "| //a[contains(@href,'youtube')][./h3][not(ancestor::div[contains(@style,'display:none')])]/ancestor::div[" \
        "not(@*)][parent::div[contains(@class,'g')]] "


def extract_data(url, url_num):
    driver.get(url)
    screenshots(url_num)
    html_dump(url_num)

    indexing = []
    content_list = []
    link_list = []
    title_list = []

    title_path = '(' + xpath + ')' + '//div/a/h3'
    link_path = '(' + xpath + ')' + "//div[@class='TbwUpd NJjxre']"
    content_path = '(' + xpath + ')' + "//div[@class='VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf']|//div[" \
                                       "@class='VwiC3b yXK7lf MUxGbd yDYNvb " \
                                       "lyLwlc'] "
    titles = driver.find_elements(by=By.XPATH, value=title_path)
    links = driver.find_elements(by=By.XPATH, value=link_path)
    contents = driver.find_elements(by=By.XPATH, value=content_path)
    for content in contents:
        content_list.append(content.text)

    for link in links:
        link_list.append(link.text.split(" ")[0])

    for title in titles:
        title_list.append(title.text)

    df_title = pd.DataFrame(title_list)

    for i in range(len(df_title)):
        indexing.append(i)

    df_link = pd.DataFrame(link_list)

    df_content = pd.DataFrame(content_list)

    for i in range(len(df_title)):
        only_title.append('Title')
        only_content.append('Content')
        only_links.append('Link')

    emb_title = pd.Series(only_title)
    emb_link = pd.Series(only_links)
    emb_content = pd.Series(only_content)

    df_title.insert(0, '', emb_title)
    df_link.insert(0, '', emb_link)
    df_content.insert(0, '', emb_content)

    final_df = pd.concat([df_title, df_link, df_content])
    index_file = []
    for i in range(3):
        for j in range(len(df_title)):
            a = (str(url_num) + '.' + str(j + 1) + '.' + str(i + 1))
            index_file.append(a)

    index_file = pd.Series(index_file)

    final_df.index = index_file
    final_df.columns = header
    return final_df


def read_csv():
    df = pd.read_csv('./url_list.csv')
    return df


def screenshots(url_num):
    viewport_height = driver.execute_script("return window.innerHeight")
    viewport_height -= 80  # -> to obtain full data screenshot
    height = driver.execute_script("return document.body.scrollHeight")
    i = 0  # -> for file name
    y = 0  # -> for equating height left to scroll
    while y < height:
        driver.get_screenshot_as_file(f"./screenshots/{url_num}_v" + str(i) + '.png')
        driver.execute_script(f"window.scrollBy(0,{viewport_height})")
        sleep(2)
        y += viewport_height
        i += 1

    s = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
    driver.set_window_size(s('Width'), s('Height'))
    driver.find_element(by=By.TAG_NAME, value='body').screenshot(f'./screenshots/{url_num}.png')
    driver.set_window_size(s('Width'), viewport_height)


def html_dump(url_num):
    driver.implicitly_wait(2)
    f = open(f'./html_dumps/webpage{url_num}.html', "w")
    # obtain page source
    h = driver.page_source
    # write page source content to file
    f.write(h)
    f.close()


def main():
    output = pd.DataFrame()
    url_num = 1
    url_list = read_csv()
    for urls in url_list['URL']:
        final_df = extract_data(urls, url_num)
        output = output.append(final_df)
        url_num = url_num + 1
    output.index.name = 'Index'
    print(output)
    output.to_csv('output.csv')
    driver.close()


if __name__ == '__main__':
    main()
