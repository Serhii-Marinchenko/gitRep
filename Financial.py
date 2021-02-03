import pandas as pd
import random

class FinModel:
    def __init__(self):
        self.ops = pd.DataFrame(columns = ['Назва', 'Дт', 'Кт', 'Сума'], index=[0])
    
    def get_ops(self):
        return self.ops
    
    def add(self, name, acc1, acc2, _sum):
        if self.get_ops().loc[self.get_ops().index[-1]].any():
            self.ops.loc[self.get_ops().index[-1] +1] = [name, acc1, acc2, _sum]
            return
        self.ops.loc[self.ops.index[-1]] = [name, acc1, acc2, _sum]


class Acc(FinModel):
    def __init__(self, name, finmod, active=True, net_b=0):
        self.name = name
        self.finmod = finmod
        self.active = active
        self.net_b = net_b
        self.subaccs = []
        self.names = []
    
    def set_active(self, val=True):
        self.active = val
    
    def get_ops(self, p=False):
        if p:
            if self.name > 100:
                n = 'Субр'
            else:
                n = 'Р'
        def f(p=False):
            df = self.finmod.get_ops().copy(deep=False)\
                                      .loc[(self.finmod.get_ops()['Дт'] == self.name)\
                                           | (self.finmod.get_ops()['Кт'] == self.name)]
            df.loc['Всього'] = ['--', '--', '--', df.Sum.sum()]
            if p:
                print(f'\n{n}ахунок № {self.name}\nЗагалом\n------------------------------------------------------------------------------------')
            return df
        yield f
        def f1(p=False):
            df1 = self.finmod.get_ops().copy(deep=False)\
                                       .loc[(self.finmod.get_ops()['Дт'] == self.name)]
            df1.loc['Всього'] = ['--', '--', '--', df1['Сума'].sum()]
            if p:
                print(f'\n{n}ахунок № {self.name}\nЗа Дебетом\n------------------------------------------------------------------------------------')
            return df1
        yield f1
        def f2(p=False):
            df2 = self.finmod.get_ops().copy(deep=False)\
                                       .loc[(self.finmod.get_ops()['Кт'] == self.name)]
            df2.loc['Всього'] = ['--', '--', '--', df2['Сума'].sum()]
            if p:
                print(f'\n{n}аунок № {self.name}\nЗа кредитом\n------------------------------------------------------------------------------------')
            return df2
        yield f2
        
    def find(self, name):
        self.find_subaccs()
        for i in self.subaccs:
            if i.name == name:
                return i
        
    def get_net(self):
        dc = self.traverse()
        d = sum(dc[0])
        c = sum(dc[1])
        if self.active:
            net_end = self.net_b + d - c
        else:
            net_end = self.net_b + c - d
        print('------------------------------------------------------------------------------------')
        print(f'\nСальдо на початок: {self.net_b}\nОборот за дебетом: {d}\nОборот за кредитом: {c}\nСальдо на кінець: {net_end}')
        return [self.net_b, d, c, net_end]
    
    def find_subaccs(self):
        sub = self.name * 10
        for e1, e2 in zip(self.finmod.get_ops()['Дт'], self.finmod.get_ops()['Кт']):
            if (e1 - sub < 10 and e1 - sub > 0) and e1 not in self.names:
                child = Acc(e1, self.finmod)
                child.active = self.active
                self.subaccs.append(child)
                self.names.append(e1)
            if (e2 - sub < 10 and e2 - sub > 0) and (e2 not in self.names):
                child = Acc(e2, self.finmod)
                child.active = self.active
                self.subaccs.append(child)
                self.names.append(e2)
        if not self.subaccs:
            raise Exception(f'В журналі відсутні субрахунки рахунку {self.name}')
    
    def add_subacc(self, acc):
        self.subaccs.append(acc)
    
    def remove_subacc(self, acc):
        self.subaccs = [acc for acc in self.subaccs if acc != acc]
    
    def traverse(self, p=False):
        nodes_to_visit = [self]
        ansd, ansc = [], []
        while nodes_to_visit:
            current_node = nodes_to_visit.pop()
            if not current_node.subaccs:
                try:
                    current_node.find_subaccs()
                except Exception:
                    pass
            g = current_node.get_ops(1)
            next(g)
            d = next(g)
            c = next(g)
            if d()['Сума'].any():
                print(d(1))
            if c()['Сума'].any():
                print(c(1))
            ansd += [d().drop('Всього', 0)['Сума'].sum()]
            ansc += [c().drop('Всього', 0)['Сума'].sum()]
            nodes_to_visit += current_node.subaccs
        return ansd, ansc


f = FinModel()
def curry(func):
    return lambda x: lambda y: lambda z: lambda w: func(x, y, z, w)

#op = ['op' + str(i) for i in range(30)]
#dt = [630 + i for i in range(12)] + [random.randint(10, 1000) for i in range(10)] + \
#    [(630 + i) * 10 + i for i in range(10)]
#ct = [random.randint(10, 1000) for i in range(30)]
#Sum = [random.randint(100, 2000) for i in range(30)]

#while op:
    #f.add(op.pop(), dt.pop(), ct.pop(), Sum.pop())

#a63 = Acc(63, f)
#a63.get_net()

f1 = FinModel()

def curry(func):
    return lambda x: lambda y: lambda z: lambda w: func(x, y, z, w)

func = curry(f.add)

#Case 1
wr1 = ["Зареєстровано збільшення СК", 46, 401, 250000,
       "Внесок в нац. валюті", 311, 46, 96000,
       "Внесок в ін. валюті", 312, 46, 520000,
       "Внесок товарами від нерезидента", 281, 46, 780000,
       "Сплата ввізного мита", 377, 311, 780000*0.05,
       "Сплата пдв", 377, 311, 780000*0.2,
       "Включено суму ввізного мита до вартості товару", 28, 377, 780000*0.05,
       "Відображено ПК", 641, 377, 780000*0.2,
       "Внесок обладнання резидентом", 152, 46, 200000,
       "В т.ч. ПДВ", 641, 46, 40000]

while wr1:
    f1.add(wr1.pop(0), wr1.pop(0), wr1.pop(0), wr1.pop(0))
    #f1= func(ans.pop(0))
    #f2 = f1(ans.pop(0))
    #f3 = f2(ans.pop(0))
    #f3(ans.pop(0))

a377 = Acc(377, f)
#a377.get_net()

a31 = Acc(31, f)
#a31.get_net()

#Case 2
wr2 = ["Зареєстровано статутний капітал", 46, 401, 700000,
       "Внесено засновниками до СК", 311, 46, 660000,
       "Зменшено обсяг СК", 401, 46, 40000]

f2 = FinModel()
while wr2:
    f2.add(wr2.pop(0), wr2.pop(0), wr2.pop(0), wr2.pop(0))

#case 3
wr3 = [
    "Відображено заборгованість перед учасником", 452, 672, (900000-100000)*0.3,
    "Відображенно зменшення СК", 401, 452, 900000*0.3,
    "Відображено різницю між вкладом до СК і виплатою учасникові", 452, 442, 0.3*100000, 
    "Перерахування коштів учасникові", 672, 311, (900000-100000)*0.3
]

f3 = FinModel()
while wr3:
    f3.add(wr3.pop(0), wr3.pop(0), wr3.pop(0), wr3.pop(0))

#case4
wr4 = [
    "Прибуток направлено на виплату дивідендів", 441, 443, 110000,
    "Нараховано дивіденди засновникам", 443, 671, 110000,
    "Утримано ПДФО", 671, 641.1, 110000*0.05,
    "Утримано ВЗ", 671, 641.2, 110000*0.015,
    "Відвантажено товари", 361, 702, 90000,
    "Відображенно ПЗ", 702, 641, 90000/6,
    "Відображено собівартість реалізації", 902, 281, 70000,
    "Залік заборгованостей", 671, 361, 90000
]

f4 = FinModel()
while wr4:
    f4.add(wr4.pop(0), wr4.pop(0), wr4.pop(0), wr4.pop(0))

a67 = Acc(67, f4)
a67.active = 0

f4.add("Виплачено решту дивідендів", 671, 311, a67.get_net()[-1])

#case5
income_tax = 9550
income = income_tax / 0.18

wr5 = [
    "Спрямовано прибуток на виплату дивідендів", 441, 443, 100000,
    "Нараховані дивіденди фіз. особі", 443, 671.1, 35000,
    "Утримано ПДФО", 671.1, 641.1, 35000*0.05,
    "Утримано ВЗ", 671.1, 642, 35000 * 0.015,
    "Нараховані дивіденди юр. особі", 443, 671.2, 65000,
    "Сплата авансового внеску", 641.2, 311, abs(65000-income) * 0.18,
    "Сплата ПДФО", 641.1, 311, 35000*0.05,
    "Сплата ВЗ", 642, 311, 35000*0.015,
]

f5 = FinModel()
while wr5:
    f5.add(wr5.pop(0), wr5.pop(0), wr5.pop(0), wr5.pop(0))

a64 = Acc(64, f5)
a64.get_net()

a67 = Acc(67, f5); a67.active = 0
a671_1 = a67.find(671.1)
f5.add("Сплата дивідендів фіз. особі", 671.1, 311, a671_1.get_net()[-1])
#a671_1.get_net()

a671_2 = a67.find(671.2)
f5.add("Спалата дивідендів юр. особі", 671.2, 311, a671_2.get_net()[-1])

#case6
f6 = FinModel()
wr6 = [
    "Нараховано дивіденди: ", 0, 0, 0,
    "Пилипенко Д. В.", 443, 671, 15000,
    "Кирбі Ю. В. ", 443, 671, 10000,
    "ТОВ 'Зоряний шлях'", 443, 671, 75000,
    "Нараховано військовий збір", 671, 642, 25000*0.015,
    "Зареєстровано зміну СК", 46, 401, 100000,
    "Спрямовано дивіденди на збільшення СК", 671, 46, 100000,
    "Сплачено ВЗ", 642, 311, 25000*0.015,
    "Отримано кошти на сплату ВЗ", 311, 671,25000*0.015
]

while wr6:
    f6.add(wr6.pop(0), wr6.pop(0), wr6.pop(0), wr6.pop(0))

a67 = Acc(67, f6)

