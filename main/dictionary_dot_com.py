import requests as r
from  bs4 import BeautifulSoup as bs

class DictionaryReference:

     def __init__(self, word):
          self.word = word
          self.definition_list = []
          self.extra_list = []
          self._request = None
          self._soup = None
          self._get_page_contents()
          self._difficulty = None

     def _get_page_contents(self):
          '''
          Get HTML content
          :return:
          '''
          self._request = r.get('http://dictionary.reference.com/browse/' + self.word)
          self._soup = bs(self._request.text, "lxml")
          self._request.close()

     def get_definitions(self):
          '''
          Get all definitions
          :return:
          '''
          tables = self._soup.find_all("section", class_="def-pbk ce-spot")
          difficultyObj = self._soup.find("section", id="difficulty-box")
          self._difficulty = difficultyObj.get("data-difficulty") + " - " + difficultyObj.find("span", class_="subtext").text
          for table in tables:
               try:
                    word_type = table.find("span", class_="dbox-pg").text
               except:
                    word_type = "none"
               set_def = table.find_all("div", class_="def-content")
               for def_ in set_def:
                    meaning = self.get_formated(def_.text)
                    if (meaning != None):
                         self.definition_list.append(Definition(self.word, word_type, meaning, self._difficulty))

     def get_formated(self, string):
          '''
          reformat a definition
          :param string:
          :return:
          '''
          return string.replace("                 ", " ").replace('\n\r', '').replace('\t', '').strip()

     def get_first(self):
          if len(self.definition_list) < 1:
               return None
          return self._difficulty + "\n" + self.definition_list[0].__str__()

     def get_top3(self):
          if len(self.definition_list) < 3:
               return self._difficulty + "\n" + "".join(self.definition_list[i].__str__() + "\n" for i in range(0, len(self.definition_list)))
          return self._difficulty + "\n" + "".join(self.definition_list[i].__str__() + "\n" for i in range(0, 3))

     def __str__(self):
          return self.word


class Definition:
     def __init__(self, word, word_type, meaning, difficulty=0):
          self.word = word
          self.type = word_type
          self.meaning = meaning
          self.difficulty = difficulty

     def __str__(self):
          return "{1} - {2}".format(self.word, self.type, self.meaning)

if __name__ == '__main__':
     dr = DictionaryReference("swell")
     dr.get_definitions()
     print(dr.get_top3())