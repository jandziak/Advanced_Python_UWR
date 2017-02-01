__author__ = 'jidziak'
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

# We are going to create a class called LinkParser that inherits some
# methods from HTMLParser which is why it is passed into the definition
class LinkParser(HTMLParser):


    # This is a function that HTMLParser normally has
    # but we are adding some functionality to it
    def handle_starttag(self, tag, attrs):
        # We are looking for the begining of a link. Links normally look
        # like <a href="www.someurl.com"></a>
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    # We are grabbing the new URL. We are also adding the
                    # base URL to it. For example:
                    # www.netinstructions.com is the base and
                    # somepage.html is the new URL (a relative URL)
                    #
                    # We combine a relative URL with the base URL to create
                    # an absolute URL like:
                    # www.netinstructions.com/somepage.html
                    newUrl = parse.urljoin(self.baseUrl, value)
                    # And add it to our colection of links:
                    self.links = self.links + [newUrl]

    # This is a new function that we are creating to get links
    # that our spider() function will call
    def getLinks(self, url):
        self.links = []
        # Remember the base URL which will be important when creating
        # absolute URLs
        self.baseUrl = url
        # Use the urlopen function from the standard Python 3 library
        response = urlopen(url)
        # Make sure that we are looking at HTML and not other things that
        # are floating around on the internet (such as
        # JavaScript files, CSS, or .PDFs for example)
        if response.getheader('Content-Type')=='text/html':
            htmlBytes = response.read()
            # Note that feed() handles Strings well, but not bytes
            # (A change from Python 2.x to Python 3.x)
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "",[]

# And finally here is our spider. It takes in an URL, a word to find,
# and the number of pages to search through before giving up
def spider(url, word, maxPages):
    pagesToVisit = [url]
    numberVisited = 0
    foundWord = False
    # The main loop. Create a LinkParser and get all the links on the page.
    # Also search the page for the word or string
    # In our getLinks function we return the web page
    # (this is useful for searching for the word)
    # and we return a set of links from that web page
    # (this is useful for where to go next)
    while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
        numberVisited = numberVisited +1
        # Start from the beginning of our collection of pages to visit:
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            print(numberVisited, "Visiting:", url)
            parser = LinkParser()
            data, links = parser.getLinks(url)
            if data.find(word)>-1:
                foundWord = True
                # Add the pages that we visited to the end of our collection
                # of pages to visit:
                pagesToVisit = pagesToVisit + links
                print(" **Success!**")
        except:
            print(" **Failed!**")
    if foundWord:
        print("The word", word, "was found at", url)
    else:
        print("Word never found")




__author__ = 'jidziak'

#dorzucanie wyjatkow
import re
import urllib
import operator

class Wyszukiwarka:
    def __init__(self):
        self.startowa = "http://prac.im.pwr.wroc.pl/~kwasnicki/pl/"
        self.lista_stron = []
        self.lista_slownik = []
        self.adres = "(\w+\.)*[a-zA-Z]+"
        self.automat = re.compile("http://" +self.adres)
    def wyszukaj_adresy(self, adres_strony):
        self.lista_link = []
        self.try_to_open_wyszukaj(adres_strony)
        return(self.lista_link)
    def try_to_open_wyszukaj(self, adres_strony):
        try:
            self.f = urllib.request.urlopen(adres_strony)
            self.tekst = self.f.read()
            self.lista_link = [url.group() for url in self.automat.finditer(str(self.tekst))]
        except urllib.error.URLError:
            self.f.close()
            raise urllib.error.URLError("weszlem")
        except ConnectionResetError:
            self.f.close()
            raise urllib.error.URLError("szybko weszlem")
        finally:
            self.f.close()
    def try_to_open_przeszukiwanie(self, urls):
        try:
            tmp = self.wyszukaj_adresy(urls)
            for urls1 in tmp:
                if urls1 not in self.lista_slownik:
                    self.lista_stron[str(self.licznik + 1)].append(urls1)
                    self.lista_slownik.append(urls1)
        except urllib.error.URLError:
            pass
        except ConnectionResetError:
            pass
        except KeyError:
            pass
        finally:
            self.f.close()
    def try_to_open_indexowanie(self, urls, slowo_automat):
        try:
            self.f = urllib.request.urlopen(urls)
            self.tekst = self.f.read()
            lista_slow = [l.group() for l in slowo_automat.finditer(str(self.tekst))]
            self.slownik_stron[urls].append(len(lista_slow))
        except urllib.error.URLError:
            self.slownik_stron[urls].append(0)
            pass
        except ConnectionResetError:
            self.slownik_stron[urls].append(0)
            pass
        finally:
            self.f.close()
    def przegladaj_strony(self, k):
        self.licznik = 0
        self.lista_stron = {str(i): [] for i in range(k+1)}
        self.lista_stron["0"].append(self.startowa)
        while self.licznik < k:
            for urls in self.lista_stron[str(self.licznik)]:
                self.try_to_open_przeszukiwanie(urls)
            self.licznik += 1
    def indexowanie(self):
        lista = sorted(self.slownik_stron.items(), key = operator.itemgetter(1), reverse = True)
        return(lista)
    def prpr(self):
        return(self.lista_stron)
    def wyszukaj(self, slowo):
        self.slownik_stron = {str(i): [] for i in self.lista_slownik}
        slowo_automat = re.compile(slowo)
        for urls in self.lista_slownik:
            self.try_to_open_indexowanie(urls, slowo_automat)
        return(self.indexowanie())


x = Wyszukiwarka()
x.prpr()
x.wyszukaj_adresy("http://prac.im.pwr.wroc.pl/~kwasnicki")
x.przegladaj_strony(1)
qq1 = x.wyszukaj("the")


x = Wyszukiwarka()
x.prpr()
x.wyszukaj_adresy("http://prac.im.pwr.wroc.pl/~kwasnicki")
x.przegladaj_strony(2)
qq = x.wyszukaj()
adres = "serdecznie"
adres.lower()
automat = re.compile(adres.lower())
lista_link = [url.group() for url in automat.finditer(str(qq))]
# qq = x.prpr()
# http://terrytao.wordpress.com