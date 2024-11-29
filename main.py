import re
import csv


def delete_dubles(contacts_list):
    '''Объединяем записи о человеке.'''
    for person in contacts_list:
        for another_person in contacts_list:
            if person[0] in another_person[0]:
                for i in range(7):
                    if person[i] == '': 
                        person[i] = another_person[i]

    formatted_contacts_list = []
    for person in contacts_list: 
        if len(person) != 7:
            del person[7:]
        if person not in formatted_contacts_list:
            formatted_contacts_list.append(person)
    return formatted_contacts_list


if __name__ == "__main__":
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = []
        for i in rows:
            # Разбиение на правильные три - Ф И О
            full_name = i[0] + ' ' + i[1] + ' ' + i[2]
            full_name_split = full_name.split(' ', maxsplit=2)
            last_name = full_name_split[0].replace(' ', '')
            first_name = full_name_split[1].replace(' ', '')
            surname = full_name_split[2].replace(' ', '')
            list_split_full_name = [last_name, first_name, surname]
            i[0] = last_name
            i[1] = first_name
            i[2] = surname
            # Замена формата номера
            pattern = re.compile(r"(\+7|8)?[\s-]*\(?([\d]{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d+)*\s?\(?(доб.)?[\s]?(\d+)?\)?")
            new_phone_number = pattern.sub(r"+7(\2)\3-\4-\5 \6\7", i[5])
            if 'доб' not in new_phone_number:
                new_phone_number = new_phone_number.replace(' ', '')
            i[5] = new_phone_number
            # Добавление изменённых ФИО и номера в список
            contacts_list.append(i)

    formatted_contacts_list = delete_dubles(contacts_list)

    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(formatted_contacts_list)
