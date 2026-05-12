import urllib.request
import re
import pandas as pd
from html.parser import HTMLParser


class BasketPars(HTMLParser):
    def __init__(self):
        super().__init__()
        self.is_tr = False
        self.is_td = False
        self.row = []
        self.data_all = []

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.is_tr = True
            self.row = []
        if self.is_tr and tag in ["td", "th"]:
            self.is_td = True

    def handle_endtag(self, tag):
        if tag == "tr":
            self.is_tr = False
            if self.row:
                self.data_all.append(self.row)
        if tag in ["td", "th"]:
            self.is_td = False

    def handle_data(self, data):
        if self.is_td:
            self.row.append(data.strip())


def get_stats():
    searching_for = input("Введіть ім'я гравця англійською (Ім'я Прізвище): ").lower().split()

    fname, lname = searching_for[0], searching_for[1]

    folder = lname[0]
    player_id = lname[:5] + fname[:2] + "01"
    url = f"https://www.basketball-reference.com/players/{folder}/{player_id}.html"

    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
    except:
        return

    match = re.search(r'<table[^>]*id="per_game".*?</table>', html, re.DOTALL)
    tab_html = match.group(0) if match else html

    pars = BasketPars()
    pars.feed(tab_html)

    res = []
    year_re = r'^\d{4}-\d{2}$'

    for r in pars.data_all:
        if len(r) > 13 and re.match(year_re, r[0]):
            season = r[0]
            three_p = r[11]
            three_pa = r[12]

            raw_pct = r[13]
            try:
                if raw_pct:
                    val = float(raw_pct) * 100
                    pretty_pct = f"{val:.1f}%"
                else:
                    pretty_pct = "0.0%"
            except:
                pretty_pct = "0.0%"

            res.append({
                "Season": season,
                "3P_In": three_p,
                "3P_Att": three_pa,
                "3P_Pct": pretty_pct
            })

    if res:
        df = pd.DataFrame(res).drop_duplicates(subset=['Season'])
        file_name = f"{fname}_{lname}_stats.xlsx"
        df.to_excel(file_name, index=False)


get_stats()