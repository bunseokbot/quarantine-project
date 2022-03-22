import feedparser
import requests
import re


CUSTOM_USER_AGENT = "dev team dev@gugu.com"


def get_cik_ticker_mapping():
    res = requests.get(
        "https://www.sec.gov/files/company_tickers.json"
    )
    data = res.json()
    values = [data[key] for key in data.keys()]
    mapping = {}

    for value in values:
        mapping[value['ticker']] = value['cik_str']
    
    return mapping


def get_ticker():
    res = requests.get(
        "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true",
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'}
    )
    rows = res.json()['data']['rows']

    for row in rows:
        symbol = row['symbol'].replace('/', '-')
        name = row['name']
        country = row['country']
        industry = row['industry']
        sector = row['sector']
        if "^" in symbol:
            continue

        yield symbol, name, country, industry, sector


def get_edgar_rss_feed():
    feed = feedparser.parse(
        "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb=&owner=include&start=0&count=40&output=atom",
        agent=CUSTOM_USER_AGENT,
        request_headers={
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.sec.gov',
        }
    )
    for entry in feed.entries:
        matches = re.match(r"(.*?) \- (.*?)\((.*?)\).\((.*?)\)", entry.title)
        if matches:
            form = matches.group(1)
            company = matches.group(2)
            cik = int(matches.group(3))
            report_type = matches.group(4)
            link = '/'.join(entry.link.split('/')[-2:])
            from time import mktime
            from datetime import datetime
            print(datetime.fromtimestamp(mktime(entry.updated_parsed)))
            print(form, company, cik, report_type, link)
            break


if __name__ == "__main__":
    """
    mapping = get_cik_ticker_mapping()
    for symbol, name, country, industry, sector in get_ticker():
        try:
            mapping[symbol]
        except:
            print(symbol, name)
    """
    get_edgar_rss_feed()
