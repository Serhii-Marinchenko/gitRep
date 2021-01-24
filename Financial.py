import pandas as pd

class FinModel:
    def __init__(self):
        self.ops = pd.DataFrame(columns = ['Name', 'Dt', 'Kt', 'Sum'], index=[0])
    
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
                                      .loc[(self.finmod.get_ops()['Dt'] == self.name)\
                                           | (self.finmod.get_ops()['Kt'] == self.name)]
            df.loc['Всього'] = ['--', '--', '--', df.Sum.sum()]
            if p:
                print(f'\n{n}ахунок № {self.name}\nЗагалом\n----------------------------\n')
            return df
        yield f
        def f1(p=False):
            df1 = self.finmod.get_ops().copy(deep=False)\
                                       .loc[(self.finmod.get_ops()['Dt'] == self.name)]
            df1.loc['Всього'] = ['--', '--', '--', df1.Sum.sum()]
            if p:
                print(f'\n{n}ахунок № {self.name}\nЗа Дебетом\n----------------------------\n')
            return df1
        yield f1
        def f2(p=False):
            df2 = self.finmod.get_ops().copy(deep=False)\
                                       .loc[(self.finmod.get_ops()['Kt'] == self.name)]
            df2.loc['Всього'] = ['--', '--', '--', df2.Sum.sum()]
            if p:
                print(f'\n{n}аунок № {self.name}\nЗа кредитом\n----------------------------\n')
            return df2
        yield f2
    
    def get_net(self):
        dc = self.traverse()
        d = sum(dc[0])
        c = sum(dc[1])
        if self.active:
            net_end = self.net_b + d - c
        else:
            net_end = self.net_b + c - d
        print(f'Сальдо на початок: {self.net_b}\nОборот за дебетом: {d}\nОборот за кредитом: {c}\nСальдо на кінець: {net_end}')
        return [self.net_b, d, c, net_end]
    
    def find_subaccs(self):
        sub = self.name * 10
        for e1, e2 in zip(self.finmod.get_ops()['Dt'], self.finmod.get_ops()['Kt']):
            if (abs(e1 - sub) < 10) and (e1 not in self.subaccs):
                self.subaccs.append(Acc(e1, self.finmod))
            if (abs(e2 - sub) < 10) and (e2 not in self.subaccs):
                self.subaccs.append(Acc(e2, self.finmod))
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
            if d()['Sum'].any():
                print(d(1))
            if c()['Sum'].any():
                print(c(1))
            ansd += [d().drop('Всього', 0).Sum.sum()]
            ansc += [c().drop('Всього', 0).Sum.sum()]
            nodes_to_visit += current_node.subaccs
        return ansd, ansc
