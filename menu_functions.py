import os
import importlib
import pandas as pd
import re
import openpyxl


def add_bank_list():
    files = os.listdir('banks/')
    names = []
    for i in files:
        if '.py' in i:
            k = i.split('.')
            names.append(k[0])
    return names


def bank_import(module):
    return importlib.import_module(module, package=None)


def show_current_funds():
    print('Your current funds:')
    total = 0
    bank_modules = bank_modules_list()
    for bank in bank_modules:
        bf = bank.balance()
        for k in bank.dictionary:
            total += int(bank.dictionary[k])
            print(k + ': ' + str(bank.dictionary[k]) + ' EUR')
    print('Total: %s EUR' % total)
    press_any_key = input("Press any key ")


def expenses_per_month():
    print('Enter month and year in the following format MM-YYYY:')

    date1 = input()
    date_pattern = r"^(\d\d)(-)(\d\d\d\d)"
    date_dict = {1: 'January', 2: 'February', 3: 'March',
                 4: 'April', 5: 'May', 6: 'June',
                 7: 'July', 8: 'August', 9: 'September',
                 10: 'October', 11: 'November', 12: 'December'}
    if re.match(date_pattern, date1):
        try:
            date2 = pd.Timestamp(date1)
            date_end = pd.Timestamp(year=date2.year, month=date2.month, day=date2.days_in_month)
            print('Select a credit card:')
            names = []
            bank_modules = bank_modules_list()
            for bank in bank_modules:
                bf = bank.balance()
                for k in bank.dictionary:
                    names.append(k)
            cleared_data = sum_of_tables()
            names.append('Total')
            names.append('Exit to the main menu')
            for i in range(len(names)):
                print('%s. %s' % ((i + 1), names[i]))
            try:
                command = int(input())
                if 0 <= command <= len(names):
                    if command == (len(names)):
                        print('Exit...')
                    elif command == len(names) - 1:  # Total
                        print('Report for %s %s, all credit cards:' % (date_dict[date2.month], date2.year))
                        result = cleared_data[(cleared_data['Date and time'] > date2)
                                              & (cleared_data['Date and time'] < date_end)][
                            ['From', 'Date and time', 'Card', 'Money', 'Balance']]
                        result = result.reset_index(drop=True)
                        received = 0
                        spent = 0
                        for i in range(result.shape[0]):
                            if result['Money'].iloc[i] > 0:
                                received += result['Money'].iloc[i]
                            else:
                                spent -= result['Money'].iloc[i]
                        print('Received: %s\n'
                              'Spent: %s\n'
                              'Delta (received - spent): %s' % (received, spent, (received - spent)))
                        exp = input('Export a full report to Excel? (y/n) ')
                        while True:
                            if exp == 'y':
                                print('Processing...')
                                try:
                                    with pd.ExcelWriter('export/Total %s %s.xlsx'
                                                        % (date_dict[date2.month], date2.year)) as writer:
                                        result.to_excel(writer, sheet_name='Total for %s %s'
                                                                           % (date_dict[date2.month], date2.year))
                                        writer.sheets['Total for %s %s' %
                                                      (date_dict[date2.month], date2.year)].column_dimensions[
                                            'A'].width = 3
                                        writer.sheets['Total for %s %s' %
                                                      (date_dict[date2.month], date2.year)].column_dimensions[
                                            'C'].width = 20
                                        writer.sheets['Total for %s %s' %
                                                      (date_dict[date2.month], date2.year)].column_dimensions[
                                            'H'].width = 21
                                    wb = openpyxl.load_workbook('export/Total %s %s.xlsx'
                                                                % (date_dict[date2.month], date2.year))
                                    worksheet = wb['Total for %s %s' %
                                                   (date_dict[date2.month], date2.year)]
                                    worksheet['H2'] = 'Received:'
                                    worksheet['H3'] = 'Spent:'
                                    worksheet['H4'] = 'Delta (received - spent):'
                                    worksheet['I2'] = received
                                    worksheet['I3'] = spent
                                    worksheet['I4'] = received - spent
                                    wb.save('export/Total %s %s.xlsx'
                                            % (date_dict[date2.month], date2.year))
                                    print('Done!')
                                    break
                                except PermissionError:
                                    print('Error: close the file and try again')
                                    input('Press any key if closed')
                            elif exp == 'n':
                                break
                            else:
                                print('Error: wrong command')
                                exp = input('Enter again (y/n) ')

                    else:  # processing card separately
                        command -= 1
                        print('Report for %s %s, %s:' % (date_dict[date2.month], date2.year, names[command]))
                        result = cleared_data[(cleared_data['Date and time'] > date2)
                                              & (cleared_data['Date and time'] < date_end)][
                            ['From', 'Date and time', 'Card', 'Money', 'Balance']]
                        result = result[result.Card == names[command].split()[0]][:]
                        result = result.reset_index(drop=True)
                        received = 0
                        spent = 0
                        for i in range(result.shape[0]):
                            if result['Money'].iloc[i] > 0:
                                received += result['Money'].iloc[i]
                            else:
                                spent -= result['Money'].iloc[i]
                        print('Received: %s\n'
                              'Spent: %s\n'
                              'Delta (received - spent): %s' % (received, spent, (received - spent)))
                        exp = input('Export a full report to Excel? (y/n) ')

                        while True:
                            if exp == 'y':
                                print('Processing...')
                                try:
                                    with pd.ExcelWriter('export/%s %s %s.xlsx'
                                                        % (names[command].strip('*'), date_dict[date2.month],
                                                           date2.year)) as writer:
                                        result.to_excel(writer, sheet_name='%s %s'
                                                                           % (date_dict[date2.month], date2.year))

                                        writer.sheets['%s %s' %
                                                      (date_dict[date2.month],
                                                       date2.year)].column_dimensions[
                                            'A'].width = 3
                                        writer.sheets['%s %s' %
                                                      (date_dict[date2.month],
                                                       date2.year)].column_dimensions[
                                            'C'].width = 20
                                        writer.sheets['%s %s' %
                                                      (date_dict[date2.month],
                                                       date2.year)].column_dimensions[
                                            'H'].width = 21
                                    wb = openpyxl.load_workbook('export/%s %s %s.xlsx'
                                                                % (names[command].strip('*'), date_dict[date2.month],
                                                                   date2.year))
                                    worksheet = wb['%s %s' %
                                                   (date_dict[date2.month], date2.year)]
                                    worksheet['H2'] = 'Received:'
                                    worksheet['H3'] = 'Spent:'
                                    worksheet['H4'] = 'Delta (received - spent):'
                                    worksheet['II2'] = received
                                    worksheet['I3'] = spent
                                    worksheet['I4'] = received - spent
                                    wb.save('export/%s %s %s.xlsx'
                                            % (names[command].strip('*'), date_dict[date2.month], date2.year))
                                    print('Done!')
                                    break
                                except PermissionError:
                                    print('Error: close the file and try again')
                                    input('Press any key if closed')
                            elif exp == 'n':
                                break
                            else:
                                print('Error: wrong command')
                                exp = input('Enter again (y/n) ')
                else:
                    print('Error: choose a command from the list')
            except ValueError:
                print('Error: enter a number')
        except ValueError:
            print('Error: incorrect date')
    else:
        print('Error: incorrect date')


def table_parsing():
    filename = 'SMS.csv'
    read = pd.read_csv(filename, ';')
    df = pd.DataFrame(columns=['From', 'Date and time', 'Text'])
    bank_modules = bank_modules_list()
    banks_numbers = []
    for bank in bank_modules:
        banks_numbers.append(bank.bank_number)
    for number in banks_numbers:
        df = df.append(read[read.From == number])
    df['Date and time'] = pd.to_datetime(df['Date and time'],
                                         format='%Y-%m-%d')
    df = df.sort_values(by=['Date and time'])
    df = df.reset_index(drop=True)
    return df


def sum_of_tables():
    bank_modules = bank_modules_list()
    data_frame = pd.DataFrame(columns=['From', 'Date and time', 'Card', 'Money', 'Balance'])
    for bank in bank_modules:
        added_columns = bank.add_columns()
        data_frame = data_frame.append(added_columns, ignore_index=True)
    data_frame = data_frame.sort_values(by=['Date and time'])
    data_frame = data_frame.reset_index(drop=True)
    return data_frame


def bank_modules_list():
    bank_list = add_bank_list()
    bank_modules = []
    for name in bank_list:
        bank_modules.append(bank_import('banks.' + name))
    return bank_modules
