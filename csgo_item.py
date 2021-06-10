from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import time
import datetime
import eel
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QIcon
from ui2 import Ui_Scraping
import sys
from PyQt5.QtCore import QThread
# qlineargradient(spread:pad, x1:0.921, y1:0.961, x2:0.069, y2:0.0568182, stop:0 rgba(40, 40, 40, 255), stop:1 rgba(255, 255, 255, 255));
# background-image:
#     linear-gradient(
#       to right, 
#       gray, black
#     );

game = None
price = None

class WW(Qt.QMainWindow):
    def __init__(self):

        super(WW, self).__init__()
        self.ui = Ui_Scraping()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):
        game_list = ['CSGO', 'DOTA', 'PUBG', 'RUST' , 'TF2', 'UNT', 'PD2', 'KF2', 'DST', 'Z1', 'BS', 'ART']
        self.setWindowTitle('Парсинг')
        self.ui.textEdit_5.setPlaceholderText(f'Например: {game_list}')
        self.ui.textEdit_2.setPlaceholderText('Например: 1-5')
        self.ui.textEdit_3.setPlaceholderText('Например: 150')
        #self.ui.textEdit_3.setText(f'Начало {datetime.datetime.now()}')
        self.ui.pushButton.clicked.connect(self.ccc)

    def ccc(self):
        game = self.ui.textEdit_5.toPlainText()
        price = self.ui.textEdit_2.toPlainText()
        sheets = self.ui.textEdit_3.toPlainText()
        print(self.main_p(game, price, sheets))

    def write_into(self, text):
        with open('data.csv', 'a') as f:
            f.write(u'{text}'.format(text=text))
            f.write('\n')

    def main_p(self, input_game, input_price, sheets):
        input_game = input_game.upper()
        games = {
            'STEAM': 'https://steamcommunity.com/market/search/render/?query=&start=Q&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=753',
            'CSGO': 'https://steamcommunity.com/market/search/render/?query=&start=Q&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730&category_730_ItemSet%5B%5D=',
            'DOTA2': 'https://steamcommunity.com/market/search/render/?query=&start=Q&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=570&category_570_Hero%5B%5D=',
            'PUBG': 'https://steamcommunity.com/market/search/render/?query=&start=Q&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=578080',
            'RUST': 'https://steamcommunity.com/market/search/render/?query=&start=Q&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=252490&category_252490_itemclass%5B%5D=any',
            'TF2': 'https://steamcommunity.com/market/search/render/?query=&start=Q&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=440&category_440_Collection%5B%5D=any&category_440_Type%5B%5D=any',
            'UNT': 'https://steamcommunity.com/market/search/render/?query=&start=Q&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=304930&category_304930_collection%5B%5D=any&category_304930_effect%5B%5D=any&category_304930_particle_effect%5B%5D=any&category_304930_skin_slot%5B%5D=any',
            'PD2': 'https://steamcommunity.com/market/search/render/?query=&start=Q&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=218620&category_218620_collection%5B%5D=any',
            'KF2': 'https://steamcommunity.com/market/search/render/?query=&start=Q&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=232090',
            'DST': 'https://steamcommunity.com/market/search/render/?query=&start=Q&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=322330',
            'Z1': 'https://steamcommunity.com/market/search/render/?query=&start=Q&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=433850&category_433850_Origin%5B%5D=any',
            'BS': '',
            'ART': 'https://steamcommunity.com/market/search/render/?query=Qstart=10&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=583950',
            'BP': 'https://steamcommunity.com/market/search/render/?query=&start=Q&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=706990',
            'PCE: EXTINCTION': 'https://steamcommunity.com/market/search/render/?query=&start=Q&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=321360&category_321360_Class%5B%5D=any'
        }
        game_list = ['STEAM', 'CSGO', 'DOTA', 'PUBG', 'RUST', 'TEAM_FORTRESS2', 'UTURNED', 'PAY_DAY2', 'KILLING_FLOOR2', 'DONT_STRAVE_TOGETHER', 'Z1_BATTLE_ROYALE', 'BLACK_SQUAD', 'ARTIFACT']
        input_stair = 'ALL'
        line = input_price
        br = 0
        try:
            line = line.split('-')
        except:
            line = input_price
        sleep_ban = 90
        sleep = 3

        if input_stair == 'ALL':
            print('Скрипт запущен')
            print(f'Начало: {str(datetime.datetime.now())[:-7:]}')
            time.sleep(sleep)# new url
            link = games[input_game]
            link = link.replace('Q', str(0))
            page = urlopen(link)
            data = json.loads(page.read().decode())# print(data)
            count = data['total_count']
            for i in range(count):
                self.__init__()
                try:
                    time.sleep(sleep)
                    link = games[input_game]
                    link = link.replace('Q', str(i * 10))
                    page = urlopen(link)
                    data = json.loads(page.read().decode())
                    html = data['results_html']
                    bs_page = BeautifulSoup(html, features = "html.parser")
                    objects = bs_page.findAll(
                        class_ = "market_listing_row market_recent_listing_row market_listing_searchresult")
                    res = []
                    for g in objects:
                        name = g.find('span', class_ = 'market_listing_item_name').get_text(
                            strip = True)# market_listing_item_name
                        price = g.find('span', {
                            'data-price': True
                        }).text
                        pr = price
                        clear_h = pr.split(' USD')
                        clear = clear_h[0].split('$')[1]
                        total = name
                        if 'ALL' in line[0]:
                            res.append(str(total) + f'; {clear};')
                        else :
                            if float(clear) <= float(line[1]) and float(clear) >= float(line[0]):
                                res.append(str(total) + f'; {clear};')
                            else :
                                continue
                    time.sleep(sleep)

                    try:
                        for m in res:
                            self.write_into(m)
                            print(m)
                        a = objects[6]
                    except:
                            print(f'Пустая страница {i+1}')
                            if br > int(sheets):
                                break
                            else :
                                br += 1
                    print(f'Спарсили страницу {i+1}')
                except Exception as e:
                    print(f"Перерыв, ждем {sleep_ban} сек. ;). Начало перерыва: {str(datetime.datetime.now())[:-7:]}")# self.ui.textEdit_3.setText(f "Перерыв, ждем {sleep_ban} сек. ;). Начало перерыва: {datetime.datetime.now()}")# print(str(e))
                    time.sleep(sleep_ban)

    #main_p()


if __name__ == '__main__':    
    app = Qt.QApplication([])
    applicatoin = WW()
    applicatoin.show()
    sys.exit(app.exec())
