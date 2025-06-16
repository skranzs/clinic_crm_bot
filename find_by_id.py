def upload_new_info(sheet, id_patient, cell, info):
    data = sheet.col_values(1)
    for i, name in enumerate(data):
        if name == id_patient:
            sheet.update_cell(i + 1, cell, info)