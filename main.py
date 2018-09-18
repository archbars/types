import os
import chardet
import json
import xml.etree.ElementTree as ET


def get_count_of_words(list_of_words):
    dict_words = {}
    for line_in_list in list_of_words:
        words = line_in_list.rstrip(" \n").split(" ")
        for i in words:
            i = i.lower()
            if len(i) >= 6:
                if dict_words.get(i, 0) == 0:
                    dict_words[i] = int(1)
                else:
                    dict_words[i] = int(dict_words[i]+1)
    sorted_words = sorted(dict_words.items(), key=lambda item: -item[1])
    list_of_10 = []
    for i in range(10):
        # print(sorted_words[i])
        list_of_10.append(sorted_words[i])
    return list_of_10


def detect_file_charset(file):
    cur_file = open(file, 'rb')
    cur_char = chardet.detect(cur_file.read()).get('encoding')  # определим кодировку
    return cur_char


def get_all_descriptions_from_json_file(file, charset):
    list_descriptions = []
    cur_file = open(file, 'r', encoding=charset)
    data = json.load(cur_file)
    list1 = data['rss']['channel']['items']
    for i in range(len(list1)):
        list_descriptions.append(list1[i]['description'])
    return list_descriptions


def get_all_descriptions_from_xml_file(file, charset):
    list_descriptions = []
    xmlp = ET.XMLParser(encoding=charset)
    tree = ET.parse(file, parser=xmlp)
    root = tree.getroot()
    for child in root.iter('description'):
        list_descriptions.append(child.text)
    return list_descriptions


def for_all_txt_files_in_script_folder():
    for d, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), 'data')):
        for file in files:
            if str(file.find(".json")) != '-1':
                # print('json')
                charset = detect_file_charset(os.path.join(d, file))
                # print(charset)
                all_descriptions = get_all_descriptions_from_json_file(os.path.join(d, file), charset)
                print("Самые встречающиеся слова в файле {} - {}".format(file, get_count_of_words(all_descriptions)))
            elif str(file.find(".xml")) != '-1':
                charset = detect_file_charset(os.path.join(d, file))
                all_descriptions = get_all_descriptions_from_xml_file("E:\handmade\PyCharm\\types2\data\\newsafr.xml",
                                                                      charset)
                print("Самые встречающиеся слова в файле {} - {}".format(file, get_count_of_words(all_descriptions)))


for_all_txt_files_in_script_folder()
