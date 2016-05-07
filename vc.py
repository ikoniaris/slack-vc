from bs4 import BeautifulSoup
import httplib2
import unicodedata
import utils

portfolio_dict = {
    "a16z": "http://a16z.com/portfolio/venture-growth/",
    "khosla": "http://www.khoslaventures.com/portfolio",
    #"accel": "http://www.accel.com/companies/",
    "sequoia": "https://www.sequoiacap.com/companies/",
    #"first round": "http://firstround.com/companies",
    "kpcb": "http://www.kpcb.com/companies",
    "ff": "http://foundersfund.com/portfolio/",
    #"greylock": "http://www.greylock.com/greylock-companies",
}

industries = ["advertising", "agriculture-food", "big-data", "chemical-fuels", "consumer", "education", "efficiency", "enterprise", "financial-services", "health", "materials", "power", "robotics", "space", "storage", "transportation"]

# Crawl the portfolio list of a16z
def geta16zPortfilio():
    url = portfolio_dict['a16z']
    http = httplib2.Http()
    status, response = http.request(url)
    soup = BeautifulSoup(response)
    companies = {}
    company = ""
    for li in soup.find(id="main").findAll('li'):
        t = li.get_text()
        if t[0] == "C":
            company = t[9:]
        if t[1] == "W":
            companies[company] = "http://" + t[10:]
    return companies

# Crawl the portfolio list of Khosla Venture
def getKhoslaPortfolio():
    url = portfolio_dict['khosla']
    http = httplib2.Http()
    status, response = http.request(url)
    soup = BeautifulSoup(response)
    companies = {}
    cstring = ""
    for industry in industries:
        url = portfolio_dict['khosla'] + "/" + industry
        status, response = http.request(url)
        soup = BeautifulSoup(response)
        for i in range(1, 10):
            cstring = "company-" + str(i)
            company = soup.find(id=cstring)
            if (company == None):
                break
            else:
                for li in company.findAll('a'):
                    t = li.get_text()
                    u = li.get('href')
                    companies[t] = "http://www.khoslaventures.com" + u
    return companies

# Crawl the portfolio list of Sequoia Cap
def getSequoiaPortfolio():
    url = portfolio_dict['sequoia']
    http = httplib2.Http()
    status, response = http.request(url)
    soup = BeautifulSoup(response)
    companies = {}
    name = ""
    for li in soup.find(id="allColumn").findAll('li'):
        name = li.get_text()
        companies[name] = "https://www.sequoiacap.com"+ li.find('div').get('data-url')
    return companies

# Crawl the portfolio list of KPCB ventures
def getKPCBPortfolio():
    url = portfolio_dict['kpcb']
    http = httplib2.Http()
    status, response = http.request(url)
    soup = BeautifulSoup(response)
    companies = {}
    name = ""
    for li in soup.find("div", {"class":"medium-9"}).findAll("li"):
        if li != None:
            a = li.find('a')
            if a != None:
                url = a.get('href')
                if url[0] == '/':
                    url = "http://www.kpcb.com" + url
                name = utils.extract_name_from_url(a.get('href'))
                companies[name] = url
    return companies

# crawl portfolio list of Founder Fund
def getFFPortfolio():
    url = portfolio_dict['ff']
    # mock a browser
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    
    http = httplib2.Http()
    status, response = http.request(url, 'GET', None, headers)
    soup = BeautifulSoup(response)
    companies = {}
    name = ""
    for a in soup.find("ul", {"class":"portfolio"}).findAll('a'):
        url = str(a.get('href'))
        url_l = url.split('/')
        name = url_l[len(url_l)-2]

        formatted_name = ""
        formatted_name += name[0].upper()

        for c in name[1:]:
            formatted_name += c
        companies[formatted_name] = url
    return companies


def getPortfolio(vc):
    vc = vc.lower()
    if vc == "a16z":
        return geta16zPortfilio()
    elif vc == "khosla":
        return getKhoslaPortfolio()
    elif vc == "sequoia":
        return getSequoiaPortfolio()
    elif vc = "ff":
        return getFFPortfolio()
    elif vc == "kpcb":
        return getKPCBPortfolio()

if __name__ == "__main__":
	#print geta16zPortfilio()
    #print getKhoslaPortfolio()
    #print getSequoiaPortfolio()
    #print getKPCBPortfolio()
    #print getFFPortfolio()
