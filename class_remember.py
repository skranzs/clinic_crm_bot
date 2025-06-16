class Remember_id:
    def __init__(self):
        self.id_patient = 0
        self.flag = None
        self.id_img = []
        self.data = None

    def set_id(self, new_id):
        self.id_patient = new_id
        print(f"ID установлен: {self.id_patient}")

    def get_id(self):
        return self.id_patient

    def set_flag(self, boolean):
        self.flag = boolean

    def get_flag(self):
        return self.flag

    def set_id_img(self, id_im):
        for i in id_im:
            self.id_img.append(i)

    def set_zero_id_img(self):
        self.id_img = []

    def get_id_img(self):
        return self.id_img

    def set_data(self, new_data):
        self.data = new_data

    def get_data(self):
        return self.data

rem_id = Remember_id()
