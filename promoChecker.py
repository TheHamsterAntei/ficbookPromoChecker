import numpy as np
import cloudscraper
import re
import time
import scipy.stats as stats


allowed_list = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
allowed_list += 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'


def main():
    scraper = cloudscraper.create_scraper()
    f = open('parsed.txt', 'w')
    dict_fics = {}
    for i in range(0, 100000):
        time.sleep(np.random.choice([0.002, 0.008, 0.01, 0.015]))
        print(str(100000 - i) + " осталось")
        response = scraper.get("https://ficbook.net/")
        if response:
            text = response.text
            found = re.findall('h4.*h4', text)
            found.pop(0)
            for j in range(0, len(found)):
                found[j] = found[j][3:len(found[j]) - 4]
                found[j] = ''.join(o for o in found[j] if o in list(allowed_list))
                if found[j] not in dict_fics.keys():
                    dict_fics[found[j]] = 1
                else:
                    dict_fics[found[j]] += 1
            print('Кол-во итераций: ' + str(i + 1))
            print('Выдано фанфиков: ' + str(len(dict_fics.keys())))
            print(max(dict_fics.values()))
            print(min(dict_fics.values()))
            math = 0
            items = list(dict_fics.items())
            item_values = []
            perfect_values = []
            for j in range(1, len(items) + 1):
                math += j * items[j - 1][1] / ((i + 1) * 10)
                item_values.append(j * items[j - 1][1] / ((i + 1) * 10))
                perfect_values.append(j / len(items))
            disper = 0
            for j in range(1, len(items) + 1):
                disper += ((j * items[j - 1][1] / ((i + 1) * 10) - math)**2) * items[j - 1][1] / ((i + 1) * 10)
            deviation = disper**0.5
            print('Мат. ожидание: ' + str(math))
            print('Дисперсия: ' + str(disper))
            print('Отклонение: ' + str(deviation))
            print('Вероятность случайности отклонения: ' + str(stats.mannwhitneyu(item_values, perfect_values,
                                                                                  use_continuity=False, method='exact',
                                                                                  alternative='two-sided').pvalue))
    try:
        f.write(
            'Мат. ожидание: ' + str(math) + '\n' +
            'Дисперсия: ' + str(disper) + '\n' +
            'Отклонение: ' + str(deviation) + '\n' +
            'Ожидание: ' + str(1 / 300) + '\n'
        )
    except Exception:
        f.write(
            'ОШИБКА ВЫЧИСЛЕНИЯ СТАТИСТИЧЕСКИХ ЗНАЧЕНИЙ\n'
        )
    for i in dict_fics.keys():
        f.write(i + ' / попался ' + str(dict_fics[i]) + ' раз\n')


if __name__ == '__main__':
    main()
