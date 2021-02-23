import json
import os
from pprint import pprint
from .analyse_site import Analyse_Web
from .analyse_data import AnalyseData
from .analyse_financials import AnalyseFondamental

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
path_json = os.path.join(path, 'datas', "files.json")

list_liens = {}
with open(path_json) as json_data:
    liens_dict = json.load(json_data)

class Fondamentaux:
    def __init__(self, ticker):

        analyse = AnalyseFondamental(ticker=ticker)

    def _(self):
        for entreprise, liens in liens_dict.items():
            if entreprise == "action":
                site = liens[0]
                dividende = liens[1]
                # self.donne_site = Analyse_Web(entreprise, site, dividende).__dict__
                # self.analyse_data = AnalyseData(self.donne_site).__dict__
                # pprint(self.analyse_data)
                # self.analyse_entreprise = Analyse_Enreprise(self.donne_site).__dict__
                # self.analyse = Analyse_Donnee(self.analyse_entreprise['data_analyse'])
                # print(analyse_entreprise['data_analyse'])
                # analyse['Entreprise'] = entreprise
                # pprint(analyse)

