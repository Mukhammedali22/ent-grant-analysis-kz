import re

professions = []

def read_file(file_name: str) -> list[str]:
    with open(file=file_name, mode="r", encoding="utf8") as file:
        return file.readlines()

def clean(input_file, output_file):
    lines = read_file(file_name=input_file)

    record = True # записываем нужные строки
    isKvota = False
    flag = False # чтобы склеить предложение Список ...
    list_of_words = []

    with open(file=output_file, mode="w", encoding="utf8") as file:
        for i in range(len(lines)):
            # очищащем строку от ненужных символов с друх сторон
            lines[i] = lines[i].strip(";_\n")

            # убирает лишние ; внутри строки
            if re.search(r";{2,}", lines[i]):
                lines[i] = re.sub(r";{2,}", ";", lines[i])

            # чтобы пропустить нумерацию страницы
            if lines[i].isdigit():
                continue

            # пропускаем пустую строку
            # if len(lines[i]) == 0:
            #     continue

            if record is True:
                # ищем название ГОПа
                # if re.search(r"^(B|BM|6B)\d+ - .+", lines[i]):
                if re.search(r"^B|6B|BM - .+", lines[i]):
                    if lines[i].startswith("6B"):
                        isKvota = True

                    record = False
                    # print(i, lines[i])
                    file.write(f"\n{lines[i]}\n")

                    prof = lines[i].split(" - ")[0]
                    if lines[i] not in professions:
                        professions.append(lines[i])

                    continue
                # филиал МГУ
                elif re.search(r"(\d+\.\d+\.\d+) - .+", lines[i]): #works
                    # 24.05.03 - Испытание летательных аппаратов
                    record = False
                    # print(i, lines[i])
                    file.write(f"\n{lines[i]}\n")

                    prof = lines[i].split(" - ")[0]
                    if lines[i] not in professions:
                        professions.append(lines[i])

                    continue
                
                # Склеиваем предложение
                if lines[i].startswith("Список"):
                    flag = True
                elif lines[i].startswith("Справочник"):
                    break
                    flag = True
                elif "ОТДЕЛЕНИЕ" in lines[i]:
                    continue
            
                if len(lines[i]) == 0:
                    if flag is True:
                        flag = False
                        text = " ".join(list_of_words)
                        # print(text)
                        file.write(f"\n{text}\n")
                        list_of_words.clear()
                if flag:
                    list_of_words.append(lines[i])
                    continue


                if len(lines[i]) != 0:
                    if "ОБЛАСТЬ" in lines[i]:
                        file.write(f"\n")
                    if "ШЫМКЕНТ" == lines[i]:
                        file.write(f"\n")
                    if "ФОРМА ОБУЧЕНИЯ" in lines[i]:
                        file.write(f"\n")

                    # if lines[i].startswith("Справочник"):
                    #     file.write("\n")  
                    file.write(f"{lines[i]}\n")

            else:
                if lines[i].startswith("№"):
                    # print(i, lines[i])
                    record = True
                    file.write(f"{lines[i]}\n")
                if re.search(r"^(\d+) - .+", lines[i]): # works
                    # 031 - Карагандинский университет имени академика Е.А. Букетова
                    # univer = lines[i]
                    file.write(f"{lines[i]}\n")
                if isKvota and re.search("Преимущественное право:", lines[i]):
                    lines[i] = re.sub("(Преимущественное право: .+)", r"\1", lines[i])
                    file.write(f"{lines[i]}\n")        



def prepare(input_file, output_file):
    lines = read_file(file_name=input_file)

    spisok = False
    isKvota = False
    isSerpin = False
    isTarget = False
    privilege = "Общий конкурс"
    univer_code = None
    speciality_code = None
    isReducedEdu = False
    edu_form = "Полная"
    header = "№;ИКТ;Фамилия, Имя, Отчество;ЕНТ;ВУЗ;ГОП;Примечание;Форма обучения"

    test_f = open(file="test.txt", mode="w", encoding="utf8")

    with open(file=output_file, mode="w", encoding="utf8") as file:
        
        file.write(f"{header}\n")
        for i in range(len(lines)):
            lines[i] = lines[i].strip()

            if not spisok:
                if lines[i].startswith("Список обладателей"):
                    privilege = "Общий конкурс"
                    if "общему конкурсу" in lines[i]:
                        # print(lines[i])
                        isKvota = False
                        privilege = "Общий конкурс"
                    elif "педагогическим группам" in lines[i]:
                        isKvota = False
                        privilege = "Пед"
                    elif "сельскохозяйственным группам" in lines[i]:
                        isKvota = False
                        privilege = "СельХоз"
                    elif "Министерства здравоохранения" in lines[i]:
                        isKvota = False
                        privilege = "Мед"
                    elif "сельской молодежи, переселяющихся в регионы" in lines[i]:
                        isKvota = False
                        isSerpin = True
                        privilege = "Серпін"
                    elif "западных регионов и вновь созданных областей" in lines[i]:
                        isKvota = False
                        isTarget = True
                        privilege = "Целевой грант"
                    elif "без попечения родителей" in lines[i]:
                        isKvota = True
                        privilege = "Сирота"
                    elif "лиц с инвалидностью с детства" in lines[i]:
                        isKvota = True
                        privilege = "Инвалид"
                    elif "к ветеранам Великой Отечественной войны" in lines[i]:
                        isKvota = True
                        privilege = "УВОВ"
                    elif "четыре и более несовершеннолетних детей" in lines[i]:
                        isKvota = True
                        privilege = "МнС"
                    elif "из числа неполных семей" in lines[i]:
                        isKvota = True
                        privilege = "НепС"
                    elif "воспитывающих детей с инвалидностью" in lines[i]:
                        isKvota = True
                        privilege = "СВинв"
                    elif "лиц казахской национальности, не являющихся гражданами" in lines[i]:
                        isKvota = True
                        privilege = "Кандас"
                    elif "олимпиад" in lines[i]:
                        isKvota = False

                        univer_code = "-"
                        speciality_code = "-"
                        privilege = "Олимпиада"
                        
                        # Пока не включаем поступивших без ент
                        break
                    elif "государственных и правоохранительных органов" in lines[i]:
                        univer_code = "-"
                        speciality_code = "-"
                        privilege = "Гос"
                    elif "обучение иностранных граждан" in lines[i]:
                        univer_code = "-"
                        speciality_code = "-"
                        privilege = "Иност"

                # Извлекаем код ГОП
                if re.search(r"^B|6B|BM - .+", lines[i]):
                    # B001 - Педагогика и психология
                    # 6B01 - Педагогические науки
                    # Heriot-Watt (АРУ, 6B07, KZ-UK) - Heriot-Watt (АРУ, 6B07, KZ-UK)
                    # СКУ (US, 6B05) - СКУ (US, 6B05)
                    speciality_code = re.findall(r"B\d+|6B\d+|BM\d+", lines[i])[0]
                    # print(speciality_code)
                    if lines[i].startswith("6B"):
                        isKvota = True

                    # spisok = True
                elif re.search(r"(\d+\.\d+\.\d+) - .+", lines[i]): #works
                    # филиал МГУ
                    # извлекаем код ГОП
                    # 24.05.03 - Испытание летательных аппаратов
                    # spisok = True
                    isKvota = False
                    speciality_code = lines[i].split(" - ")[0]
                    # print(i, speciality_code)

                # извлекаем код университета если она указана
                if re.search(r"^\d+ - .+", lines[i]):
                    univer_code = lines[i].split(" - ")[0]
                    # print(i, univer_code)

                # начало списка
                if lines[i].startswith("№"):
                    # print(lines[i])
                    spisok = True
                    # file.write(f"{header}\n")
                elif spisok and len(lines[i]) == 0:
                    spisok = False
                if "ОЧНАЯ СОКРАЩЕННАЯ" in lines[i]:
                    isReducedEdu = True
                    edu_form = "Сокращенная"


                # print(i, privilege, edu_form)


            else:

                # конец списка
                if len(lines[i]) == 0:
                    spisok = False
                    # если что вернешь iskvota
                    # 1;003024277;Ж Д М;62 (44,3%);B057 (KZ-UK)

                    # isKvota = False
                    isSerpin = False
                    isTarget = False
                    continue

                # Написать имена в прописным буквами, пример: Иван Иванов Иванович
                person = re.findall(r"\;([\D ]+)\;", lines[i])

                # делим ФИО
                if len(person) == 1:
                    person = person[0].split()
                    # print(i, person, lines[i])

                # Ловим отчество и добавляем к ФИО
                if i+1 != len(lines):
                    lines[i+1] = lines[i+1].strip()
                    if lines[i+1].isalpha() and lines[i+1] != "ШЫМКЕНТ":
                        # person = person[0].split()
                        # print(i, lines[i+1])
                        person.append(lines[i+1])
                        # print(i, person)

                # if len(person) != 0:
                full_name = " ".join([name.capitalize() for name in person])
                lines[i] = re.sub(r";(\D+);", f";{full_name};", lines[i])

                # # Ловим отчество и добавляем к ФИО
                # if i+1 != len(lines):
                #     lines[i+1] = lines[i+1].strip()
                #     if lines[i+1].isalpha() and lines[i+1] != "ШЫМКЕНТ":
                #         person = re.findall(r"\;([\D ]+)\;", lines[i])
                #         person.append(lines[i+1])
                #         full_name = " ".join([name.capitalize() for name in person])
                #         lines[i] = re.sub(r";(\D+);", f";{full_name};", lines[i])
                #         # print(i, lines[i])
                #         if lines[i+1] == "ДІНМҰХАМЕДҰЛЫ":
                #             print(i, lines[i], lines[i+1])
                #         # test_f.write(f"{i} {lines[i]}\n")
                #         # continue

                if not isKvota:
                    # if "002730333" in lines[i]:
                    #     print(isKvota, privilege, i, lines[i])

                    if not lines[i].isalpha():
                        # добавляем код университета и меняем примечание
                        if len(lines[i].split(";")) == 5 and lines[i].split(";")[-1].isalpha():
                            lines[i] = lines[i].split(";")
                            prv = lines[i][-1]
                            lines[i] = ";".join(lines[i][:-1])
                            lines[i] = lines[i] + f";{univer_code};{prv}"

                        # добавляем код университета если не указано
                        if len(lines[i].split(";")) == 4:
                            lines[i] = lines[i] + f";{univer_code}"
                            # print(i, lines[i])
                            # test_f.write(f"{i} {lines[i]}\n")

                        # вставляем код ГОП до примечания
                        if len(lines[i].split(";")) == 6:
                            # print(i, lines[i])
                            lines[i] = lines[i].split(";")
                            prv = lines[i][-1]
                            # privilege = lines[i][-1]
                            # print(privilege)
                            lines[i] = ";".join(lines[i][:-1])
                            lines[i] = lines[i] + f";{speciality_code};{prv};{edu_form}"
                            test_f.write(f"{i} {lines[i]}\n")
                            file.write(f"{lines[i]}\n")
                            continue
                        
                        # добавляем ГОП, примечание и форму обученяһия
                        lines[i] = f"{lines[i]};{speciality_code};{privilege};{edu_form}"
                    
                        file.write(f"{lines[i]}\n")
                    else:
                        continue
                else:
                    if i+1 != len(lines) and lines[i+1] == "ДІНМҰХАМЕДҰЛЫ":
                        print(i, lines[i], lines[i+1])

                    if not lines[i].isalpha():
                        # убираем проценты и извлекаем код ГОП и университета
                        # вставляем под правильный формат
                        # 1;002878647;А А Д;122 (93,8%);B005 (020)
                        # 17;003056413;К А К;117 (90%);B007 (035)
                        # 17;003056413;К А К;117;B007 (035)
                        if re.search(r" \(\d{2},\d%\)| \(\d{2,3}%\)", lines[i]):
                            lines[i] = re.sub(r" \(\d{2},\d%\)| \(\d{2,3}%\)", "", lines[i])
                        else:
                            print(i, lines[i])
                        # убираем ненужную вещь
                        # 150;002974692;Қ А Ә;77 (55%);B016 (AST-ALM) (007)
                        # 150;002974692;Қ А Ә;77 (55%);B016  (007)
                        if re.search(r" *\(\D+\)", lines[i]):
                            lines[i] = re.sub(r" *\(\D+\)", "", lines[i])

                        # if "002730333" in lines[i]:
                            # print(i, lines[i])

                        # меняем местами ГОП и код университета
                        # 150;002974692;Қ А Ә;77;B016  (007)
                        # 150;002974692;Қ А Ә;77;007;B016
                        if re.search(r"(B|BM)(\d{2,3}) *\((\d{3})\)", lines[i]):
                            lines[i] = re.sub(r"(B|BM)(\d{2,3}) *\((\d{3})\)", r"\3;\1\2", lines[i])

                        # добавляем код университета
                        # 001 - Медицинский университет Астана
                        # 1;002921848;А Н;122;BM087
                        # 1;002921848;А Н;122;001;BM087
                        if len(lines[i].split(";")) == 5:
                            lines[i] = lines[i].split(";")
                            speciality_code = lines[i][-1]
                            lines[i][-1] = univer_code
                            lines[i].append(speciality_code)
                            # print(i, lines[i])


                            lines[i] = ";".join(lines[i])
                            # print(i, lines[i])

                        if len(lines[i].split(";")) == 6:                        
                            # print(lines[i])
                            lines[i] = lines[i] + f";{privilege};{edu_form}"
                            test_f.write(f"{lines[i]}\n")
                        if len(lines[i].split(";")) < 6:
                            test_f.write(f"{lines[i]}\n")

                        file.write(f"{lines[i]}\n")



                

def test(file_name):
    lines = read_file(file_name=file_name)

    isGood = True
    with open(file="test.txt", mode="w", encoding="utf8") as file:
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
            if len(lines[i].split(";")) < 8:
                isGood = False
                file.write(f"{i} {lines[i]}\n")

    if isGood:
        print("Good")
    else:
        print("Bad")




clean(input_file="src\\Список грантов 2024.csv", output_file="src\\grant2024_1.csv")
prepare(input_file="src\\grant2024_1.csv", output_file="src\\grant2024_final_list.csv")
test("src\\grant2024_final_list.csv")


with open("src\\ГОПы.csv", "w", encoding="utf8") as file:
    file.write("N;Код ГОПа;Наименование ГОПа\n")
    for profession in professions:
        profession = profession.replace(" - ", ";")
        file.write(f";{profession}\n")

# print(len(prof_code), sorted(list(prof_code)))