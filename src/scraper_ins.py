#imports here
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import tkinter as tk
import tkinter.ttk as ttk
import datetime
import os
import sys
import time

#user and credential management
USERNAME = ''
PASSWORD = ''
#definition of language and get label from dictionary
LANGUAGE = 'spanish'
#definition of search parameters, scroll and articles number
KEYWORD = ''
NSCROLL = 2
NARTICLES = 3

def get_label_by_language(text):
    global LANGUAGE

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

def start_scraper_ins():
    global LANGUAGE

    #removes automation flag
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    #specify the path to chromedriver.exe (download and save on your computer)
    DRIVER_PATH = 'C:/Programas/chromedriver_win32/chromedriver.exe'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)

    if LANGUAGE=='english' :
        #open the webpage
        driver.get("https://www.instagram.com/?hl=en-us")
    else:
        #open the webpage
        driver.get("https://www.instagram.com/?hl=es-la")
    
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
    keyword = KEYWORD

    searchbox.send_keys(keyword)
    
    #FIXING THE DOUBLE ENTER
    time.sleep(5) # Wait for 5 seconds
    my_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/" + keyword[1:] + "/')]")))
    my_link.click()

    #scroll down 2 times
    #increase the range to sroll more
    n_scrolls = NSCROLL
    for j in range(0, n_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    #click to first presentation
    driver.find_element_by_class_name('v1Nh3').click()

    #iterate each presentation 5 times
    n_articles = NARTICLES
    for art in range(0, n_articles):
        print('---------------', (art+1), '---------------')
        time.sleep(10)
        #extract data of presentation
        user = find_text_by_xpath(driver, '//article[contains(@role, "presentation")]/header/div[2]/div[1]//a', 'user')
        location = find_text_by_xpath(driver, '//article[contains(@role, "presentation")]/header/div[2]/div[2]//a', 'location')
        image_description = find_attribute_by_xpath(driver, '//article[contains(@role, "presentation")]/div[2]/div[1]//img[1]', 'alt', 'image_description')
        image_url = find_attribute_by_xpath(driver, '//article[contains(@role, "presentation")]/div[2]/div[1]//img[1]', 'src', 'image_url')
        
        if image_url!='':
            image_type = 'jpg'
        
        video_url = ''

        if image_url=='':
            image_url = find_attribute_by_xpath(driver, '//article[contains(@role, "presentation")]/div[2]/div[1]//video[1]', 'poster', 'image_url')
            image_type = find_attribute_by_xpath(driver, '//article[contains(@role, "presentation")]/div[2]/div[1]//video[1]', 'type', 'image_type')
            video_url = find_attribute_by_xpath(driver, '//article[contains(@role, "presentation")]/div[2]/div[1]//video[1]', 'src', 'video_url')
        
        verificated = find_text_by_xpath(driver, '//article[contains(@role, "presentation")]/header/div[2]//span[contains(@title, "'+get_label_by_language('Verificated')+'")]', 'verificated')

        if verificated=='':
            verificated = 'No verificado'

        comment = find_text_by_xpath(driver, '//article[contains(@role, "presentation")]/div[3]/div[1]/ul[1]/div[1]/li/div/div/div[2]/span', "comment")
        date_time = find_attribute_by_xpath(driver, '//article[contains(@role, "presentation")]/div[3]/div[2]//time', 'datetime', 'date_time')
        
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
        publications = find_text_by_xpath(driver, '(//*[contains(., "'+get_label_by_language('publications')+'")])[last()]/span', "publications")
        followers = find_text_by_xpath(driver, '(//*[contains(., "'+get_label_by_language('followers')+'")])[last()]/span', "followers")
        followed = find_text_by_xpath(driver, '(//*[contains(., "'+get_label_by_language('followed')+'")])[last()]/span', "followed")

        #new instance of article and save data
        article = Article(user, location, image_description, image_url, image_type, video_url, verificated, publications, followers, followed, comment, date_time)
        print(user, location, image_description, image_url, image_type, video_url, verificated, publications, followers, followed, comment, date_time)
        article.save_as_txt(keyword)
        #go to next presentation
        driver.find_element_by_class_name('coreSpriteRightPaginationArrow').click()
        time.sleep(5)

#definition to find element text by xpath parameter
def find_text_by_xpath(driver, xpath, field):
    text = ''
    try:
        element = driver.find_element_by_xpath(xpath)
        text = element.text
    except:
        e = sys.exc_info()[0]
        print(field, str(e))
    return text

#definition to find element attribute by xpath and attribute
def find_attribute_by_xpath(driver, xpath, attribute, field):
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
    def __init__(self, user, location, image_description, image_url, image_type, video_url, verificated, publications, followers, followed, comment, date_time):
        self.user = user
        self.location = location
        self.image_description = image_description
        self.image_url = image_url
        self.image_type = image_type
        self.video_url = video_url
        self.verificated = verificated
        self.publications = publications
        self.followers = followers
        self.followed = followed
        self.comment = comment
        self.date_time = date_time
    
    #format to csv text
    def format_to_csv_text(self, text, sep=';'):
        format_text = text
        format_text = format_text.replace(sep, '|')
        format_text = format_text.replace('"', '""')
        format_text = format_text.replace('\n', '\\n')
        format_text = format_text.replace('\r', '\\n')
        format_text = '"'+format_text+'"'
        return format_text
    
    #save data as csv
    def save_as_txt(self, name):
        sep = ';'
        sys_time = datetime.datetime.now().isoformat()
        self.location = self.format_to_csv_text(self.location, sep)
        self.image_description = self.format_to_csv_text(self.image_description, sep)
        self.publications = self.format_to_csv_text(self.publications, sep)
        self.followers = self.format_to_csv_text(self.followers, sep)
        self.followed = self.format_to_csv_text(self.followed, sep)
        self.comment = self.format_to_csv_text(self.comment, sep)
        line = name+sep+sys_time+sep+self.user+sep+self.location+sep+self.image_description+sep+self.image_url+sep+self.image_type+sep+self.video_url+sep+self.verificated+sep+self.publications+sep+self.followers+sep+self.followed+sep+self.comment+sep+self.date_time+'\n'
        fname = 'influencia_elecciones_presidenciales_ec_2021.csv'
        empty = os.path.exists(fname)==False or os.stat(fname).st_size==0
        
        fwrite = open(fname, 'a+', encoding='utf-8')

        if empty:
            header = 'hashtag'+sep+'sys_time'+sep+'user'+sep+'location'+sep+'image_description'+sep+'image_url'+sep+'image_type'+sep+'video_url'+sep+'verificated'+sep+'publications'+sep+'followers'+sep+'followed'+sep+'comment'+sep+'date_time'+'\n'
            fwrite.write(header)

        fwrite.write(line)
        fwrite.close()

#define execute scraper action
def execute_scraper():
    username_entry, password_entry, language_entry, search_entry, scroll_entry, articles_entry, \
        message_label = widgets

    global USERNAME 
    global PASSWORD
    global LANGUAGE
    global KEYWORD
    global NSCROLL
    global NARTICLES

    USERNAME = username_entry.get()
    PASSWORD = password_entry.get()
    LANGUAGE = language_entry.get()
    KEYWORD = '#'+search_entry.get()
    NSCROLL = int(scroll_entry.get())
    NARTICLES = int(articles_entry.get())
    
    message_label.config(text='')

    if USERNAME!=None and USERNAME!=''\
        and PASSWORD!=None and PASSWORD!=''\
        and LANGUAGE!=None and LANGUAGE!=''\
        and KEYWORD!=None and KEYWORD!=''\
        and NSCROLL!=None and NSCROLL>0\
        and NARTICLES!=None and NARTICLES>0:
        print(USERNAME, PASSWORD, LANGUAGE, KEYWORD, NSCROLL, NARTICLES)
        message_label.config(text='Procesando')
        start_scraper_ins()
        message_label.config(text='Terminado')
    else:
        message_label.config(text='(*) Los campos marcados son obligatorios')

#define main screen
def main_screen(root):
    root.title('Scraper Instagram')
    root.geometry('550x350')

    FONT = ('Helvetica', 11)

    #username
    username_label = tk.Label(root, text='Teléfono, usuario o correo electrónico*', font=FONT)
    username_label.grid(column=0, row=0, padx=10, pady=10)

    username_entry = tk.Entry(root, font=FONT)
    username_entry.grid(column=1, row=0, padx=10, pady=10)

    #password
    password_label = tk.Label(root, text='Contraseña*', font=FONT)
    password_label.grid(column=0, row=1, padx=10, pady=10)

    password_entry = tk.Entry(root, show='*', font=FONT)
    password_entry.grid(column=1, row=1, padx=10, pady=10)

    #language
    language_label = tk.Label(root, text='Idioma del Sistema Operativo*', font=FONT)
    language_label.grid(column=0, row=2, padx=10, pady=10)

    language_options = ['spanish', 'english']
    language_combo = ttk.Combobox(root, value=language_options, state='readonly', font=FONT, width=18)
    language_combo.grid(column=1, row=2, padx=10, pady=10)
    language_combo.current(0)

    #search
    search_label = tk.Label(root, text='Texto a buscar*', font=FONT)
    search_label.grid(column=0, row=3, padx=10, pady=10)

    search_entry = tk.Entry(root, font=FONT)
    search_entry.grid(column=1, row=3, padx=10, pady=10)

    #scroll
    scroll_label = tk.Label(root, text='Número desplazamientos después de buscar*', font=FONT)
    scroll_label.grid(column=0, row=4, padx=10, pady=10)

    scroll_entry = tk.Entry(root, font=FONT)
    scroll_entry.insert(tk.END, '2')
    scroll_entry.grid(column=1, row=4, padx=10, pady=10)
    
    #articles
    articles_label = tk.Label(root, text='Número publicaciones o artículos a buscar*', font=FONT)
    articles_label.grid(column=0, row=5, padx=10, pady=10)

    articles_entry = tk.Entry(root, font=FONT)
    articles_entry.insert(tk.END, '5')
    articles_entry.grid(column=1, row=5, padx=10, pady=10)
    
    #message
    message_label = tk.Label(root, text='')
    message_label.grid(column=0, row=6, padx=10, pady=5)

    #button
    exec_scraper_button = tk.Button(root, text='Ejecutar', fg='#fff', bg='#3582e8', font=FONT, command=execute_scraper)
    exec_scraper_button.grid(column=1, row=7, padx=10, pady=10)

    return username_entry, password_entry, language_combo, search_entry, scroll_entry, articles_entry, message_label

#start main
main_window = tk.Tk()
widgets = main_screen(main_window)
main_window.mainloop()
