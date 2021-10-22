import abc 
import requests
import json
import xmltodict
  
class AbstractCurrencyGetter(object, metaclass=abc.ABCMeta): 
    
    def __init__(self, year, month, day): 
      
        if self.__class__ is AbstractCurrencyGetter: 
            raise TypeError('Classe abstrata não pode ser instanciada') 

        self.__url = self.get_url()
        self.__year = year
        self.__month = month
        self.__day = day
        self.__valor = ''
        self.__curreny_name = self.currency_name()

    @abc.abstractmethod 
    def currency_name(self): 
        pass

    @abc.abstractmethod 
    def get_url(self): 
        pass
 
    def __get_value_from_bcb(self):
        try:
            header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
            page = requests.get(f'{self.__url}{self.__year}-{self.__month}-{self.__day}', headers=header)
            
            if page.status_code == 200:
                valor = json.loads(json.dumps(xmltodict.parse(page.content)))
                self.__valor = f'{self.__curreny_name} , {self.__day}-{self.__month}-{self.__year}' , "%.4f" %(1 / float(valor['valor-convertido']))
            else:
                raise ValueError(self.__curreny_name,' A cotação desta moeda ainda não está disponivel no Banco Central')
            
            return self.__valor
            
        except ValueError as e:
            return e

    def get_value(self):
        return self.__get_value_from_bcb()
        
    def __str__(self):
        return str(self.__valor)

class Dolar(AbstractCurrencyGetter):

    def currency_name(self): 
        return 'Dólar Americano'

    def get_url(self): 
        return 'https://www3.bcb.gov.br/bc_moeda/rest/converter/1/1/790/220/'
    
class Euro(AbstractCurrencyGetter):

    def currency_name(self): 
        return 'Euro'

    def get_url(self): 
        return 'https://www3.bcb.gov.br/bc_moeda/rest/converter/1/1/790/978/'

class DolarCanadense(AbstractCurrencyGetter):

    def currency_name(self): 
        return 'Dólar Canadense'

    def get_url(self): 
        return 'https://www3.bcb.gov.br/bc_moeda/rest/converter/1/1/790/165/'

    
  
if __name__ == '__main__': 
    
    teste_dolar = Dolar('2021','10','21')
    teste_euro = Euro('2021','10','21')
    teste_cad = DolarCanadense('2023','10','23')
    
    print(teste_dolar.get_value())
    print(teste_euro.get_value())
    print(teste_cad.get_value())
    