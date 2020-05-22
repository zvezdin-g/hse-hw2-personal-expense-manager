import menu_functions as f


def balance():
    global dictionary
    frame = add_columns()
    global bank_number
    for i in range(frame.shape[0]):
        card_name = frame['Card'].iloc[i] + ' (SuperBank)'
        dictionary.update([(card_name, frame['Balance'].iloc[i])])
    return frame


def add_columns():
    global bank_number
    bf = f.table_parsing()
    bf = bf[bf.From == bank_number][:]
    df = f.table_parsing()
    new_df = df[['From', 'Date and time']]
    bank_filter = new_df[new_df.From == bank_number][:]
    bank_filter = bank_filter.reset_index(drop=True)
    money_data = []
    balance_data = []
    card_data = []
    for i in range(bank_filter.shape[0]):
        if bf['Text'].iloc[i].split()[0] == 'Withdrawal:':
            money_data.append(int(bf['Text'].iloc[i].split()[3]) * (-1))
        elif bf['Text'].iloc[i].split()[0] == 'Transfer:':
            money_data.append(int(bf['Text'].iloc[i].split()[3]))
        balance_data.append(int(bf['Text'].iloc[i].split(',')[1].split()[1]))
        card_data.append(bf['Text'].iloc[i].split()[2].strip(':'))
    bank_filter['Card'] = card_data
    bank_filter['Money'] = money_data
    bank_filter['Balance'] = balance_data
    return bank_filter


bank_number = 480
dictionary = {}
