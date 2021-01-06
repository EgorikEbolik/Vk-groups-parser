import vk
from time import sleep
import csv


token = "Тут был мой токен, но его нельзя показывать, поэтому введите свой"
session = vk.Session(access_token=token)
vk_api = vk.API(session)
apivers = 5.92


def iterate():

    cities = vk_api.database.getCities(
        country_id=1, need_all=0, v=apivers)

    names = [it['title'] for it in cities['items']]
    ids = [it['id'] for it in cities['items']]

    dct = dict(zip(names, ids))

    city_name = input("Введите название города: ")

    if city_name.title() in dct:
        global city_id
        city_id = dct[city_name.title()]


def get_content():

    name = input("Введите название групп: ")
    count = int(input("Введите кол-во групп: "))
    
    # Поиск групп по параметрам

    pybl = vk_api.groups.search(
        q=name, type="group", v=apivers, city_id=city_id, count=count)

    url = "https://vk.com/"

    number = pybl["items"]
    print("Количество найденных групп:", len(number))
    print("-"*40)

    zero = -1

    short = pybl['items'][zero]["screen_name"]
    ids = pybl['items'][zero]['id']
    members = vk_api.groups.getMembers(group_id=ids, v=apivers)
    lst = []
    print("Ссылки на группы:\n")

    for i in range(len(number)):

        zero += 1
        ids = pybl['items'][zero]['id']
        short = url + pybl['items'][zero]["screen_name"]
        f = 0
        try:
            members = vk_api.groups.getMembers(group_id=ids, v=apivers)
        except vk.exceptions.VkAPIError:
            print(short, "\t id:", ids, "\tКол-во подписчиков:", "скрыто")
            f = 1
        if f != 1 and members["count"] > 600:
            print(short, "\t id:", ids,
                  "\tКол-во подписчиков:", members["count"])
                  
            lst.append(
                {
                    "link" : short,
                    "id" : ids,
                    "subs" : members["count"]
                }
            )
        
        sleep(0.25)
        
    print(zero + 1)
    
    file = input("Введите путь, в которм вы хотите сохранить файл(обязательно укажите расширение файла .csv)\nПример(D:\Home\Programms\eq.csv): ")
    save_file(lst, file)
    return lst
    
    
def save_file(items, path):
    with open(path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Ссылка', 'ID', 'Кол-во подписчиков'])
        for item in items:
            writer.writerow([item['link'], item['id'],
                             item['subs']])


iterate()
get_content()


input("Нажмите Enter, чтобы выйти:")
