import requests
from bs4 import BeautifulSoup
import openpyxl
import datetime

# https://www.amazon.in/s?k= biscuit &page=2

site = "https://www.amazon.in/s?k="

#to match
keyword = "biscuit"
excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'Britannia'
sheet.append(
    ["Platform", "Date", "Category", "Brand name", "Product Name", "Rating", "Reviews", "Discount", "Size", "Price/g",
     "Keyword", "Actual price", "Offer price", "Delivery Date", "Page Number", "Item Number"])


def soupExtract(site, keyword,brand=0,page=1):
    if brand !=0:
        sheet.title = brand
    url = site + keyword + "&page=" + str(page)
    while True:
        try:
            req = requests.get(url)
            req.raise_for_status()
            print("\nSuccess\n")
            soup = BeautifulSoup(req.text, "html.parser")
            break

        except Exception as e:
            print("Retrying...",end =" ")
    a = soup.find('span', class_='rush-component s-latency-cf-section').find_all('span')
    name = soup.find('span', class_='rush-component s-latency-cf-section').find_all('span',
                                                                                    class_='a-size-base-plus a-color-base a-text-normal')
    price = soup.find('span', class_='rush-component s-latency-cf-section').find_all('span', class_='a-price-whole')
    rating = soup.find('span', class_='rush-component s-latency-cf-section').find_all('span', class_='a-icon-alt')
    reviews = soup.find('span', class_='rush-component s-latency-cf-section').find_all('span',
                                                                                       class_='a-size-base s-underline-text')
    beforeprice = soup.find('span', class_='rush-component s-latency-cf-section').find_all('span',
                                                                                           class_='a-price a-text-price')
    weightPerGram = soup.find('span', class_='rush-component s-latency-cf-section').find_all('span',
                                                                                             class_='a-size-base a-color-secondary')
    delivery = soup.find('span', class_='rush-component s-latency-cf-section').find_all('span',
                                                                                        class_='a-color-base a-text-bold')
    print(url)
    rdt = []
    rdt.append(["Platform", "Date", "Category", "Brand name", "Product Name", "Rating", "Reviews", "Discount", "Size",
                "Price/g", "Keyword", "Actual price", "Offer price", "Delivery Date"])

    for i in range(len(name)):
        if page == 7 & i == 10:
            break
        try:
            pl = 'Amazon'
            dt = datetime.datetime.now().strftime("%x")
            ct = 'Biscuits'
            bn = name[i].text.split()[0]
            n = " ".join(name[i].text.split()[:-1])
            n = name[i].text.split(',')[0]
            # n = name[i].text
            r = float(rating[i].text.split()[0].replace(',', ''))
            re = int(reviews[i].text.replace(',', ''))
            # discount
            si = name[i].text.split()[-1]
            wpg = weightPerGram[i].text
            k = keyword
            b = float(beforeprice[i].text.split('₹')[1].replace(',', ''))
            p = float(price[i].text.replace(',', ''))
            de = delivery[i].text
            di = b - p
            di = di / b
            di = di * 100
            di = round(di, 2)
            di = str(di) + "%"
        except:
            pass
        #keyword
        if k.lower() not in name[i].text.lower():
            continue
        if (brand != 0) & (bn != brand):
            continue
        rdt.append([pl, dt, ct, bn, n, r, re, di, si, wpg, k, b, p, de, page, i + 1])
        sheet.append([pl, dt, ct, bn, n, r, re, di, si, wpg, k, b, p, de, page, i + 1])

    if page == 1:
        totalPages = soup.find('span', class_='s-pagination-item s-pagination-disabled').text

        # totalPages = soup.find('span', class_="s-pagination-item s-pagination-next s-pagination-disabled ").text
        print(totalPages)
        return totalPages



# totalpages = soupExtract(site,'bourbon biscuit','Britannia')
# for i in range(2,int(totalpages)+1):
#     soupExtract(site,keyword,i)


keywords = ['biscuit']
for keyword in keywords:
    totalpages = soupExtract(site, keyword, 'Britannia')
    for i in range(2, int(totalpages) + 1):
        try:
            soupExtract(site, keyword, 'Britannia', i)
        except:
            pass
excel.save("Data.xlsx")
