from tkinter import *
from bs4 import BeautifulSoup
import requests
from difflib import get_close_matches
import webbrowser

root = Tk()


class Price_compare:

    def __init__(self, master):
        self.var = StringVar()
        self.var_ebay = StringVar()
        self.var_flipkart = StringVar()
        self.var_amzn = StringVar()

        label = Label(master, text='Enter the product')
        label.grid(row=0, column=0)

        entry = Entry(master, textvariable=self.var)
        entry.grid(row=0, column=1)

        button_find = Button(master, text='Find', bd=4, command=self.find)
        button_find.grid(row=1, column=1, sticky=W, pady=8)

    def find(self):
        self.product = self.var.get()
        self.product_arr = self.product.split()
        self.n = 1
        self.key = ""
        self.title_flip_var = StringVar()
        self.title_amzn_var = StringVar()
        self.variable_amzn = StringVar()
        self.variable_flip = StringVar()

        for word in self.product_arr:
            if self.n == 1:
                self.key = self.key + str(word)
                self.n += 1

            else:
                self.key = self.key + '+' + str(word)

        self.window = Toplevel(root)
        self.window.title('Price Comparison Engine')
        label_title_flip = Label(self.window, text='Flipkart Title:')
        label_title_flip.grid(row=0, column=0, sticky=W)

        label_flipkart = Label(self.window, text='Flipkart price (Rs):')
        label_flipkart.grid(row=1, column=0, sticky=W)

        entry_flipkart = Entry(self.window, textvariable=self.var_flipkart)
        entry_flipkart.grid(row=1, column=1, sticky=W)

        label_title_amzn = Label(self.window, text='Amazon Title:')
        label_title_amzn.grid(row=3, column=0, sticky=W)

        label_amzn = Label(self.window, text='Amazon price (Rs):')
        label_amzn.grid(row=4, column=0, sticky=W)

        entry_amzn = Entry(self.window, textvariable=self.var_amzn)
        entry_amzn.grid(row=4, column=1, sticky=W)

        self.price_flipkart(self.key)
        self.price_amzn(self.key)

        try:
            self.variable_amzn.set(self.matches_amzn[0])
        except:
            self.variable_amzn.set('Product not available')
        try:
            self.variable_flip.set(self.matches_flip[0])
        except:
            self.variable_flip.set('Product not available')

        option_amzn = OptionMenu(self.window, self.variable_amzn, *self.matches_amzn)
        option_amzn.grid(row=3, column=1, sticky=W)

        lab_amz = Label(self.window, text='Not this? Try out suggestions by clicking on the title')
        lab_amz.grid(row=3, column=2, padx=4)

        option_flip = OptionMenu(self.window, self.variable_flip, *self.matches_flip)
        option_flip.grid(row=0, column=1, sticky=W)

        lab_flip = Label(self.window, text='Not this? Try out suggestions by clicking on the title')
        lab_flip.grid(row=0, column=2, padx=4)

        button_search = Button(self.window, text='Search', command=self.search, bd=4)
        button_search.grid(row=2, column=2, sticky=E, padx=10, pady=4)

        button_amzn_visit = Button(self.window, text='Visit Site', command=self.visit_amzn, bd=4)
        button_amzn_visit.grid(row=4, column=2, sticky=W)

        button_flip_visit = Button(self.window, text='Visit Site', command=self.visit_flip, bd=4)
        button_flip_visit.grid(row=1, column=2, sticky=W)

    def price_flipkart(self, key):
        url_flip = 'https://www.flipkart.com/search?q=' + str(
            key) + '&marketplace=FLIPKART&otracker=start&as-show=on&as=off'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        title_arr = []
        self.opt_title_flip = StringVar()
        source_code = requests.get(url_flip, headers=self.headers)
        plain_text = source_code.text
        self.soup_flip = BeautifulSoup(plain_text, "html.parser")
        for title in self.soup_flip.find_all('div', {'class': '_3wU53n'}):
            title_arr.append(title.text)

        user_input = self.var.get().title()

        self.matches_flip = get_close_matches(user_input, title_arr, 20, 0.1)
        try:
            self.opt_title_flip.set(self.matches_flip[0])
        except IndexError:
            self.opt_title_flip.set('Product not found')
        try:
            for div in self.soup_flip.find_all('a', {'class': '_31qSD5'}):
                for each in div.find_all('div', {'class': '_3wU53n'}):
                    if each.text == self.opt_title_flip.get():
                        self.link_flip = 'https://www.flipkart.com' + div.get('href')

            product_source_code = requests.get(self.link_flip, headers=self.headers)
            product_plain_text = product_source_code.text
            product_soup = BeautifulSoup(product_plain_text, "html.parser")
            for price in product_soup.find_all('div', {'class': '_1vC4OE _3qQ9m1'}):
                self.var_flipkart.set(price.text[1:] + '.00')
        except UnboundLocalError:
            pass

    def price_amzn(self, key):
        url_amzn = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + str(key)

        # Faking the visit from a browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        # Getting titles of all products on that page

        self.title_arr = []
        self.opt_title = StringVar()
        source_code = requests.get(url_amzn, headers=self.headers)
        plain_text = source_code.text
        self.soup = BeautifulSoup(plain_text, "html.parser")
        # for titles in self.soup.find_all('a', {'class': 'a-link-normal a-text-normal'}):
        for title in self.soup.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'}):
            self.title_arr.append(title.text)

        # Getting closest match of the input from user in titles
        user_input = self.var.get().title()

        self.matches_amzn = get_close_matches(user_input, self.title_arr, 20, 0.1)
        try:
            self.opt_title.set(self.matches_amzn[0])
        except IndexError:
            self.opt_title.set('Product not found')
        try:
            for span in self.soup.find_all('a', {'class': 'a-link-normal a-text-normal'}):
                for each in span.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'}):
                    if each.text == self.opt_title.get():
                        self.product_link = 'https://www.amazon.in' + span.get('href')

            product_source_code = requests.get(self.product_link, headers=self.headers)
            product_plain_text = product_source_code.text
            product_soup = BeautifulSoup(product_plain_text, "html.parser")
            for price in product_soup.find_all('span', {'class': 'a-price-whole'}):
                self.var_amzn.set(price.text[1:] + '.00')
        except UnboundLocalError:
            pass

        # self.opt_title.set(self.matches_amzn[0])
        # product_block = self.soup.find(attrs= {'title': self.opt_title.get()})
        # self.product_link = product_block.get('href')
        # product_source_code = requests.get(self.product_link, headers=self.headers)
        # product_plain_text = product_source_code.text
        # product_soup = BeautifulSoup(product_plain_text, "html.parser")
        # try:
        #     for price in product_soup.find(attrs={'id': 'priceblock_ourprice'}):
        #
        #         self.var_amzn.set(price)
        #         self.title_amzn_var.set(self.matches_amzn[0])
        # except TypeError:
        #         self.var_amzn.set('None')
        #         self.title_amzn_var.set('product not available')

    def search(self):
        amzn_get = self.variable_amzn.get()
        self.opt_title.set(amzn_get)
        product_block = self.soup.find(attrs={'title': self.opt_title.get()})
        self.product_link = product_block.get('href')
        product_source_code = requests.get(self.product_link, headers=self.headers)
        product_plain_text = product_source_code.text
        product_soup = BeautifulSoup(product_plain_text, "html.parser")
        try:
            for price in product_soup.find(attrs={'id': 'priceblock_ourprice'}):
                self.var_amzn.set(price)
        except TypeError:
            self.var_amzn.set('None')
            self.title_amzn_var.set('product not available')

        flip_get = self.variable_flip.get()
        self.opt_title_flip.set(flip_get)

        try:
            for div in self.soup_flip.find_all('a', {'class': '_31qSD5'}):
                for each in div.find_all('div', {'class': '_3wU53n'}):
                    if each.text == self.opt_title_flip.get():
                        self.link_flip = 'https://www.flipkart.com' + div.get('href')

            product_source_code = requests.get(self.link_flip, headers=self.headers)
            product_plain_text = product_source_code.text
            product_soup = BeautifulSoup(product_plain_text, "html.parser")
            for price in product_soup.find_all('div', {'class': '_1vC4OE _3qQ9m1'}):
                self.var_flipkart.set(price.text[1:] + '.00')
        except UnboundLocalError:
            pass

    def visit_amzn(self):
        webbrowser.open(self.product_link)

    def visit_flip(self):
        webbrowser.open(self.link_flip)


c = Price_compare(root)
root.title('Price Comparison Engine')
root.mainloop()