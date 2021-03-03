from selenium import webdriver
from PIL import Image
import time, datetime, threading, random, os, pyimgur

try:
    f = open("/last_date.txt", 'r')
    f.close()
except Exception:
    f = open("/last_date.txt", 'w')
    f.write('nyon')
    f.close()
try:
    f = open("/off.txt", 'r')
    f.close()
except Exception:
    f = open("/off.txt", 'w')
    f.close()
try:
    f = open("/link.txt", 'r')
    f.close()
except Exception:
    f = open("/link.txt", 'w')
    f.close()
try:
    f = open("/rlink.txt", 'r')
    f.close()
except Exception:
    f = open("/rlink.txt", 'w')
    f.close()
# Webdriver
executable_path = '/chromedriver'

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--lang=ja")

CLIENT_ID = "CLIENT_ID"

im = pyimgur.Imgur(CLIENT_ID)



def remove():
    def loop():
        def write_date(date):
            try:
                f = open("/last_date.txt", 'w')
                f.write(str(date))
                f.close()
                f = open("/off.txt", 'w')
                f.write('0')
                f.close()
                f = open("/link.txt", 'w')
                f.close()
            except:
                print('error occured while writing date')
                return -1

        date = datetime.datetime.today().day
        # Check the last Date
        try:
            with open("/last_date.txt", 'r') as a:
                last_date = a.read()
        except:
            return

        if str(date) != last_date:
            if (write_date(date)) == -1:
                raise

    while True:
        try:
            loop()
            time.sleep(3600)
        except:
            print('error occured while do the remove()')
            pass


def browser_f():
    def loop():
        with open("/off.txt", 'r') as a:
            if a.read() == '1':
                return
        time.sleep(5)

        def picture(num, filename):
            hight = 45 * (num - 1)
            merged = Image.new('RGB', (560, 60 + hight))
            img = Image.open('/cache.png')
            area = (0, 265, 560, 325)
            area1 = (0, 380, 560, 378 + hight + 378)
            img1 = img.crop(area)
            img2 = img.crop(area1)
            merged.paste(img1, (0, 0))
            merged.paste(img2, (0, 60))
            merged = merged.convert("RGB")
            merged.save(filename + '.jpg')
            PATH = f"/{filename}.jpg"
            if filename == 'morning':
                try:
                    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
                    with open("/link.txt", 'a', ) as b:
                        b.write(filename + " " + uploaded_image.link)
                    return
                except:
                    time.sleep(3610)
                    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
                    with open("/link.txt", 'a', ) as b:
                        b.write(filename + " " + uploaded_image.link)
                    return
            try:
                uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
                with open("/link.txt", 'a', ) as b:
                    b.write(filename + " " + uploaded_image.link + '\n')
            except:
                time.sleep(3610)
                uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
                with open("/link.txt", 'a', ) as b:
                    b.write(filename + " " + uploaded_image.link + '\n')

        def remove_file():
            minute = 30
            hour = 17
            while 1:
                if hour >= 20:
                    break
                if minute >= 58:
                    hour += 1
                    minute = 0
                    continue
                try:
                    os.remove('/' + str(hour) + str(minute) + '.jpg')
                except:
                    time.sleep(2)
                    os.remove('/' + str(hour) + str(minute) + '.jpg')
                    pass
                minute += 3
            try:
                os.remove('/morning.jpg')
            except:
                time.sleep(2)
                os.remove('/morning.jpg')
                pass
            return 'Success'

        browser = webdriver.Chrome(executable_path=executable_path, desired_capabilities=options.to_capabilities())
        try:
            year = str(datetime.datetime.today().year)
            month = str(datetime.datetime.today().month)
            date = datetime.datetime.today().day
            num_ = 0
            morning = False
            with open("/link.txt", 'r') as file:
                read = file.read()
            with open("/link.txt", 'r') as file:
                readlines = file.readlines()

            if read == "":
                hou = 17
                minu = 30
            else:
                g = readlines[len(readlines) - 1]
                g = g.split(' ')
                if g[0] == 'morning':
                    f = open("/off.txt", 'w')
                    f.write('1')
                    f.close()
                    return
                g = g[0]
                hou = int(g[0:2])
                minu = int(g[2:len(g)])
                if minu + 3 > 57:
                    if hou + 1 > 19:
                        morning = True
                    else:
                        hou += 1
                        minu = 0
                else:
                    minu += 3
            if not morning:
                while hou < 20:
                    if minu < 60:
                        url = 'https://www.navitime.co.jp/transfer/searchlist?orvStationName=%E5%85%A5%E9%96%93%E5%B8%82&orvStationCode' \
                              '=00007307&dnvStationName=%E3%81%B2%E3%81%B0%E3%82%8A%E3%83%B6%E4%B8%98%28%E6%9D%B1%E4%BA%AC%E9%83%BD%29' \
                              '&dnvStationCode=00000108&thr1StationName=&thr1StationCode=&thr2StationName=&thr2StationCode' \
                              '=&thr3StationName=&thr3StationCode=&year=' + year + '&month=' + month \
                              + '&day=' + str(date) + '&hour=' + str(hou) + '&minute=' + str(
                            minu) + '&basis=1&sort=0&wspeed=100&airplane=1&sprexprs=1&utrexprs=1' \
                                    '&othexprs=1&mtrplbus=1&intercitybus=1&ferry=1 '
                        browser.get(url)
                        for num in range(1, 6):
                            try:
                                browser.find_element_by_xpath(
                                    '/html/body/div[1]/div/div/div[1]/ol[1]/li[' + str(num) + ']/dl/dt')
                            except:
                                num_ = num
                                break
                        browser.save_screenshot('/cache.png')
                        hmin = str(hou) + str(minu)
                        picture(num_, hmin)
                        minu += 3
                        time.sleep(random.randrange(3, 6))
                    elif minu >= 60:
                        minu = 0
                        hou += 1
            if 5 <= datetime.datetime.today().weekday() <=6:
                url = 'https://www.navitime.co.jp/transfer/searchlist?orvStationName=%E3%81%B2%E3%81%B0%E3%82%8A%E3%83%B6%E4%B8' \
                      '%98%28%E6%9D%B1%E4%BA%AC%E9%83%BD%29&orvStationCode=00000108&dnvStationName=%E5%85%A5%E9%96%93%E5%B8%82' \
                      '&dnvStationCode=00007307&thr1StationName=&thr1StationCode=&thr2StationName=&thr2StationCode' \
                      '=&thr3StationName=&thr3StationCode=&year=' + year + '&month=' + month + '&day=' + str(date) + \
                      '&hour=7&minute=20&basis=1&sort=0&wspeed=100&airplane=1&sprexprs=1&utrexprs=1&othexprs=1&mtrplbus=1' \
                      '&intercitybus=1&ferry=1 '
            else:
                url = 'https://www.navitime.co.jp/transfer/searchlist?orvStationName=%E3%81%B2%E3%81%B0%E3%82%8A%E3%83%B6%E4%B8' \
                      '%98%28%E6%9D%B1%E4%BA%AC%E9%83%BD%29&orvStationCode=00000108&dnvStationName=%E5%85%A5%E9%96%93%E5%B8%82' \
                      '&dnvStationCode=00007307&thr1StationName=&thr1StationCode=&thr2StationName=&thr2StationCode' \
                      '=&thr3StationName=&thr3StationCode=&year=' + year + '&month=' + month + '&day=' + str(date) + \
                      '&hour=7&minute=25&basis=1&sort=0&wspeed=100&airplane=1&sprexprs=1&utrexprs=1&othexprs=1&mtrplbus=1' \
                      '&intercitybus=1&ferry=1 '
            browser.get(url)
            for num in range(1, 6):
                try:
                    browser.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/ol[1]/li[' + str(num) + ']/dl/dt')
                except:
                    num_ = num
                    break
            browser.save_screenshot('/cache.png')
            picture(num_, 'morning')
            remove_file()
            with open("/off.txt", 'w') as a:
                a.write('1')
            print(datetime.datetime.today())
        except:
            print('error occured while browser running')
            browser.quit()
        browser.quit()
    while True:
        loop()
        time.sleep(3600)


def loopf():
    def loop_():
        minute = datetime.datetime.today().minute
        hour = datetime.datetime.today().hour
        print(minute, hour)
        if 12 <= hour < 17 or hour == 17 and minute < 30:
            hour = 17
            minute = 30
        if 19 < hour:
            hour = 19
            minute = 57
        if minute % 3 == 1:
            minute -= 1
        if minute % 3 == 2:
            if minute != 59:
                minute += 1
            else:
                minute = 57
        p_name = str(hour) + str(minute)
        if hour < 12:
            p_name = 'morning'

        with open("/link.txt", 'r') as c:
            d = c.readlines()

        for link in d:
            link = link.split(' ')
            link[1] = link[1].rstrip('\n')
            if link[0] == p_name:
                with open("/rlink.txt", 'w') as c:
                    c.write(link[1])
        print('ok')

    while True:
        loop_()
        time.sleep(60)


th = threading.Thread(target=loopf)
t1 = threading.Thread(target=remove)
th.start()
t1.start()

browser_f()
