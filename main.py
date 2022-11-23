from genericpath import isdir
import flet, requests, os
from cairosvg import svg2png
from flet import Page, Text, Dropdown, dropdown, Column, Image, Row, theme
from bs4 import BeautifulSoup

cities = [
    "Balatonfüred",
    "Békéscsaba",
    "Budapest",
    "Debrecen",
    "Eger",
    "Győr",
    "Kaposvár",
    "Kecskemét",
    "Keszthely",
    "Miskolc",
    "Nyíregyháza",
    "Pécs",
    "Salgótarján",
    "Siófok",
    "Szeged",
    "Szekszárd",
    "Székesfehérvár",
    "Szolnok",
    "Szombathely",
    "Veszprém",
    "Zalaegerszeg",
]

# ========== DEFAULT DATAS ==========

city = "Győr"
url = f"https://www.idokep.hu/idojaras/{city}"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")
temp = soup.find_all("div", class_="ik current-temperature")
weather = soup.find_all("div", class_="ik current-weather")
weather_image = soup.find_all("img", class_="ik forecast-bigicon pe-2 pd-md-0")
weather_image_src = weather_image[0]["src"]
weather_image_svg = f"https://www.idokep.hu{weather_image_src}"
weather_image_filname = weather_image_src.split(sep="/")[-1][:-4]
if os.path.isdir("images") == False:
    os.mkdir("images")
weather_image_png = f"images/{weather_image_filname}.png"
if not os.path.isfile(weather_image_png):
    svg2png(url=weather_image_svg, write_to=weather_image_png)
    

# ========== ENTRY POINT ==========


def main(page: Page):   
    page.window_width = 400
    page.window_height = 400
    page.title = "WeatherApp (Időkép) v1.0"
    page.horizontal_alignment = "center"

    def refresh_city(e):
        url = f"https://www.idokep.hu/idojaras/{dd.value}"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        temp = soup.find_all("div", class_="ik current-temperature")
        temp_text.value = temp[0].string
        weather = soup.find_all("div", class_="ik current-weather")
        weather_text.value = weather[0].string
        weather_image = soup.find_all("img", class_="ik forecast-bigicon pe-2 pd-md-0")
        weather_image_src = weather_image[0]["src"]
        weather_image_svg = f"https://www.idokep.hu{weather_image_src}"
        weather_image_filname = weather_image_src.split(sep="/")[-1][:-4]
        weather_image_png = f"images/{weather_image_filname}.png"
        if not os.path.isfile(weather_image_png):
            svg2png(url=weather_image_svg, write_to=weather_image_png)
        img.src = weather_image_png
        
        temp_text.update()
        weather_text.update()
        img.update()
        

    dd = Dropdown(label="Város",
                  options=[dropdown.Option(city) for city in cities],
                  autofocus=True,
                  value=city,
                  on_change=refresh_city,)

    weather_text = Text(
        value=weather[0].string,
        text_align="center",
        size=20)
    
    temp_text = Text(
        value=temp[0].string,
        text_align="center",
        size=24,
        weight="bold")
    
    img = Image(
        src=weather_image_png,
        width=60,
        height=60,)
    
    col = Column(
        alignment="center",
        width=300,
        height=200,
        horizontal_alignment="center",
    )    
    
    col_2 = Column(
        alignment="center",
        horizontal_alignment="center",
        controls=[
            weather_text,
            temp_text
        ])
    
    row = Row(
        controls=[
            img,
            col_2
        ]
    )

    col.controls.append(dd)
    col.controls.append(row)
    col.controls.append(Row(height=170))
    col.controls.append(Text(value="© 2022 - LimJ", size=10, color="#EE7700"))
    page.add(col)

    page.update()


flet.app(target=main, assets_dir=".")