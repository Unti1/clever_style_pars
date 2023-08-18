from settings import *
import time, os


class Pars():
    def __init__(self, invisable=False) -> None:
        """Шаблон для парсера с антидетект браузером Dolphin Anty

        Args:
            profile_id (str, optional): профиль ID от бразуера.
            invisable (bool, optional): запуск в свернутом режиме. Defaults to False.
            Версии эмуляторов: https://anty.dolphin.ru.com/docs/basic-automation/
            Для Linux сделать предвартилеьно chmo+x ..utils/cromedriver-linux
        """
        self._invis = invisable
        self.file_bizy = False
        self.running_times = 0
        self.driver = self.based_browser_startUp(invisable) # обычный запуск без dolphin
        #self.dolphin_browser_startUp(False) # запуск c dolphin
        self.wait = WebDriverWait(self.driver,6)
        self.main_data = {}
    
    def process_monitor(self):
        while True in list(map(lambda x: self.thread_dict[x][0].is_alive(),self.thread_dict)):    
            if platform.system() != "Linux":
                clear_command = "CLS"
            else:
                clear_command = "clear"

            os.system(clear_command)
            print("===="*20)
            for proc in self.thread_dict:
                print(f"ID: {self.thread_dict[proc][0].name}| Работает?: {self.thread_dict[proc][0].is_alive()} | Статус: {self.thread_dict[proc][1]}")
            print("===="*20)
        else:
            return 0

    def authorithation(self,driver):
        driver.get("https://clever-style.ru/catalog/")
        # //div[@data-modal="auth"]/span - вход кнопка
        WebDriverWait(driver,6).until(EC.element_to_be_clickable((By.XPATH,"//div[@data-modal='auth']/span")))
        driver.find_element(By.XPATH,"//div[@data-modal='auth']/span").click()

        # //input[@name="email"] - почта
        # //input[@name="password"] - пароль
        WebDriverWait(driver,6).until(EC.element_to_be_clickable((By.XPATH,"//input[@name='email']")))
        driver.find_element(By.XPATH,"//input[@name='email']").send_keys("kashaewa.oxana@yandex.ru")
        driver.find_element(By.XPATH,"//input[@name='password']").send_keys("210807Martin220485Tatyana")

        # //form[@class="auth__form form js-auth-form"]//button[@type="submit"] - кнопка входа
        WebDriverWait(driver,6).until(EC.element_to_be_clickable((By.XPATH,'//form[@class="auth__form form js-auth-form"]//button[@type="submit"]')))
        driver.find_element(By.XPATH, '//form[@class="auth__form form js-auth-form"]//button[@type="submit"]').click()
        time.sleep(2)

    def based_browser_startUp(self, invisable):
        self.running_times += 1
        options = webdriver.ChromeOptions()
        if invisable:
            options.add_argument('--headless')
        # Отключаем уведомления
        options.add_argument("--disable-notifications")
        # Отключаем логирование
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # Обработчик для нескольких драйверов
        if self.running_times == 1:
            exc_path = ChromeDriverManager().install()
            print("Путь основного ядра: ", exc_path)
        else:
            print("Основное ядро занято, создаю новое для отдельного потока")
            if platform.system() != "Linux":
                exc_path = ChromeDriverManager().install()
                exc_path = exc_path.replace("/","\\")
                exc_path = exc_path.rsplit("\\",maxsplit=1)
                exc_path[-1] = exc_path[-1].replace('.',f'_{self.running_times}.')
                copy_name = "\\".join(exc_path)
                exc_path = ChromeDriverManager().install()

                if not os.path.exists(copy_name):
                    shutil.copy2(exc_path, copy_name)            
                    while not os.path.exists(copy_name):
                        time.sleep(0.1)
                    exc_path = copy_name
                    print(f"Новое ядро расположено по пути: {copy_name}")
                else:
                    exc_path = copy_name
            else:
                exc_path = ChromeDriverManager().install()
        driver = webdriver.Chrome(executable_path=exc_path, options=options)
        driver.set_window_size(1920, 1080)
        return driver
    
    def remove_last_files(self):
        import shutil,os
        folder_path = 'data'  # Путь к папке data
        # Удалить папку "data" со всем ее содержимым
        shutil.rmtree(folder_path)
        # Создать пустую папку "data"
        os.mkdir(folder_path)

    def write_to_csv(self, filename, data, key_stat = ""):
        import csv
        self.file_bizy = True
        self.thread_dict[key_stat][1] = f"> Сохраняю \"{filename}.csv\" в папку \"data\""
        # Открываем файл в режиме дозаписи ('a') или создаем новый файл ('w')
        with open(f"data/{filename}.csv", 'w', newline='', encoding='cp1251') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            #(title, base_cost, sale_cost, articul, sizes, colors, description, img)
            # Добавляем заголовки колонок
            header = ['Название', 'Базовая цена', 'Цена со скидкой', 'Артикул','Размеры','Цвет','Описание','Фото']  # Замените на свои заголовки
            writer.writerow(header)
            # Записываем каждую строку данных в файл CSV
            for row in data:
                writer.writerow(row)  
        self.thread_dict[key_stat][1] = f"> Данные сохранены"
        self.file_bizy = False
        
    def file_exists(self, filename):
        try:
            with open(f'data/{filename}.csv', 'r') as file:
                return True
        except FileNotFoundError:
            return False

    def catalog(self):
        action = ActionChains(self.driver,250)
        self.driver.get("https://clever-style.ru/catalog/")
        self.wait.until(EC.element_to_be_clickable((By.XPATH,'//a[@href="/catalog/zhenskoe/"]'))) # ожидание
        try:
            for el in self.driver.find_elements(By.XPATH,"//nav/section/button"):
                action.move_to_element(el)
                action.click(el)
                action.perform()  
        except:
            pass
        time.sleep(2)
        catalog_links = []
        sections = self.driver.find_elements(By.XPATH,"//nav/section")
        for i in range(len(sections)):
            catalog = self.driver.find_element(By.XPATH,f"//nav/section[{i+1}]/h2").text
            catalog_links.append(list(
                    map(
                        lambda x: [ f"{catalog}-{x.text}", x.get_attribute('href')],
                        self.driver.find_elements(By.XPATH,f"//nav/section[{i+1}]/ul/li/a")
                    )
                ))
        return(sum(catalog_links,[]))

    def sale_catalog(self,catalog_data:list[str,str]):
        sale_link = catalog_data[1][:catalog_data[1].find('catalog/') + len('catalog/')] + "sale/" + catalog_data[1][catalog_data[1].find('catalog/') + len("catalog/"):]
        regenerate_data = [catalog_data[0],sale_link]
        return(regenerate_data)

    def subcatalogs(self,catalog_data):
        """Позволяет получить все ссылки на подкаталоги на сайте

        Args:
            catalog_data (_type_): _description_
        """
        cat_name = catalog_data[0]
        self.driver.get(catalog_data[1])
        try:
            self.driver.find_element(By.XPATH,"//section/div/button").click()# ещё
            # time.sleep(1.2)
        except:
            pass
        try:
            return(list(map(lambda x: (cat_name + '-Распродажа' if 'распродажа' in x.text.lower() else cat_name, x.get_attribute("href")),self.driver.find_elements(By.XPATH,"/html/body/main/div/section/div[1]/div/ul/li/a"))))
            # return(list(map(lambda x: cat_name +,self.driver.find_elements(By.XPATH,"/html/body/main/div/section/div[1]/div/ul/li/a"))))
        except:
            return None

    def parse_subcatalog_page_links(self,driver:webdriver.Chrome, link):
        driver.get(link)
        # //a[@class="card-product js-card-product"]
        links_list = []
        try: 
            page_num = int(driver.find_elements(By.XPATH,'//a[@class="paginations__item"]')[-2].text)
        except:
            page_num = 1
        for i in range(page_num):
            links_list.extend(list(map(lambda x: x.get_attribute('href'),driver.find_elements(By.XPATH,'//a[@class="card-product js-card-product"]'))))
            if page_num != 1 and i != page_num-1:
                driver.find_elements(By.XPATH,'//a[@class="paginations__item"]')[-1].click()
        return(links_list)
    
    def remove_duplicates(self, lst):
        unique_list = list(set(map(tuple, lst)))
        return [list(sublist) for sublist in unique_list]

    def parse_subcatalogs(self,driver: webdriver.Chrome, subcatalogs:list[tuple], test=False, key_stat = ""):
        """Основной модуль парсинга

        Args:
            subcatalogs (_type_): [(подкаталог, ссылки подкаталога), ...]
        """
        try:
            self.authorithation(driver)
        except:
            logging.info(traceback.format_exc())

        for s in subcatalogs:
            tovar_data = []
            try:
                title = s[0]
                self.thread_dict[key_stat][1] = f"Начинаю сбор для \"{title}\""
                if test == False:
                    links = self.parse_subcatalog_page_links(driver, s[-1]) # собирает ссылки на товари из подкаталога
                else:
                    links = self.parse_subcatalog_page_links(driver, s[-1])
                    if len(links) > 0:
                        links = links[:10]
                self.thread_dict[key_stat][1] = f"> Получены {len(links)} ссылок на товар. Собираю информацию..."
                # собирает конкретные значения из товаров
                
                for step,link in enumerate(links):
                    self.thread_dict[key_stat][1] = f">Просмотренно: [{step+1}/{len(links)}] | {title}"
                    tovar = list(self.single_tovar_grab(driver, link))
                    
                    # Разбиение по сраным цветам с зависимостью в виде размера
                    colors = tovar[5]
                    sizes = tovar[4]
                    img = tovar[-1]
                    # print(tovar)
                    if len(colors) > 1:
                        for i in range(len(colors)):
                            new_tovar = tovar
                            new_tovar[5] = colors[i]
                            new_tovar[4] = sizes[i]
                            new_tovar[-1] = img[i]
                            tovar_data.append(new_tovar)
                    else:
                        if type(tovar[5]) == list:
                            colors = ";".join(tovar[5])
                            tovar[5] = colors
                        if type(tovar[4]) == list:
                            sizes = ";".join(tovar[4])
                            tovar[4] = sizes
                        if type(tovar[-1]) == list:
                            img = ";".join(tovar[-1])
                            tovar[-1] = img
                        tovar_data.append(tovar)

                # Очистка дублей и сохранение информации
                if tovar_data != []:
                    if self.main_data.get(title) != None:
                        self.main_data[title] = self.remove_duplicates(sum([self.main_data[title],tovar_data],[]))
                        tovar_data = []
                        self.sigment_catalog(key_stat = key_stat)

                    else:
                        self.main_data[title] = self.remove_duplicates(tovar_data)
                        tovar_data = []
                        self.sigment_catalog(key_stat = key_stat)                       
                else:
                    self.thread_dict[key_stat][1] = "Каталог пуст"
                    tovar_data = []
            except:
                tovar_data = []
                logging.error(f"Ошибка сбора данных в каталоге {s[0]} \n{traceback.format_exc()}\n -- Набор данных --> {tovar_data}")
        return
    
    def sigment_catalog(self, key_stat = ""):
        while self.file_bizy:
            time.sleep(0.2)
        else:
            for title,value in self.main_data.items():
                self.write_to_csv(title,value,key_stat = key_stat)
                
    def single_tovar_grab(self,driver: webdriver.Chrome, link: str):
        driver.get(link)
        action = ActionChains(driver,250)
        try:
            more = driver.find_element(By.XPATH,'//section[1]/div/div[2]/section[3]/button')
            action.move_to_element(more)
            action.click(more)
            action.perform()
            time.sleep(0.25)
        except: 
            pass
        
        WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'//h1[@class="product__title main-title"]')))
        title = driver.find_element(By.XPATH,'//h1[@class="product__title main-title"]').text.replace("\n","")

        about_tovar = driver.find_elements(By.XPATH,'//div[@class="product-about__list-item js-product-qualities-item"]')
        articul = ""
        for about in about_tovar:
            if "Артикул" in about.text:
                articul = about.text.replace("\n","").replace("Артикул:","")
        if articul == "":
            articul = "Не найден" 
        
        colors = []
        sizes = [] # зависит от colors
        counts = [] # зависит от sizes
        img = []
        try:
            for index,color_button in enumerate(driver.find_elements(By.XPATH,'//section[1]/div[2]/div//button')):
                action.move_to_element(color_button)
                action.click(color_button)
                action.perform()
                sizes.append(
                    ";".join(
                            list(map(lambda x: x.text, driver.find_elements(By.XPATH,'//div[@class="product-sizes__size js-size-wrap positioned-right"]/button')))
                        )
                    )
                colors.append( driver.find_element(By.XPATH,'//span[@class="product-color__name js-color-name"]').text )
                
                try:                    
                    img.append(";".join(
                        list(
                            map(lambda x: x.get_attribute("src"), 
                                driver.find_elements(By.XPATH,'//div[@class="product__slider-container visible"]//img')
                                )
                            )))
                except:
                    img.append("Не найдены")
                """блок с добавлением количества товара"""
                # //section[2]/div[i]/div//input[@class="counter js-counter"]
                try:
                    all_counts = list(map(lambda x: x.get_attribute('max'),driver.find_elements(By.XPATH,f'//section[2]/div[{index+1}]/div//input[@class="counter js-counter"]')))
                    all_counts = list(filter(lambda x: x !="0",all_counts))                          
                    counts.append(";".join(all_counts))
                except:
                    counts.append("-")
                    logging.info(traceback.format_exc())
        except:
            logging.error(traceback.format_exc())
            colors = []

        try:
            if colors == []:
                sizes = list(map(lambda x: x.text, driver.find_elements(By.XPATH,'//div[@class="product-sizes__size js-size-wrap positioned-right"]/button')))
                sizes = ";".join(sizes)
                try:
                    all_counts = list(map(lambda x: x.get_attribute('max'),driver.find_elements(By.XPATH,'//input[@class="counter js-counter"]')))
                    all_counts = list(filter(lambda x: x !="0",all_counts))                          
                    counts.append(";".join(all_counts))
                except:
                    counts.append("-")
                    logging.info(traceback.format_exc())
                try:
                    img = list(map(lambda x: x.get_attribute("src"), driver.find_elements(By.XPATH,'//div[@class="product__slider-container visible"]//img')))
                    img = ";".join(img)
                except:
                    img = "Не найдены"
        except:
            sizes = []
            counts = []
            img = []
        
        
        
        try:
            base_cost = driver.find_element(By.XPATH,'//b[@class="product__price-price js-basic-price"]').text
            base_cost = base_cost[:-4].replace(".",",").strip()
        except:
            base_cost = "Отсутствует"

        try:
            sale_cost = driver.find_element(By.XPATH,'//b[@class="product__price-price js-discount-price"]').text
            sale_cost = sale_cost[:-4].replace(".",",").strip()
            
        except:
            sale_cost = "Отсутствует"

        try:
            description = driver.find_element(By.XPATH,'//section[@class="product-descr hidden-mobile"]/p').text
        except exceptions.NoSuchElementException:
            description = "Отсутствует"
        
        

        return (title, base_cost, sale_cost, articul, sizes, colors, description, img)
    
    def test(self):
        self.remove_last_files()
        print("Авторизация",end=" ")
        self.authorithation(self.driver)
        print("[Успешно]")

        # catalog_data = self.catalog()
        # sale_cat = list(map(lambda x: self.sale_catalog(x),catalog_data))
        # catalog_data.extend(sale_cat)
        # catalog_data.reverse()
        # logging.info(f"Список каталогов - {catalog_data}")
        # subcatalogs = list(map(lambda data: self.subcatalogs(data),catalog_data))
        # print(subcatalogs)
        # subcatalogs = sum(subcatalogs,[])
        # subcatalogs = list(filter(lambda x: x != None, subcatalogs))
        # logging.info(f"Список подкаталогов - {subcatalogs}")
        
        subcatalogs = [('Постельные принадлежности-Одеяла-Распродажа', 'https://clever-style.ru/catalog/sale/postelnyeprinadlezhnosti/odeyala/detskie/'), ('Постельные принадлежности-Одеяла-Распродажа', 'https://clever-style.ru/catalog/sale/postelnyeprinadlezhnosti/odeyala/evro/'), ('Постельные принадлежности-Одеяла-Распродажа', 'https://clever-style.ru/catalog/sale/postelnyeprinadlezhnosti/odeyala/dvuspalnye/'), ('Постельные принадлежности-Одеяла-Распродажа', 'https://clever-style.ru/catalog/sale/postelnyeprinadlezhnosti/odeyala/polutornye/'), ('Постельные принадлежности-Подушки-Распродажа', 'https://clever-style.ru/catalog/sale/postelnyeprinadlezhnosti/podushki/odeyala_1/'), ('Постельные принадлежности-Подушки-Распродажа', 'https://clever-style.ru/catalog/sale/postelnyeprinadlezhnosti/podushki/70kh70/'), ('Постельные принадлежности-Подушки-Распродажа', 'https://clever-style.ru/catalog/sale/postelnyeprinadlezhnosti/podushki/60kh60/'), ('Постельные принадлежности-Подушки-Распродажа', 'https://clever-style.ru/catalog/sale/postelnyeprinadlezhnosti/podushki/drugierazmery/'), ('Детское-Шапки-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/shapki_1_1_1_1_1/shapki_1_1_1_1_1_1/'), ('Детское-Шапки-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/shapki_1_1_1_1_1/sharfysnudy_1_1_1/'), ('Детское-Шапки-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/shapki_1_1_1_1_1/letniegolovnyeubory_1_1_1/'), ('Детское-Ясли-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/yasli_1/futbolkidzhempery_1/'), ('Детское-Ясли-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/yasli_1/kombinezonybodi_1/'), ('Детское-Ясли-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/yasli_1/komplekty_1/'), ('Детское-Ясли-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/yasli_1/tolstovkikhudi/'), ('Детское-Носки-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/noski_1_1_1/noskidlyadevochki/'), ('Детское-Носки-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/noski_1_1_1/noskidlyamalchika/'), ('Детское-Носки-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/noski_1_1_1/teplye_1_1_1/'), ('Детское-Носки-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/noski_1_1_1/kolgotki_1_1/'), ('Детское-Мальчик-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/malchik_1/futbolkidzhempery/'), ('Детское-Мальчик-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/malchik_1/tolstovkikhudi_1_1_1_1_1_1/'), ('Детское-Мальчик-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/malchik_1/bryuki_1_1_1_1/'), ('Детское-Мальчик-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/malchik_1/shorty_1_1_1_1_1_1/'), ('Детское-Мальчик-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/malchik_1/pizhamykomplekty_1/'), ('Детское-Мальчик-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/malchik_1/zhaketykardigany_1/'), ('Детское-Мальчик-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/malchik_1/sorochkirubashki_1/'), ('Детское-Девочка-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/devochka_1/futbolkidzhempery_1_1_1/'), ('Детское-Девочка-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/devochka_1/platya/'), ('Детское-Девочка-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/devochka_1/bryuki_1_1_1/'), ('Детское-Девочка-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/devochka_1/losinylegginsy/'), ('Детское-Девочка-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/devochka_1/pizhamykomplekty/'), ('Детское-Девочка-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/devochka_1/tolstovkikhudi_1_1_1_1_1/'), ('Детское-Девочка-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/devochka_1/shorty_1_1_1_1_1/'), ('Детское-Девочка-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/devochka_1/yubki_1_1_1/'), ('Детское-Девочка-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/devochka_1/zhaketykardigany/'), ('Детское-Девочка-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/devochka_1/maykitopy_1/'), ('Детское-Девочка-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/devochka_1/sorochki/'), ('Детское-Девочка-Распродажа', 'https://clever-style.ru/catalog/sale/detskoe/devochka_1/bluzkirubashki/'), ('Мужское-Шапки-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/shapki_1_1/shapki_1_1_1/'), ('Мужское-Шапки-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/shapki_1_1/sharfysnudy_1/'), ('Мужское-Носки-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/noski_1/noski_1_1_1_1/'), ('Мужское-Носки-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/noski_1/teplye_1/'), ('Мужское-Носки-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/noski_1/noskidrugiemarki/'), ('Мужское-Одежда-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/odezhda_1/futbolkimayki_1/'), ('Мужское-Одежда-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/odezhda_1/dzhemperykardinany_1/'), ('Мужское-Одежда-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/odezhda_1/bryukidzhinsy_1/'), ('Мужское-Одежда-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/odezhda_1/shorty_1_1_1/'), ('Мужское-Одежда-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/odezhda_1/tolstovkikhudi_1_1_1/'), ('Мужское-Одежда-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/odezhda_1/pidzhaki_1/'), ('Мужское-Одежда-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/odezhda_1/rubashkisorochki_1/'), ('Мужское-Белье-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/bele_1/trusy_1/'), ('Мужское-Белье-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/bele_1/trusyfashion_1/'), ('Мужское-Белье-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/bele_1/maykifutbolki_1/'), ('Мужское-Домашняя одежда-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/domashnyayaodezhda_1/komplektypizhamy_1/'), ('Мужское-Домашняя одежда-Распродажа', 'https://clever-style.ru/catalog/sale/muzhskoe/domashnyayaodezhda_1/futbolkimayki/'), ('Женское-Аксессуары-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/aksessuary_1/povyazkadlyagolovy_1/'), ('Женское-Аксессуары-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/aksessuary_1/suveniry_1/'), ('Женское-Шапки, перчатки-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/shapki/shapki_1/'), ('Женское-Шапки, перчатки-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/shapki/sharfysnudy/'), ('Женское-Носки-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/noski/noski_1_1/'), ('Женское-Носки-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/noski/teplye/'), ('Женское-Носки-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/noski/kolgotkidrugiemarki/'), ('Женское-Носки-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/noski/noskidrugiemarki_1/'), ('Женское-Носки-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/noski/noskiigolfypadrugiemarki/'), ('Женское-Одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/odezhda/tolstovkikhudi_1_1/'), ('Женское-Одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/odezhda/dzhemperykardigany_1/'), ('Женское-Одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/odezhda/bryuki/'), ('Женское-Одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/odezhda/shorty_1/'), ('Женское-Одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/odezhda/platyasarafany_1/'), ('Женское-Одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/odezhda/kostyumtrikotazhnyy_1/'), ('Женское-Одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/odezhda/maykitopy_1_1_1_1/'), ('Женское-Одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/odezhda/bluzkirubashki_1/'), ('Женское-Одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/odezhda/yubki_1/'), ('Женское-Белье-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/bele/trusy/'), ('Женское-Белье-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/bele/trusyfashion/'), ('Женское-Белье-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/bele/maykitopy_1_1/'), ('Женское-Белье-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/bele/futbolki_1_1_1/'), ('Женское-Белье-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/bele/komplektbelevoy_1/'), ('Женское-Белье-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/bele/byustgalter_1/'), ('Женское-Белье-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/bele/kupalniki_1/'), ('Женское-Белье-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/bele/eroticheskoebele_1/'), ('Женское-Белье-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/bele/trusydrugiemarki/'), ('Женское-Домашняя одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/domashnyayaodezhda/komplektypizhamy/'), ('Женское-Домашняя одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/domashnyayaodezhda/tolstovkikhudi_1/'), ('Женское-Домашняя одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/domashnyayaodezhda/futbolki/'), ('Женское-Домашняя одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/domashnyayaodezhda/losinylegginsy_1/'), ('Женское-Домашняя одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/domashnyayaodezhda/bryukibridzhi_1/'), ('Женское-Домашняя одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/domashnyayaodezhda/shorty/'), ('Женское-Домашняя одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/domashnyayaodezhda/vodolazki_1/'), ('Женское-Домашняя одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/domashnyayaodezhda/platyasarafany/'), ('Женское-Домашняя одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/domashnyayaodezhda/khalaty_1_1_1/'), ('Женское-Домашняя одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/domashnyayaodezhda/sorochki_1/'), ('Женское-Домашняя одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/domashnyayaodezhda/yubki/'), ('Женское-Домашняя одежда-Распродажа', 'https://clever-style.ru/catalog/sale/zhenskoe/domashnyayaodezhda/kostyumy/'), ('Постельные принадлежности-Полотенца', 'https://clever-style.ru/catalog/postelnyeprinadlezhnosti/polotentsa/kukhonnye/'), ('Постельные принадлежности-Полотенца', 'https://clever-style.ru/catalog/postelnyeprinadlezhnosti/polotentsa/makhrovye/'), ('Постельные принадлежности-Матрасы', 'https://clever-style.ru/catalog/postelnyeprinadlezhnosti/matrasy/matrasy_1/'), ('Постельные принадлежности-Ортопедические подушки', 'https://clever-style.ru/catalog/postelnyeprinadlezhnosti/ortopedicheskiepodushki/ortopedicheskiepodushki_1/'), ('Постельные принадлежности-Одеяла', 'https://clever-style.ru/catalog/postelnyeprinadlezhnosti/odeyala/detskie/'), ('Постельные принадлежности-Одеяла', 'https://clever-style.ru/catalog/postelnyeprinadlezhnosti/odeyala/evro/'), ('Постельные принадлежности-Одеяла', 'https://clever-style.ru/catalog/postelnyeprinadlezhnosti/odeyala/dvuspalnye/'), ('Постельные принадлежности-Одеяла', 'https://clever-style.ru/catalog/postelnyeprinadlezhnosti/odeyala/polutornye/'), ('Постельные принадлежности-Подушки', 'https://clever-style.ru/catalog/postelnyeprinadlezhnosti/podushki/odeyala_1/'), ('Постельные принадлежности-Подушки', 'https://clever-style.ru/catalog/postelnyeprinadlezhnosti/podushki/70kh70/'), ('Постельные принадлежности-Подушки', 'https://clever-style.ru/catalog/postelnyeprinadlezhnosti/podushki/60kh60/'), ('Постельные принадлежности-Подушки', 'https://clever-style.ru/catalog/postelnyeprinadlezhnosti/podushki/drugierazmery/'), ('Детское-Термобелье', 'https://clever-style.ru/catalog/detskoe/termobele_1_1/termobele_1_1_1_1/'), ('Детское-Шапки', 'https://clever-style.ru/catalog/detskoe/shapki_1_1_1_1_1/shapki_1_1_1_1_1_1/'), ('Детское-Шапки', 'https://clever-style.ru/catalog/detskoe/shapki_1_1_1_1_1/sharfysnudy_1_1_1/'), ('Детское-Шапки', 'https://clever-style.ru/catalog/detskoe/shapki_1_1_1_1_1/letniegolovnyeubory_1_1_1/'), ('Детское-Ясли', 'https://clever-style.ru/catalog/detskoe/yasli_1/futbolkidzhempery_1/'), ('Детское-Ясли', 'https://clever-style.ru/catalog/detskoe/yasli_1/kombinezonybodi_1/'), ('Детское-Ясли', 'https://clever-style.ru/catalog/detskoe/yasli_1/bryuki_1_1_1_1_1/'), ('Детское-Ясли', 'https://clever-style.ru/catalog/detskoe/yasli_1/komplekty_1/'), ('Детское-Ясли', 'https://clever-style.ru/catalog/detskoe/yasli_1/platya_1/'), ('Детское-Ясли', 'https://clever-style.ru/catalog/detskoe/yasli_1/tolstovkikhudi/'), ('Детское-Носки', 'https://clever-style.ru/catalog/detskoe/noski_1_1_1/noskidlyadevochki/'), ('Детское-Носки', 'https://clever-style.ru/catalog/detskoe/noski_1_1_1/noskidlyamalchika/'), ('Детское-Носки', 'https://clever-style.ru/catalog/detskoe/noski_1_1_1/teplye_1_1_1/'), ('Детское-Носки', 'https://clever-style.ru/catalog/detskoe/noski_1_1_1/kolgotki_1_1/'), ('Детское-Носки', 'https://clever-style.ru/catalog/detskoe/noski_1_1_1/yasli/'), ('Детское-Мальчик', 'https://clever-style.ru/catalog/detskoe/malchik_1/futbolkidzhempery/'), ('Детское-Мальчик', 'https://clever-style.ru/catalog/detskoe/malchik_1/tolstovkikhudi_1_1_1_1_1_1/'), ('Детское-Мальчик', 'https://clever-style.ru/catalog/detskoe/malchik_1/bryuki_1_1_1_1/'), ('Детское-Мальчик', 'https://clever-style.ru/catalog/detskoe/malchik_1/shorty_1_1_1_1_1_1/'), ('Детское-Мальчик', 'https://clever-style.ru/catalog/detskoe/malchik_1/pizhamykomplekty_1/'), ('Детское-Мальчик', 'https://clever-style.ru/catalog/detskoe/malchik_1/zhaketykardigany_1/'), ('Детское-Мальчик', 'https://clever-style.ru/catalog/detskoe/malchik_1/sorochkirubashki_1/'), ('Детское-Мальчик', 'https://clever-style.ru/catalog/detskoe/malchik_1/khalaty_1_1/'), ('Детское-Мальчик', 'https://clever-style.ru/catalog/detskoe/malchik_1/bele_1_1_1/'), ('Детское-Девочка', 'https://clever-style.ru/catalog/detskoe/devochka_1/futbolkidzhempery_1_1_1/'), ('Детское-Девочка', 'https://clever-style.ru/catalog/detskoe/devochka_1/platya/'), ('Детское-Девочка', 'https://clever-style.ru/catalog/detskoe/devochka_1/bryuki_1_1_1/'), ('Детское-Девочка', 'https://clever-style.ru/catalog/detskoe/devochka_1/losinylegginsy/'), ('Детское-Девочка', 'https://clever-style.ru/catalog/detskoe/devochka_1/pizhamykomplekty/'), ('Детское-Девочка', 'https://clever-style.ru/catalog/detskoe/devochka_1/tolstovkikhudi_1_1_1_1_1/'), ('Детское-Девочка', 'https://clever-style.ru/catalog/detskoe/devochka_1/shorty_1_1_1_1_1/'), ('Детское-Девочка', 'https://clever-style.ru/catalog/detskoe/devochka_1/yubki_1_1_1/'), ('Детское-Девочка', 'https://clever-style.ru/catalog/detskoe/devochka_1/zhaketykardigany/'), ('Детское-Девочка', 'https://clever-style.ru/catalog/detskoe/devochka_1/maykitopy_1/'), ('Детское-Девочка', 'https://clever-style.ru/catalog/detskoe/devochka_1/sorochki/'), ('Детское-Девочка', 'https://clever-style.ru/catalog/detskoe/devochka_1/khalaty_1/'), ('Детское-Девочка', 'https://clever-style.ru/catalog/detskoe/devochka_1/bluzkirubashki/'), ('Детское-Девочка', 'https://clever-style.ru/catalog/detskoe/devochka_1/bele_1_1/'), ('Детское-Девочка', 'https://clever-style.ru/catalog/detskoe/devochka_1/kupalniki/'), ('Мужское-Аксессуары', 'https://clever-style.ru/catalog/muzhskoe/aksessuary/upakovka_1/'), ('Мужское-Шапки', 'https://clever-style.ru/catalog/muzhskoe/shapki_1_1/shapki_1_1_1/'), ('Мужское-Шапки', 'https://clever-style.ru/catalog/muzhskoe/shapki_1_1/sharfysnudy_1/'), ('Мужское-Шапки', 'https://clever-style.ru/catalog/muzhskoe/shapki_1_1/letniegolovnyeubory_1/'), ('Мужское-Носки', 'https://clever-style.ru/catalog/muzhskoe/noski_1/noski_1_1_1_1/'), ('Мужское-Носки', 'https://clever-style.ru/catalog/muzhskoe/noski_1/podsledniki_1_1_1_1_1/'), ('Мужское-Носки', 'https://clever-style.ru/catalog/muzhskoe/noski_1/teplye_1/'), ('Мужское-Носки', 'https://clever-style.ru/catalog/muzhskoe/noski_1/noskidrugiemarki/'), ('Мужское-Одежда', 'https://clever-style.ru/catalog/muzhskoe/odezhda_1/futbolkimayki_1/'), ('Мужское-Одежда', 'https://clever-style.ru/catalog/muzhskoe/odezhda_1/dzhemperykardinany_1/'), ('Мужское-Одежда', 'https://clever-style.ru/catalog/muzhskoe/odezhda_1/bryukidzhinsy_1/'), ('Мужское-Одежда', 'https://clever-style.ru/catalog/muzhskoe/odezhda_1/shorty_1_1_1/'), ('Мужское-Одежда', 'https://clever-style.ru/catalog/muzhskoe/odezhda_1/tolstovkikhudi_1_1_1/'), ('Мужское-Одежда', 'https://clever-style.ru/catalog/muzhskoe/odezhda_1/pidzhaki_1/'), ('Мужское-Одежда', 'https://clever-style.ru/catalog/muzhskoe/odezhda_1/rubashkisorochki_1/'), ('Мужское-Белье', 'https://clever-style.ru/catalog/muzhskoe/bele_1/trusy_1/'), ('Мужское-Белье', 'https://clever-style.ru/catalog/muzhskoe/bele_1/trusyfashion_1/'), ('Мужское-Белье', 'https://clever-style.ru/catalog/muzhskoe/bele_1/maykifutbolki_1/'), ('Мужское-Белье', 'https://clever-style.ru/catalog/muzhskoe/bele_1/termobele_1/'), ('Мужское-Белье', 'https://clever-style.ru/catalog/muzhskoe/bele_1/kupalnyeshortyplavki_1/'), ('Мужское-Домашняя одежда', 'https://clever-style.ru/catalog/muzhskoe/domashnyayaodezhda_1/komplektypizhamy_1/'), ('Мужское-Домашняя одежда', 'https://clever-style.ru/catalog/muzhskoe/domashnyayaodezhda_1/futbolkimayki/'), ('Мужское-Домашняя одежда', 'https://clever-style.ru/catalog/muzhskoe/domashnyayaodezhda_1/bryuki_1/'), ('Мужское-Домашняя одежда', 'https://clever-style.ru/catalog/muzhskoe/domashnyayaodezhda_1/shorty_1_1/'), ('Мужское-Домашняя одежда', 'https://clever-style.ru/catalog/muzhskoe/domashnyayaodezhda_1/khalaty_1_1_1_1/'), ('Женское-Аксессуары', 'https://clever-style.ru/catalog/zhenskoe/aksessuary_1/povyazkadlyagolovy_1/'), ('Женское-Аксессуары', 'https://clever-style.ru/catalog/zhenskoe/aksessuary_1/povyazkadlyaglaz_1/'), ('Женское-Аксессуары', 'https://clever-style.ru/catalog/zhenskoe/aksessuary_1/obuv_1/'), ('Женское-Аксессуары', 'https://clever-style.ru/catalog/zhenskoe/aksessuary_1/suveniry_1/'), ('Женское-Аксессуары', 'https://clever-style.ru/catalog/zhenskoe/aksessuary_1/prochee_1/'), ('Женское-Аксессуары', 'https://clever-style.ru/catalog/zhenskoe/aksessuary_1/upakovka/'), ('Женское-Шапки, перчатки', 'https://clever-style.ru/catalog/zhenskoe/shapki/shapki_1/'), ('Женское-Шапки, перчатки', 'https://clever-style.ru/catalog/zhenskoe/shapki/sharfysnudy/'), ('Женское-Шапки, перчатки', 'https://clever-style.ru/catalog/zhenskoe/shapki/varezhkiperchatki/'), ('Женское-Шапки, перчатки', 'https://clever-style.ru/catalog/zhenskoe/shapki/letniegolovnyeubory/'), ('Женское-Носки', 'https://clever-style.ru/catalog/zhenskoe/noski/noski_1_1/'), ('Женское-Носки', 'https://clever-style.ru/catalog/zhenskoe/noski/podsledniki_1_1_1_1/'), ('Женское-Носки', 'https://clever-style.ru/catalog/zhenskoe/noski/kolgotki_1_1_1/'), ('Женское-Носки', 'https://clever-style.ru/catalog/zhenskoe/noski/teplye/'), ('Женское-Носки', 'https://clever-style.ru/catalog/zhenskoe/noski/kolgotkidrugiemarki/'), ('Женское-Носки', 'https://clever-style.ru/catalog/zhenskoe/noski/noskidrugiemarki_1/'), ('Женское-Носки', 'https://clever-style.ru/catalog/zhenskoe/noski/noskiigolfypadrugiemarki/'), ('Женское-Одежда', 'https://clever-style.ru/catalog/zhenskoe/odezhda/tolstovkikhudi_1_1/'), ('Женское-Одежда', 'https://clever-style.ru/catalog/zhenskoe/odezhda/dzhemperykardigany_1/'), ('Женское-Одежда', 'https://clever-style.ru/catalog/zhenskoe/odezhda/bryuki/'), ('Женское-Одежда', 'https://clever-style.ru/catalog/zhenskoe/odezhda/shorty_1/'), ('Женское-Одежда', 'https://clever-style.ru/catalog/zhenskoe/odezhda/platyasarafany_1/'), ('Женское-Одежда', 'https://clever-style.ru/catalog/zhenskoe/odezhda/kostyumtrikotazhnyy_1/'), ('Женское-Одежда', 'https://clever-style.ru/catalog/zhenskoe/odezhda/maykitopy_1_1_1_1/'), ('Женское-Одежда', 'https://clever-style.ru/catalog/zhenskoe/odezhda/bluzkirubashki_1/'), ('Женское-Одежда', 'https://clever-style.ru/catalog/zhenskoe/odezhda/yubki_1/'), ('Женское-Белье', 'https://clever-style.ru/catalog/zhenskoe/bele/trusy/'), ('Женское-Белье', 'https://clever-style.ru/catalog/zhenskoe/bele/trusyfashion/'), ('Женское-Белье', 'https://clever-style.ru/catalog/zhenskoe/bele/maykitopy_1_1/'), ('Женское-Белье', 'https://clever-style.ru/catalog/zhenskoe/bele/futbolki_1_1_1/'), ('Женское-Белье', 'https://clever-style.ru/catalog/zhenskoe/bele/komplektbelevoy_1/'), ('Женское-Белье', 'https://clever-style.ru/catalog/zhenskoe/bele/bodi_1/'), ('Женское-Белье', 'https://clever-style.ru/catalog/zhenskoe/bele/byustgalter_1/'), ('Женское-Белье', 'https://clever-style.ru/catalog/zhenskoe/bele/termobele/'), ('Женское-Белье', 'https://clever-style.ru/catalog/zhenskoe/bele/kupalniki_1/'), ('Женское-Белье', 'https://clever-style.ru/catalog/zhenskoe/bele/eroticheskoebele_1/'), ('Женское-Белье', 'https://clever-style.ru/catalog/zhenskoe/bele/zakupnoekorsetnoebele/'), ('Женское-Белье', 'https://clever-style.ru/catalog/zhenskoe/bele/trusydrugiemarki/'), ('Женское-Домашняя одежда', 'https://clever-style.ru/catalog/zhenskoe/domashnyayaodezhda/komplektypizhamy/'), ('Женское-Домашняя одежда', 'https://clever-style.ru/catalog/zhenskoe/domashnyayaodezhda/tolstovkikhudi_1/'), ('Женское-Домашняя одежда', 'https://clever-style.ru/catalog/zhenskoe/domashnyayaodezhda/futbolki/'), ('Женское-Домашняя одежда', 'https://clever-style.ru/catalog/zhenskoe/domashnyayaodezhda/losinylegginsy_1/'), ('Женское-Домашняя одежда', 'https://clever-style.ru/catalog/zhenskoe/domashnyayaodezhda/bryukibridzhi_1/'), ('Женское-Домашняя одежда', 'https://clever-style.ru/catalog/zhenskoe/domashnyayaodezhda/shorty/'), ('Женское-Домашняя одежда', 'https://clever-style.ru/catalog/zhenskoe/domashnyayaodezhda/vodolazki_1/'), ('Женское-Домашняя одежда', 'https://clever-style.ru/catalog/zhenskoe/domashnyayaodezhda/platyasarafany/'), ('Женское-Домашняя одежда', 'https://clever-style.ru/catalog/zhenskoe/domashnyayaodezhda/khalaty_1_1_1/'), ('Женское-Домашняя одежда', 'https://clever-style.ru/catalog/zhenskoe/domashnyayaodezhda/sorochki_1/'), ('Женское-Домашняя одежда', 'https://clever-style.ru/catalog/zhenskoe/domashnyayaodezhda/yubki/'), ('Женское-Домашняя одежда', 'https://clever-style.ru/catalog/zhenskoe/domashnyayaodezhda/kostyumy/')]
        self.multythread_parse(subcatalogs,test = True)
        print("Конец работы парсера")

    def test_pravki(self):
        self.authorithation()
        tovar_data = []
        tovar = list(self.single_tovar_grab("https://clever-style.ru/catalog/muzhskoe/bele_1/termobele_1/clemhp600320nachkomplektbelevoymuzhskoy/"))
        # tovar = list(self.single_tovar_grab("https://clever-style.ru/catalog/detskoe/noski_1_1_1/noskidlyadevochki/cles4287202222noskidetskie/"))
        
        colors = tovar[5]
        sizes = tovar[4]
        img = tovar[-1]
        
        if len(colors) > 1:
            print(sizes,colors)
            for i in range(len(colors)):
                new_tovar = tovar
                new_tovar[5] = colors[i]
                new_tovar[4] = sizes[i]
                new_tovar[-1] = img[i]
                print('new_tovar --->',new_tovar)
                tovar_data.append(new_tovar)
        else:
            tovar_data.append(tovar)
        print('tovar_data ---> ', tovar_data)

    def main(self):
        print(f"Будет задействованно {os.cpu_count()} потоков для работы")
        print("Удаление прошлых сессий...")
        self.remove_last_files()
        print("Авторизация...", end=" ")
        self.authorithation(self.driver)
        print('[Успешно]')
        print("Собираю каталоги...",end=" ")
        catalog_data = self.catalog()
        sale_cat = list(map(lambda x: self.sale_catalog(x),catalog_data))
        catalog_data.extend(sale_cat)
        catalog_data.reverse()
        print("[Успешно]")
        logging.info(f"Список каталогов - {catalog_data}")
        print("Собираю подкаталоги...",end = "")
        subcatalogs = list(map(lambda data: self.subcatalogs(data),catalog_data))
        subcatalogs = sum(subcatalogs,[])
        subcatalogs = list(filter(lambda x: x != None, subcatalogs))
        print("[Успешно]")
        logging.info(f"Список подкаталогов - {subcatalogs}")
        self.multythread_parse(subcatalogs)
        print("Конец работы парсера")
        self.driver.quit()
    
    def split_list(self,lst, n):
        # Рассчитываем размер каждого куска
        chunk_size = len(lst) // n

        # Разбиваем список на куски
        divided_list = [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

        if len(divided_list) != n:
            divided_list[-2].extend(divided_list[-1])
            divided_list.pop(-1)
        return divided_list
    
    def multythread_parse(self,subcatalogs,test = False):
        from threading import Thread    
        thread_count: int = os.cpu_count() - 1
        self.thread_dict: dict = {}
        working_lists = self.split_list(subcatalogs, thread_count)

        for sub_catalogs in working_lists:
            thread_name = f"Thread-{len(self.thread_dict)}"
            if sub_catalogs == working_lists[0]:
                if test == False:
                    t = Thread(target=self.parse_subcatalogs,args=(self.driver, sub_catalogs,False,thread_name,))
                else:
                    t = Thread(target=self.parse_subcatalogs,args=(self.driver,sub_catalogs,test,thread_name,))
            else:
                if test == False:
                    driver = self.based_browser_startUp(self._invis)
                    t = Thread(target=self.parse_subcatalogs,args=(driver, sub_catalogs,False,thread_name,))
                else:
                    driver = self.based_browser_startUp(self._invis)
                    t = Thread(target=self.parse_subcatalogs,args=(driver,sub_catalogs,test,thread_name,))

            self.thread_dict[thread_name] = [t,'Не определен']
        monithor = Thread(target=self.process_monitor)
        for key in self.thread_dict:
            self.thread_dict[key][0].start()
        monithor.start()

        for key in self.thread_dict:
            self.thread_dict[key][0].join()
        
    
