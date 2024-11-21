class Unit:
    def __init__(self, *args):
        self.hp = (args[0], args[1])
        self.fat = (args[2], args[3])
        self.res = (args[4], args[5])
        self.ini = (args[6], args[7])
        self.matk = (args[8], args[9])
        self.ratk = (args[10], args[11])
        self.mdef = (args[12], args[13])
        self.rdef = (args[14], args[15])
        self.params = {}
        self.calculate()

    @staticmethod
    def formula_basics(par):
        if par[1] == 0:
            return par[0] + 30
        elif par[1] == 1:
            return par[0] + 35
        elif par[1] == 2:
            return par[0] + 40
        elif par[1] == 3:
            return par[0] + 45

    @staticmethod
    def formula_res(par):
        if par[1] == 0:
            return round((par[0] + 30) * 1.25)
        elif par[1] == 1:
            return round((par[0] + 35) * 1.25)
        elif par[1] == 2:
            return round((par[0] + 40) * 1.25)
        elif par[1] == 3:
            return round((par[0] + 45) * 1.25)

    @staticmethod
    def formula_ini(par):
        if par[1] == 0:
            return par[0] + 40
        elif par[1] == 1:
            return par[0] + 45
        elif par[1] == 2:
            return par[0] + 50
        elif par[1] == 3:
            return par[0] + 55

    @staticmethod
    def formula_melee(par):
        if par[1] == 0:
            return par[0] + 20
        elif par[1] == 1:
            return par[0] + 25
        elif par[1] == 2:
            return par[0] + 30
        elif par[1] == 3:
            return par[0] + 35

    def calculate(self):
        """Рассчитываем параметры по максимуму"""
        basics = [self.hp, self.fat, self.ratk, self.rdef]
        melee = [self.mdef, self.matk]

        for i in basics:
             self.params[i] = self.formula_basics(i)

        for i in melee:
            self.params[i] = self.formula_melee(i)

        self.params[self.res] = self.formula_res(self.res)
        self.params[self.ini] = self.formula_ini(self.ini)

    def analysis(self):
        recomm = []
        if self.params[self.mdef] >= 33 and self.params[self.mdef] >= 120:
            recomm.append('Потенциальный кандидат в танки')
        if self.params[self.mdef] >= 33 and self.params[self.mdef] >= 57:
            recomm.append('Потенциальный кандидат во фланговые копейщики')
        if self.params[self.ratk] >= 100 and self.params[self.fat] >= 110:
            recomm.append('Потенциальный кандидат в лучники')
        if self.params[self.mdef] < 30 and self.params[self.matk] >= 95:
            recomm.append('Защита слабовата, годится в полеармеры')
        if self.params[self.mdef] >= 30 and self.params[self.matk] >= 90 \
                and self.params[self.fat] >= 120:
            recomm.append('Достойный воин первого ряда')
        if self.params[self.res] >= 140:
            recomm.append('Годный сержант')
        if self.params[self.matk] < 85:
            recomm.append('Слишком слабая атака, такой боец нам не нужен')
        if self.params[self.fat] < 120:
            recomm.append('Слишком низкая выносливость для рукопашника')
        if self.params[self.fat] < 100:
            recomm.append('Слишком низкая выносливость даже для сержанта и лучника')
        if self.params[self.ini] >= 175 and self.params[self.fat] >= 110:
            recomm.append('Готовый "мушкетер"')
        return recomm

    def __str__(self):
        return f'H-P: {self.params[self.hp]}\t\t\tMatk: {self.params[self.matk]}\n' \
               f'FAT: {self.params[self.fat]}\t\tRatk: {self.params[self.ratk]}\n' \
               f'RES: {self.params[self.res]}\t\t\tMdef: {self.params[self.mdef]}\n' \
               f'INI: {self.params[self.ini]}\t\tRdef: {self.params[self.rdef]}\n'


def gather_paras():
    requests = [
        input('Введите кол-во звезд: '),
        input('Введите параметр FAT: '),
        input('Введите кол-во звезд: '),
        input('Введите параметр RES: '),
        input('Введите кол-во звезд: '),
        input('Введите параметр INI: '),
        input('Введите кол-во звезд: '),
        input('Введите параметр Matk: '),
        input('Введите кол-во звезд: '),
        input('Введите параметр Ratk: '),
        input('Введите кол-во звезд: '),
        input('Введите параметр Mdef: '),
        input('Введите кол-во звезд: '),
        input('Введите параметр Rdef: '),
        input('Введите кол-во звезд: '),
    ]
    for r in requests:
        # res = r
        # while not res:
        #     print('Ошибка. Введите, пожалуйста, параметр')
        #     res = r
        # paras.append(int(res))
        paras.append(int(r))


if __name__ == '__main__':
    while True:
        print('Введите параметры')
        print('Для выхода нажмите ENTER\n')
        paras = []
        checker = input('Введите параметр HP: ')
        if not checker:
            print('До новых встреч!')
            break
        else:
            paras.append(int(checker))
        gather_paras()

        unit = Unit(*paras)
        print('*' * 50)
        print(unit)
        print('РЕКОМЕНДАЦИИ ПО РАЗВИТИЮ')
        for i in unit.analysis():
            print(i)
        print('*' * 50)
        print()
