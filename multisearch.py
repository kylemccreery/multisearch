#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import argparse
import re
import json

class card_encoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

class McCard():
    def __init__(self,name,price,qty,condition):
        self.name = name
        self.price = price
        self.qty = qty
        self.condition = condition
    
    def __str__(self):
        return "Name: %s\r\nPrice: %s\r\nCondition: %s\r\nAvailable: %s\r\n" % (self.name, self.price, self.condition, self.qty)
    

class Stock(McCard):
    def __init__(self,store,card_info):
        self.store = store
        if store == "Ideal808":
            self.name = card_info.find_next('h4',class_='name').text.strip()
            strongs = card_info.find_all('strong')
            for each_quality in strongs:
                quality = each_quality.text.strip().strip(':').lower()
                desc = each_quality.next_sibling.strip()
                if quality == "condition":
                    self.condition = desc
                if quality == 'available':
                    self.qty = int(re.sub(r'[^\d]', '', desc))
                if quality == 'price':
                    self.price = desc
        if store == "Durdle Zone":
            self.name = card_info['data-name']
            self.price = card_info['data-price']
            self.condition = card_info['data-variant']
            self.qty = int(re.sub(r'[^\d]', '', card_info.find_next('select',class_='qty')['max']))
        if store == "Da-Planet":
            self.name = card_info.find_next('a',title=True)['title']
            self.condition = card_info.find_next('span', class_='variant-short-info').text
            self.price = card_info.find_next('span', class_='regular price').text
            self.qty = int(re.sub(r'[^\d]', '', card_info.find_next('select',class_='qty')['max']))

def check_ideal808(card_name):
    req = requests.get('http://www.ideal808.com/advanced_search?search[category_ids_with_descendants][]=8&search[in_stock]=1&search[with_descriptor_values][463]='+card_name)
    soup = BeautifulSoup(req.text, 'html.parser')
    all_cards = soup.find_all('div', class_='variants')
    results_list = []
    if len(all_cards) > 0:
        for each_card in all_cards:
            results_list += [Stock("Ideal808",each_card)]
    return results_list

def check_durdle_zone(card_name):
    nonfoil = 'http://www.durdlezone.com/advanced_search?search[in_stock]=1&buylist_mode=0&commit=Search&search[sort]=sell_price&search[direction]=ascend&search[category_ids_with_descendants][]=8&search[with_descriptor_values][348]='+card_name
    foil = 'http://www.durdlezone.com/advanced_search?search[in_stock]=1&buylist_mode=0&commit=Search&search[sort]=sell_price&search[direction]=ascend&search[category_ids_with_descendants][]=1549&search[with_descriptor_values][2094]='+card_name
    nf_req = requests.get(nonfoil)
    f_req = requests.get(foil)
    nf_soup = BeautifulSoup(nf_req.text, 'html.parser')
    f_soup = BeautifulSoup(f_req.text, 'html.parser')
    all_cards = nf_soup.find_all('div', class_='variants') + f_soup.find_all('div', class_='variants')
    results_list = []
    if len(all_cards) > 0:
        for each_card in all_cards:
            addToCart = each_card.find_next('form',class_='add-to-cart-form')
            results_list += [Stock("Durdle Zone",addToCart)]
    return results_list

def check_da_planet(card_name):
    req = requests.get('http://www.da-planet.com/advanced_search?search[in_stock]=1&buylist_mode=0&commit=Search&search[sort]=sell_price&search[direction]=ascend&search[category_ids_with_descendants][]=8&search[with_descriptor_values][348]='+card_name)
    soup = BeautifulSoup(req.text, 'html.parser')
    all_cards = soup.find_all('li', class_='product', itemtype=True)
    results_list = []
    if len(all_cards) > 0:
        for each_card in all_cards:
            results_list += [Stock("Da-Planet",each_card)]
    return results_list

def cheapest(list_of_card_dicts):
    lowest_price = False
    lowest_card = False
    for each_card in list_of_card_dicts:
        current_price = float(each_card.price.strip('$'))
        if lowest_price == False or current_price < lowest_price:
            lowest_price = current_price
            lowest_card = each_card
    return lowest_card

def check_all_stores(card_name):
    return check_da_planet(card_name)+check_ideal808(card_name)+check_durdle_zone(card_name)

def check_all_stores_dict(card_name):
    outDict = {}
    durdle = check_durdle_zone(card_name)
    daplanet = check_da_planet(card_name)
    ideal808 = check_ideal808(card_name)
    if durdle:
        outDict["Durdle Zone"] = durdle
    if daplanet:
        outDict["Da Planet"] = daplanet
    if ideal808:
        outDict["Ideal808"] = ideal808
    return outDict

def cheapest_of_all(card_name):
    return cheapest(check_all_stores(card_name))

def wrap_it(card_object):   # can also take lists of card objects
    return json.dumps(card_object,cls=card_encoder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Checks Durdle Zone, Da Planet, and Ideal808(ToyLynx) for card availability and prices.')
    parser.add_argument('cardname', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    cardtoSearch = ''
    for eachWord in args.cardname:
        if cardtoSearch != '':
            cardtoSearch += '+'
        cardtoSearch += str(eachWord)
    print("Ideal808")
    print("--------")
    results = check_ideal808(cardtoSearch)
    if results == []:
        print('None found.')
    else:
        for each_result in results:
            print(each_result)
    print()
    print("Durdle Zone")
    print("-----------")
    results = check_durdle_zone(cardtoSearch)
    if results == []:
        print('None found.')
    else:
        for each_result in results:
            print(each_result)
    print()
    print("Da-Planet")
    print("---------")
    results = check_da_planet(cardtoSearch)
    if results == []:
        print('None found.')
    else:
        for each_result in results:
            print(each_result)
