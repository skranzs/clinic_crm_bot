from imports import rolessheet


def create_patient_list_message(list_patient, tg_id):
    data, role = rolessheet.get_all_values(), ''
    for row in data:
        if row[0] == tg_id:
            role = row[2]
    if role == 'Админ':
        msg_text = ('Карточка пациента\n\n'
                    f'Пациент: {list_patient[1]} {list_patient[2]}\n\n'
                    f'Дата и время следующего приёма: {list_patient[-2]} {list_patient[-1]}\n\n'
                    f'Размер обуви: {list_patient[3]}\n'
                    f'Номер телефона: {list_patient[5]}\n\n'
                    f'Описание: {list_patient[4]}')
    else:
        msg_text = ('Карточка пациента\n\n'
                    f'Пациент: {list_patient[1]} {list_patient[2]}\n\n'
                    f'Дата и время следующего приёма: {list_patient[-2]} {list_patient[-1]}\n\n'
                    f'Размер обуви: {list_patient[3]}\n\n'
                    f'Описание: {list_patient[4]}')
    return msg_text