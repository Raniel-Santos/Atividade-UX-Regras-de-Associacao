import csv
# Função para calcular o suporte
def support(Ix, Iy, bd):
    sup = 0
    for transaction in bd:
        if (Ix.union(Iy)).issubset(transaction):
            sup += 1
    sup = sup / len(bd)
    return sup

# Função para calcular a confiança
def confidence(Ix, Iy, bd):
    Ix_count = 0
    Ixy_count = 0
    for transaction in bd:
        if Ix.issubset(transaction):
            Ix_count += 1
            if (Ix.union(Iy)).issubset(transaction):
                Ixy_count += 1
    conf = Ixy_count / Ix_count
    return conf

# Função para eliminar regras que não atendem aos critérios de suporte e confiança mínimos
def prune(ass_rules, min_sup, min_conf):
    pruned_ass_rules = []
    for ar in ass_rules:
        if ar['support'] >= min_sup and ar['confidence'] >= min_conf:
            pruned_ass_rules.append(ar)
    return pruned_ass_rules

# Função Apriori para associação entre 2 itens
def apriori_2(itemset, bd, min_sup, min_conf):
    ass_rules = []
    ass_rules.append([])  # nível 1 (conjuntos de itens grandes)
    for item in itemset:
        sup = support({item}, {item}, bd)
        ass_rules[0].append({'rule': str(item), 'support': sup, 'confidence': 1})
    ass_rules[0] = prune(ass_rules[0], min_sup, min_conf)
    ass_rules.append([])  # nível 2 (associação de 2 itens)
    for i in range(len(ass_rules[0])):
        for j in range(i+1, len(ass_rules[0])):
            item_1 = ass_rules[0][i]
            item_2 = ass_rules[0][j]
            rule = item_1['rule'] + '_' + item_2['rule']
            Ix = {item_1['rule']}
            Iy = {item_2['rule']}
            sup = support(Ix, Iy, bd)
            conf = confidence(Ix, Iy, bd)
            ass_rules[1].append({'rule': rule, 'support': sup, 'confidence': conf})
    ass_rules[1] = prune(ass_rules[1], min_sup, min_conf)
    return ass_rules

# Carregando a base de dados a partir do arquivo CSV
transactions_bd = []
with open('../base_dados/Bullying_2018.csv', 'r') as file:
    csv_reader = csv.DictReader(file, delimiter=';')
    for row in csv_reader:
        transaction = set()
        for key, value in row.items():
            if value != ' ':
                transaction.add(key + '_' + value)
        transactions_bd.append(transaction)

# Chamando a função Apriori
itemset = list(transactions_bd[0])
result = apriori_2(itemset, transactions_bd, 0.4, 0.6)

# Exibindo os resultados
for level in result:
    print(level)

cont = input('Pressione enter para continuar...')



