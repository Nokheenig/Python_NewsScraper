from selenium import webdriver #Webdriver de Selenium qui permet de contrôler un navigateur
from selenium.webdriver.common.by import By #Permet d'accéder aux différents élements de la page web
#from selenium.webdriver.remote.webelement

from webdriver_manager.chrome import ChromeDriverManager #Assure la gestion du webdriver de Chrome

from datetime import datetime, timedelta
import math
import time
import requests

import warnings
warnings.filterwarnings("ignore")
import os
import json
from definitions import ROOT_DIR

#import logging as logScraper
#logScraper.basicConfig(filename='logs/scraper.log', encoding='utf-8', filemode='w', format='%(asctime)s-%(levelname)s:%(message)s', level=logScraper.DEBUG)

import logging as logDal
logDal.basicConfig(filename=os.path.join(ROOT_DIR,"logs","scraper.log"), encoding='utf-8', filemode='w', format='%(asctime)s-%(levelname)s:%(message)s', level=logDal.DEBUG)

class NewsScraper:
    def __init__(self) -> None:
        self.dalArticle = self.DataAccessLayer(resourceName="article")
        self.today = datetime.now()
        self.targetDay = self.today
        self.year = str(self.targetDay.year)
        self.month = str(self.targetDay.month)
        self.day = "0" + str(self.targetDay.day) if len(str(self.targetDay.day)) < 2 else str(self.targetDay.day) #on ajoute 0 devant le jour s'il est compris entre 1 et 9
        self.driver = webdriver.Chrome()#ChromeDriverManager().install()) 
        time.sleep(3) #Ajout d'un temps de deux secondes avant de lancer l'action suivante 

    def getNewsFrom(self, 
                    year: str|None = None, 
                    month:str|None = None, 
                    day:str|None = None):
        if not year: year = self.year
        if not month: month = self.month
        if not day: day = self.day

        sessionTimestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        sessionFilesPath = os.path.join(ROOT_DIR,"logs","sessionFiles",sessionTimestamp)
        os.mkdir(sessionFilesPath)
        sessionFailuresPath = os.path.join(ROOT_DIR,sessionFilesPath,"failures")
        os.mkdir(sessionFailuresPath)
        sessionArticlesPath = os.path.join(ROOT_DIR,sessionFilesPath,"articles")
        os.mkdir(sessionArticlesPath)

        self.driver.get('https://www.euronews.com/{}/{}/{}'.format(year, month, day)) #Accès aux articles du jour d'esigne'

        #Le code ci-dessous n'est pas nécessaire pour le scrapping. Nous l'ajoutons pour montrer qu'il est possible d'effectuer
        #de manière automatique tout ce que nous aurions fait manuellement

        time.sleep(1) 
        accept_cookies =  self.driver.find_element(By.ID, "didomi-notice-agree-button") #On identifie le boutton d'acception des cookies 

        self.driver.execute_script("arguments[0].click();", accept_cookies); # On clique dessus

        len_articles = self.driver.find_element(By.XPATH, '//p[@class="c-block-listing__results"]/strong[1]').text

        pages = int(len_articles) / 30 #Nous avons remarqué la pagination de 30
        pages =  math.ceil(pages) #Permet d'arrondir au supérieur

        articles = []
        for i in range(1,pages+1) : #On itère sur chaque page où il y a des articles
            self.driver.get('https://www.euronews.com/{}/{}/{}?p={}'.format(year, month, day, i)) #On accède aux informations du jour sur chaque page
            articles_webscrapped = self.driver.find_elements(By.CLASS_NAME, "m-object__title__link ") #On récupère les articles
            for article in articles_webscrapped :
                articles.append(article.get_attribute('href')) # On ajoute à la liste "articles" les liens de chaque article

        articlesWithEmptyFieldsCount = 0
        errors = []
        list_of_articles = []
        for idx_article, article in enumerate(articles):
            if idx_article >4: continue
            try : #On utilise un try except pour pouvoir sauter les pages qui n'ont pas la même structure html pour évoter qui causerait une erreur    
                self.driver.get(article) #On accède à la page de l'article
                logDal.info(f"New scraped article: {article}")
                # Récupération du body de la page:
                body = self.driver.find_element(By.XPATH, "/html/body")

                """
                Sauvegarde des sources de la page scrappée sur le disque
                """
                with open(os.path.join(sessionArticlesPath,f"{idx_article}_article_source.html"), "w", encoding='utf-8') as f:
                        f.write(self.driver.page_source)

                with open(os.path.join(sessionArticlesPath,f"{idx_article}_article_source_body.html"), "w", encoding='utf-8') as f:
                        f.write(str(body.get_attribute("innerHTML")).strip())

                """
                Get article title
                """
                #print("c-article-redesign-title")
                title =  body.find_elements(By.CLASS_NAME, "c-article-redesign-title")[0].text
                title = title if title else body.find_elements(By.CLASS_NAME, "c-article-redesign-title")[1].text
                """
                ^v1
                """

                """
                Get article authors
                #Récupération des auteurs
                #print("c-article-contributors")
                """

                authors_scrapped =  body.find_elements(By.CLASS_NAME, "c-article-contributors")[1] #Etape 1) Accès au deuxième élément qui a la classe "c-article-contributors"
                authors_scrapped = authors_scrapped.find_elements(By.TAG_NAME, "b") #Etape 2) accès au texte des sous-balises b contenant les auteurs
                
                authors = []
                for subElement in authors_scrapped:
                    tagName = subElement.tag_name
                    if tagName is None: continue
                    subElementText = str(paragraph.get_attribute('innerText')).strip()
                    if subElementText == "ADVERTISEMENT" or not subElementText: continue
                    if tagName == "p" or tagName == "a":
                        authors.append(subElementText)
                    else:
                        pass

                authors = ", ".join(authors) #Etape 3) Concaténation des auteurs en une string
                """
                ^v1
                """

                """
                logDal.info(f"Before shit goes south:")
                #authors_scrapped = self.driver.find_elements(By.XPATH, f"//*[starts-with(@class,'c-article-contributors')][1]//p")
                #authors_scrapped += self.driver.find_elements(By.XPATH, f"//*[starts-with(@class,'c-article-contributors')][1]//a")
                #authors_scrapped += self.driver.find_elements(By.XPATH, f"//*[starts-with(@class,'c-article-contributors')][1]//b")
                #authors_scrapped = authors_scrapped.find_elements(By.XPATH, "//*")
                authors_scrapped = self.driver.find_elements(By.XPATH, f"//*[starts-with(@class,'c-article-contributors')]")[0]
                #for idx, aut in enumerate(authors_scrapped):
                #    logDal.debug(f"authors_scrapped{idx}:\n{aut.get_attribute('innerHTML')}")
                #logDal.debug(f"authors_scrapped:\n{authors_scrapped.get_attribute('innerHTML')}")
                authors = []
                tagList = ["p","a","b"]
                for tag in tagList:
                    authors_s = authors_scrapped.find_elements(By.TAG_NAME, f"{tag}")
                    for subElement in authors_s:
                        tagName = subElement.tag_name
                        if tagName is None: continue
                        subElementText = str(paragraph.get_attribute('innerText')).strip()
                        if subElementText == "ADVERTISEMENT" or not subElementText: continue
                        if tagName in ["p","a","b"]:
                            authors.append(subElementText)
                        else:
                            pass
                logDal.debug(f"authors({len(authors)}):{authors}")
                authors = ", ".join(authors) #Etape 3) Concaténation des auteurs en une string

                ^v2
                """
                
                """
                Get article publication date
                """
                #Récupération de la date de publication grâce à la valeur de l'attribut datetime 
                #du deuxième élément ayant la classe "c-article-date"
                #print("c-article-publication-date")
                date = body.find_elements(By.CLASS_NAME, "c-article-publication-date")[1].get_attribute('datetime')
                """
                ^v1
                """
                
                """
                Get article Tags
                """
                #Récupération de la catégoie grâce au texte du deuxième élément ayant la classe "media__body__cat"
                #print("media__body__cat")
                #category = driver.find_elements(By.CLASS_NAME, "media__body__cat")[1].text###
                categories_scraped = body.find_elements(By.CLASS_NAME, "c-article-tags__item")
                categories = []
                for tag in categories_scraped:
                    tagText = tag.text
                    if not tagText: continue
                    categories.append(tagText)
                category = ", ".join(categories)

                """
                ^v1
                """

                """
                Get article paragraphs
                """
                #Récupération des paragraphes
                #print("//*[@class=c-article-content]//*")

                paragraphs_scraped = body.find_elements(By.XPATH, "//*[starts-with(@class,'c-article-content')]//*") #Etape 1) On récupère tous les paragraphes de l'article grâce au X-path###
                #self.driver.find_elements(By.XPATH, "//*[@class='c-article-content js-article-content ']//*")

                #Etape 2) On récupère le texte de chaque paragraphe
                paragraphs = []
                for paragraph in paragraphs_scraped:
                    tagName = paragraph.tag_name
                    #print(f"tagName: {tagName} -", end="")
                    if tagName is None: continue
                    parag = str(paragraph.get_attribute('innerText')).strip()
                    if parag == "ADVERTISEMENT" or not parag: continue
                    if tagName == "p":
                        paragraphs.append(parag)
                    elif tagName[0] == "h" and len(tagName) == 2:
                        headerLevel = int(tagName[1])
                        paragraphs.append("#"*headerLevel + " " + parag)
                    else:
                        pass
                        #print("Debug-Skipped: Unplanned HTML tag")
                    #print()

                #print(f"paragraphs({len(paragraphs)}): {paragraphs}")
                text  = "\n".join(paragraphs) #Etape 3) On joint les paragraphes en un texte

                """
                ^v1
                """

                """
                Build dictionnary
                """
                #On crée un dictionnaire avec les différents éléments récupérés
                dictionnary_of_article = {"date": date, "title": title, "authors": authors, "category": category, "text": text, "link": article }
                logDal.debug(f"dictionnary_of_article:\n{dictionnary_of_article}")

                """
                If missing field -> Save page source in a failure file
                """
                if not date or not title or not authors or not category or not text:
                    logDal.debug(f"Article is missing fields value- Aborting...\n{article}")
                    articlesWithEmptyFieldsCount +=1
                    with open(os.path.join(sessionFailuresPath,f"{articlesWithEmptyFieldsCount}_article_dict.txt"), "w", encoding='utf-8') as f:
                        f.write(json.dumps(dictionnary_of_article, indent=4))
                    with open(os.path.join(sessionFailuresPath,f"{articlesWithEmptyFieldsCount}_article_source.html"), "w", encoding='utf-8') as f:
                        f.write(self.driver.page_source)
                else:
                    pass

                
                """
                Add scraped article data in the database
                Wait before scraping next article not to get flagged as bot and get our IP banned
                """
                list_of_articles.append(dictionnary_of_article) 
                logDal.debug(f"before postOne call")
                self.dalArticle.postOne(dictionnary_of_article)
                logDal.debug(f"after postOne call")
                time.sleep(3)#Ajout de 3 secondes avant de charger la page de l'article suivant

            except Exception as e: #
                errors.append({article: e}) #On ajoute dans une liste tous les articles dont n'où n'avons pas pu scrapper le contenu
        self.errors = errors
        self.scrapedArticles = list_of_articles
        #print(list_of_articles)
        #print(len(list_of_articles))
        return list_of_articles
    
    class DataAccessLayer:
        def __init__(self, resourceName:str) -> None:
            self.apiUrl = f"http://127.0.0.1:8000/{resourceName}s"
            self.resourceName = resourceName
        
        def getAll(self):
            logDal.info(f"{self.resourceName}Dal--getAll-Start")
            res = requests.get(f"{self.apiUrl}/")
            logDal.info(f"{self.resourceName}Dal--getAll-End")
            return res
        
        def getAllSumList(self) -> list[dict]:
            logDal.info(f"{self.resourceName}Dal--getAllSumList-Start")
            res =  requests.get(
                url=f"{self.apiUrl}/list"
                ).json()
            logDal.debug(f"Json converted list :\n{res}")
            logDal.info(f"{self.resourceName}Dal--getAllSumList-End")
            return res
        
        def postOne(self, obj: object):
            logDal.info(f"{self.resourceName}Dal--postOne-Start")
            try:
                res = requests.post(url=f"{self.apiUrl}/",
                                    json=obj
                                    )
                if res.status_code == 201:
                    logDal.debug(f"Object created in database:\n{res.json}")
                else:
                    logDal.debug(f"Error while creating the object in database:\nStatus code:{res.status_code}\nmessage:{res.content}")
            except Exception as e:
                logDal.debug(f"Error: {e}")
            logDal.info(f"{self.resourceName}Dal--postOne-End")

        def deleteOne(self, objId: str):
            logDal.info(f"{self.resourceName}Dal--deleteOne-Start")
            res = requests.delete(
                url=f"{self.apiUrl}/{objId}"
                )
            if res.status_code == 204:
                logDal.debug(f"Successfully deleted {self.resourceName} with id: {objId}")
            else:
                logDal.debug(f"Failed to delete {self.resourceName} with id: {objId}")
            logDal.info(f"{self.resourceName}Dal--deleteOne-End")

        def deleteMany(self, objIds: list[str]):
            logDal.info(f"{self.resourceName}Dal--deleteMany-Start")
            for objId in objIds:
                self.deleteOne(objId)
            logDal.info(f"{self.resourceName}Dal--deleteMany-End")

        def deleteAll(self):
            logDal.info(f"{self.resourceName}Dal--deleteAll-Start")
            itemIds = [item["_id"] for item in self.getAllSumList()]
            logDal.debug(f"List of received item ids:\n{itemIds}")
            self.deleteMany(itemIds)
            logDal.info(f"{self.resourceName}Dal--deleteAll-End")




if __name__ == "__main__":
    scraper = NewsScraper()
    scraper.dalArticle.deleteAll()
    articles = scraper.getNewsFrom()

