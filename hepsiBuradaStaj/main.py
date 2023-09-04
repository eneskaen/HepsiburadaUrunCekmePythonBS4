import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

class Product():
    def __init__(self, productName, productPrice,productLink , productCargoDetail, productDescription, productRate, productImage):
        self.productName = productName
        self.productPrice = productPrice
        self.productLink = productLink
        self.productCargoDetail = productCargoDetail
        self.productDescription = productDescription
        self.productRate = productRate
        self.productImage = productImage

productList = []
url = "https://www.hepsiburada.com"
searchText= input("Aranacak ürünü girin: ").strip()
def HepsiburadaSite(searchText):

    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    content = requests.get(url+"/ara?q="+str(searchText), headers=headers)
    soup = BeautifulSoup(content.content, "lxml")
    mainUnorderedList = soup.find("ul",attrs = {"class": "productListContent-frGrtf5XrVXRwJ05HUfU productListContent-rEYj2_8SETJUeqNhyzSm"})

    for i in tqdm(range(0,24)):

        product_div = mainUnorderedList.find("li",attrs= {"id": f"i{i}"})
        product_name = product_div.find("a", class_="moria-ProductCard-gyqBb")["title"].strip()
        product_link = url+product_div.find("a", class_="moria-ProductCard-gyqBb")["href"].strip()
        product_price = product_div.find("div", attrs= {"data-test-id": "price-current-price"}).text.strip()

        if "adservice" not in product_link: #Reklam Olanların Linki Düzgün Formatta Olduğu için onları atladım.
            product_cargoo_detail,product_description,product_rate,product_image = ProductPage(product_link,headers)
            productList.append(Product(product_name, product_price, product_link, product_cargoo_detail,product_description,product_rate,product_image))


def ProductPage(product_link,headers):
    productcontent = requests.get(product_link, headers=headers)
    soupProduct = BeautifulSoup(productcontent.content,"lxml")
    product_rate = soupProduct.find("span", attrs={"class":"rating-star"})
    if product_rate is not None:
        product_rate = product_rate.text.strip()
    else:
        product_rate = "Değerlendirme Yok!"
    product_cargoo_detail = soupProduct.find("span", attrs={"id":"campaignText"}).text.strip()
    product_description = soupProduct.find("div", attrs={"id":"productDescriptionContent"}).text.strip()
    product_image = soupProduct.find("a", attrs= {"class": "cloudzoom extendable"})
    product_image = product_image.find("img",attrs={"class":"product-image"})['src']
    return product_cargoo_detail,product_description,product_rate,product_image


HepsiburadaSite(searchText)

for count,i in enumerate(productList):
    print(count+1,"-) ",i.productName, i.productPrice, i.productLink , i.productCargoDetail, i.productDescription, i.productRate, i.productImage)
