class EditIdMessage:
    def __init__(self):
        self.id = 0

    def set_id(self, new_id):
        self.id = new_id
        print(f"ID установлен: {self.id}")

    def get_id(self):
        return self.id

edit_id = EditIdMessage()
