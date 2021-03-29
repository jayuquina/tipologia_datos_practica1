#imports here
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import datetime
import os
import sys
import time

USERNAME = 'mayuqui5'
PASSWORD = '********'

#definition of language and get label from dictionary
LANGUAGE = 'spanish'

def get_label_by_language(text):
    dictionary = (('Not Now', 'Ahora no'), ('Search', 'Busca'), 
    ('Verificated', 'Verificado'), ('publications', 'publicaciones'), 
    ('followers', 'seguidores'), ('followed', 'seguidos'))
    pos_language = 0
    
    if LANGUAGE=='english' :
        pos_language = 0
    else:
        pos_language = 1
    
    n_length = len(dictionary)
    label = ''

    for pos_dic in range(0, n_length):
        if dictionary[pos_dic][0] == text:
            label = dictionary[pos_dic][pos_language]
            break
    return label

#removes automation flag
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

#specify the path to chromedriver.exe (download and save on your computer)
#DRIVER_PATH = 'C:/Users/marth/Documents/Python_Mac/chromedriver_win32/chromedriver'
DRIVER_PATH = 'C:/Programas/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
#driver.get('https://google.com')

#driver = webdriver.Firefox(executable_path=DRIVER_PATH)

#open the webpage
driver.get("http://www.instagram.com")

#target username
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

#enter username and password
username.clear()
username.send_keys(USERNAME)
password.clear()
password.send_keys(PASSWORD)

#target the login button and click it
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

#We are logged in!
time.sleep(5)
alert = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "'+get_label_by_language('Not Now')+'")]'))).click()
alert2 = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "'+get_label_by_language('Not Now')+'")]'))).click()

#target the search input field
searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='"+get_label_by_language('Search')+"']")))
searchbox.clear()

#search for the hashtag

#keyword = "#guillermolasso"
#keyword = "#andresnomientasotravez"
#keyword = "#andresarauz"
keyword = "#lassoesmoreno"

searchbox.send_keys(keyword)
 
#FIXING THE DOUBLE ENTER
time.sleep(5) # Wait for 5 seconds
my_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/" + keyword[1:] + "/')]")))
my_link.click()

#scroll down 2 times
#increase the range to sroll more
n_scrolls = 2
for j in range(0, n_scrolls):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

#click to first presentation
driver.find_element_by_class_name('v1Nh3').click()

#definition to find element text by xpath parameter
def find_text_by_xpath(xpath, field):
    text = ''
    try:
        element = driver.find_element_by_xpath(xpath)
        text = element.text
    except:
        e = sys.exc_info()[0]
        print(field, str(e))
    return text

#definition to find element attribute by xpath and attribute
def find_attribute_by_xpath(xpath, attribute, field):
    value = ''
    try:
        element = driver.find_element_by_xpath(xpath)
        value = element.get_attribute(attribute)
    except:
        e = sys.exc_info()[0]
        print(field, str(e))
    return value

#definition Article class
class Article:
    def __init__(self, user, location, image_description, image_url, image_type, verificated, publications, followers, followed, comment, date_time):
        self.user = user
        self.location = location
        self.image_description = image_description
        self.image_url = image_url
        self.image_type = image_type
        self.verificated = verificated
        self.publications = publications
        self.followers = followers
        self.followed = followed
        self.comment = comment
        self.date_time = date_time
    
    #save data as csv
    def save_as_txt(self, name):
        sep = ';'
        sys_time = datetime.datetime.now().isoformat()
        self.location = self.location.replace(',', '|')
        self.image_description = self.image_description.replace(',', '|')
        self.publications = self.publications.replace(',', '.')
        self.followers = self.followers.replace(',', '.')
        self.followed = self.followed.replace(',', '.')
        self.comment = self.comment.replace(sep, '|')
        self.comment = self.comment.replace(',', '|')
        self.comment = self.comment.replace('\n', '\\n')
        self.comment = self.comment.replace('\r', '\\n')
        line = name+sep+sys_time+sep+self.user+sep+self.location+sep+self.image_description+sep+self.image_url+sep+self.image_type+sep+self.verificated+sep+self.publications+sep+self.followers+sep+self.followed+sep+self.comment+sep+self.date_time+'\n'
        fname = 'influencia_elecciones_presidenciales_ec_2021.csv'
        empty = os.path.exists(fname)==False or os.stat(fname).st_size==0
        
        fwrite = open(fname, 'a+', encoding='utf-8')

        if empty:
            header = 'hashtag'+sep+'sys_time'+sep+'user'+sep+'location'+sep+'image_description'+sep+'image_url'+sep+'image_type'+sep+'verificated'+sep+'publications'+sep+'followers'+sep+'followed'+sep+'comment'+sep+'date_time'+'\n'
            fwrite.write(header)

        fwrite.write(line)
        fwrite.close()

#iterate each presentation 5 times
n_articles = 15
for art in range(0, n_articles):
    print('---------------', (art+1), '---------------')
    time.sleep(10)
    #extract data of presentation
    user = find_text_by_xpath('//article[contains(@role, "presentation")]/header/div[2]/div[1]//a', 'user')
    location = find_text_by_xpath('//article[contains(@role, "presentation")]/header/div[2]/div[2]//a', 'location')
    image_description = find_attribute_by_xpath('//article[contains(@role, "presentation")]/div[2]/div[1]//img[1]', 'alt', 'image_description')
    image_url = find_attribute_by_xpath('//article[contains(@role, "presentation")]/div[2]/div[1]//img[1]', 'src', 'image_url')
    image_type = ''
    if image_url=='':
        image_url = find_attribute_by_xpath('//article[contains(@role, "presentation")]/div[2]/div[1]//video[1]', 'poster', 'image_url')
        image_type = find_attribute_by_xpath('//article[contains(@role, "presentation")]/div[2]/div[1]//video[1]', 'type', 'image_type')
    verificated = find_text_by_xpath('//article[contains(@role, "presentation")]/header/div[2]//span[contains(@title, "'+get_label_by_language('Verificated')+'")]', 'verificated')
    comment = find_text_by_xpath('//article[contains(@role, "presentation")]/div[3]/div[1]/ul[1]/div[1]/li/div/div/div[2]/span', "comment")
    date_time = find_attribute_by_xpath('//article[contains(@role, "presentation")]/div[3]/div[2]//time', 'datetime', 'date_time')
    
    #explore user element
    user_el = driver.find_element_by_xpath('//article[contains(@role, "presentation")]/header/div[2]/div[1]//span')

    #mouse over with Javascript
    move_to_user_el_script = """if(document.createEvent){
    var event=document.createEvent('MouseEvents');
    event.initMouseEvent('mouseover', true, false);
    arguments[0].dispatchEvent(event);
    } else if(document.createEventObject){
    arguments[0].fireEvent('onmouseover');}"""
    
    driver.execute_script(move_to_user_el_script, user_el)

    time.sleep(10)

    #extract data of user element
    publications = find_text_by_xpath('(//*[contains(., "'+get_label_by_language('publications')+'")])[last()]/span', "publications")
    followers = find_text_by_xpath('(//*[contains(., "'+get_label_by_language('followers')+'")])[last()]/span', "followers")
    followed = find_text_by_xpath('(//*[contains(., "'+get_label_by_language('followed')+'")])[last()]/span', "followed")

    #new instance of article and save data
    article = Article(user, location, image_description, image_url, image_type, verificated, publications, followers, followed, comment, date_time)
    print(user, location, image_description, image_url, image_type, verificated, publications, followers, followed, comment, date_time)
    article.save_as_txt(keyword)
    #go to next presentation
    driver.find_element_by_class_name('coreSpriteRightPaginationArrow').click()
    time.sleep(5)
