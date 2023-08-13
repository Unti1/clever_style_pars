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
        self.action = ActionChains(self.driver,250)
        self.main_data = {}
    
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
            print("Основное ядро занято, создаю новое")
            
            exc_path = ChromeDriverManager().install()
            exc_path = exc_path.rsplit("/",maxsplit=1)
            exc_path[-1] = exc_path[-1].replace('.',f'_{self.running_times}.')
            copy_name = "/".join(exc_path)
            exc_path = ChromeDriverManager().install()

            if not os.path.exists(copy_name):
                shutil.copy2(exc_path, copy_name)            
                while not os.path.exists(copy_name):
                    time.sleep(0.1)
                exc_path = copy_name
                print(f"Новое ядро расположено по пути: {copy_name}")
            else:
                exc_path = copy_name

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

    def write_to_csv(self, filename, data):
        import csv
        self.file_bizy = True
        print(f"\n>Сохраняю \"{filename}.csv\" в папку \"data\"")
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
        print(f">Данные сохранены")
        self.file_bizy = False
        
    def file_exists(self, filename):
        try:
            with open(f'data/{filename}.csv', 'r') as file:
                return True
        except FileNotFoundError:
            return False

    def catalog(self):
        self.driver.get("https://clever-style.ru/catalog/")
        self.wait.until(EC.element_to_be_clickable((By.XPATH,'//a[@href="/catalog/zhenskoe/"]'))) # ожидание
        try:
            for el in self.driver.find_elements(By.XPATH,"//nav/section/button"):
                self.action.move_to_element(el)
                self.action.click(el)
                self.action.perform()  
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

    def parse_subcatalogs(self,driver,subcatalogs,test=False):
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
                print(f"Начинаю сбор для \"{title}\"")
                if test == False:
                    links = self.parse_subcatalog_page_links(driver, s[-1]) # собирает ссылки на товари из подкаталога
                else:
                    links = self.parse_subcatalog_page_links(driver, s[-1])
                    if len(links) > 0:
                        links = links[:10]
                print(f"> Получены {len(links)} ссылок на товар. Собираю информацию...")
                # собирает конкретные значения из товаров
                
                for step,link in enumerate(links):
                    # sys.stdout.write(f"\r>Просмотренно товаров [{step+1}/{len(links)}] |  {link}")
                    # sys.stdout.flush()
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
                        # if type(tovar[5]) == list:
                        #     counts = ";".join(tovar[5])
                        #     tovar[5] = counts
                        if type(tovar[-1]) == list:
                            img = ";".join(tovar[-1])
                            tovar[-1] = img
                        tovar_data.append(tovar)
                # Очистка дублей
                if tovar_data != []:
                    if self.main_data.get(title) != None:
                        self.main_data[title] = self.remove_duplicates(sum([self.main_data[title],tovar_data],[]))
                        self.sigment_catalog()
                    else:
                        self.main_data[title] = self.remove_duplicates(tovar_data)
                        self.sigment_catalog()
                else:
                    print("Каталог пуст")
            except:
                logging.error(f"Ошибка сбора данных в каталоге {s[0]} \n{traceback.format_exc()}\n -- Набор данных --> {tovar_data}")
        return
    
    def sigment_catalog(self):
        while self.file_bizy:
            time.sleep(0.2)
        else:
            for title,value in self.main_data.items():
                self.write_to_csv(title,value)
                
    def single_tovar_grab(self,driver: webdriver.Chrome, link: str):
        driver.get(link)
        try:
            more = driver.find_element(By.XPATH,'//section[1]/div/div[2]/section[3]/button')
            self.action.move_to_element(more)
            self.action.click(more)
            self.action.perform()
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
                self.action.move_to_element(color_button)
                self.action.click(color_button)
                self.action.perform()
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
        catalog_data = self.catalog()
        sale_cat = list(map(lambda x: self.sale_catalog(x),catalog_data))
        catalog_data.extend(sale_cat)
        catalog_data.reverse()
        logging.info(f"Список каталогов - {catalog_data}")
        subcatalogs = list(map(lambda data: self.subcatalogs(data),catalog_data))
        print(subcatalogs)
        subcatalogs = sum(subcatalogs,[])
        subcatalogs = list(filter(lambda x: x != None, subcatalogs))
        print(logging.info(f"Список подкаталогов - {subcatalogs}"))
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
        # print(logging.info(f"Список подкаталогов - {subcatalogs}"))
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
        thread_count: int = os.cpu_count()
        thread_list: list[Thread] = []
        working_lists = self.split_list(subcatalogs, thread_count)

        for sub_catalogs in working_lists:
            if sub_catalogs == working_lists[0]:
                if test == False:
                    t = Thread(target=self.parse_subcatalogs,args=(self.driver, sub_catalogs,))
                else:
                    t = Thread(target=self.parse_subcatalogs,args=(self.driver,sub_catalogs,test))
            else:
                if test == False:
                    driver = self.based_browser_startUp(self._invis)
                    t = Thread(target=self.parse_subcatalogs,args=(driver, sub_catalogs,))
                else:
                    driver = self.based_browser_startUp(self._invis)
                    t = Thread(target=self.parse_subcatalogs,args=(driver,sub_catalogs,test))

                
            thread_list.append(t)
        
        for t in thread_list:
            t.start()
        
        for t in thread_list:
            t.join()

    
