import gspread
from google.oauth2.service_account import Credentials
import datetime as dt
from os import system, name
from time import sleep

# Constants---------------------------------------------------------------
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS_FILE = 'creds.json'
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
MACHINES_SHEET = GSPREAD_CLIENT.open('VendingMachine')
SALES_SHEET = GSPREAD_CLIENT.open('VendingSales')
ALARM_SHEET = GSPREAD_CLIENT.open('Alarms')
MACHINES_SHEET_ID = '1WgqyZJv61UsML8GGC8QygVm5rDc_4K5IeFve66Sfjp8'
SALES_SHEET_ID = '1FbPbWOSGx6rh_AAkMYSMEWlBVr_n5EkIGA-fEFsz5J8'
ALARM_SHEET_ID = '1JJfoOBQzP3t4PFv2pj6MkkTAolq6V9nA3o1Q2dzmgvU'
SHEETS_API_NAME = 'sheets'
SHEETS_API_VERSION = 'v4'

MAX_STOCK = 10
PRICE_MARS = 3
PRICE_SNICKERS = 4
PRICE_TWIX = 2
PRICE_BOUNTY = 4


# VM_Logic class ---------------------------------------------------------
class VM_Logic:
    def __init__(self):
        self.address = ""
        self.name = ""
        self.mars = 0
        self.snickers = 0
        self.twix = 0
        self.bounty = 0
        self.cash = 0
        self.date = ""
        self.time = ""

    def get_vm_list(self):
        """
        Return a list of the avaliable worksheets
        in VendingMachine workshhet (VM01)
        """
        sheets_names = []
        for spreadsheet in MACHINES_SHEET:
            sheets_names.append(spreadsheet.title)
        v_machines_list = sheets_names[1:]
        v_machines_list.sort()
        return v_machines_list

    def get_date_time(self):
        """
        Return Date and time in as list [date,time]
        """
        date_time = dt.datetime.now()
        date = date_time.strftime("%Y-%m-%d")
        time = date_time.strftime("%H:%M")
        return [date, time]

    def update_vm(self, operation):
        """
        Update the values in the work sheet
        with the data from the machine object
        Has four options:
        initialize
        cashing
        topup
        sell
        """
        def upload_data():
            current_row = [
                date_time[0],
                date_time[1],
                operation,
                self.mars,
                self.snickers,
                self.twix,
                self.bounty,
                self.cash
                ]
            current_vm = MACHINES_SHEET.worksheet(self.name)
            current_vm.append_row(current_row)
        date_time = self.get_date_time()
        if operation == 'initialize':
            self.mars = self.snickers = self.twix = self.bounty = MAX_STOCK
            self.cash = 0
            upload_data()
        elif operation == 'cashing':
            self.cash = 0
            upload_data()
        elif operation == 'topup':
            self.mars = self.snickers = self.twix = self.bounty = MAX_STOCK
            self.del_alarms()
            upload_data()
        elif operation == 'sell':
            upload_data()

    def del_alarms(self):
        """
        Delete the entries from the alarm sheet
        """
        try:
            current_vm = ALARM_SHEET.worksheet(self.name)
            data = current_vm.get_all_values()
            if len(data) > 3:
                current_vm.delete_rows(4, len(data))
        except gspread.exceptions.WorksheetNotFound as e:
            print('Trying to open non-existent sheet.')
            print(
                f'Please verify that the worksheet {e}' +
                ' exists in the Alarms spread sheet.')
            sleep(5)

    def count_sales(self, vm):
        """
        Counts quantity of sold items
        """
        current_date_time = self.get_date_time()
        raw_info = MACHINES_SHEET.worksheet(vm)
        data = raw_info.get_all_values()[3:]
        for i in reversed(range(len(data))):
            prev_quantity = []
            data_slice = []
            if data[i][0] != current_date_time[0] or i == 0:
                data_slice = data[i:]
                count = [0, 0, 0, 0]
                prev_quantity = [
                    data[i][3],
                    data[i][4],
                    data[i][5],
                    data[i][6]
                    ]
                temp_quantity = []
                for i in range(len(data_slice)):
                    if data_slice[i][2] == 'topup':
                        temp_quantity = [
                            data_slice[i-1][3],
                            data_slice[i-1][4],
                            data_slice[i-1][5],
                            data_slice[i-1][6]
                            ]
                        for x in range(4):
                            count[x] += (int(prev_quantity[x])
                                         - int(temp_quantity[x]))
                        prev_quantity = [
                            MAX_STOCK,
                            MAX_STOCK,
                            MAX_STOCK,
                            MAX_STOCK
                            ]
                    temp_quantity = [
                        data_slice[i][3],
                        data_slice[i][4],
                        data_slice[i][5],
                        data_slice[i][6]
                        ]
                for i in range(4):
                    count[i] += (int(prev_quantity[i])
                                 - int(temp_quantity[i]))
                return count

    def update_sales(self):
        """
        Updates the sales sheet with the calculated values
        """
        def calculate_revenue():
            """
            Calulate the revenue according to the prices in constants
            """
            price = [PRICE_MARS, PRICE_SNICKERS, PRICE_TWIX, PRICE_BOUNTY]
            revenue = 0
            for item, price in zip(sales, price):
                revenue += item * price
            return revenue

        date_time = self.get_date_time()
        sales = self.count_sales(self.name)
        revenue = calculate_revenue()
        current_row = [
            date_time[0],
            sales[0],
            sales[1],
            sales[2],
            sales[3],
            revenue
            ]
        try:
            current_vm = SALES_SHEET.worksheet(self.name)
            current_vm.append_row(current_row)
        except gspread.exceptions.WorksheetNotFound as e:
            print('Trying to open non-existent sheet.')
            print(
                f'Please verify that the worksheet {e}' +
                ' exists in the VendingSales spread sheet.')
            sleep(5)

    def get_data(self, vm):
        """
        Get data from the work sheet and write the values to the machine object
        """
        try:
            v_machine = MACHINES_SHEET.worksheet(vm)
            data = v_machine.get_all_values()
            last_data = data[-1]
            self.address = data[0][1]
            self.name = vm
            self.mars = int(last_data[3])
            self.snickers = int(last_data[4])
            self.twix = int(last_data[5])
            self.bounty = int(last_data[6])
            self.cash = float(last_data[7])
        except gspread.exceptions.WorksheetNotFound as e:
            print('Trying to open non-existent sheet.')
            print(
                f'Please verify that the worksheet {e}' +
                ' exists in the VendingMachine spread sheet.')
            sleep(5)

    def check_stock(self):
        """
        Check the remaining stock and return a list of row alarms
        """
        current_date_time = self.get_date_time()
        alarms = []
        near_empty = 'stock near empty (5pcs)'
        stock_empty = 'stock empty'
        if self.mars == 5:
            alarms.append(f'Mars {near_empty}')
        if self.snickers == 5:
            alarms.append(f'Snickers {near_empty}')
        if self.twix == 5:
            alarms.append(f'Twix {near_empty}')
        if self.bounty == 5:
            alarms.append(f'Bounty {near_empty}')
        if self.mars == 0:
            alarms.append(f'Mars {stock_empty}')
        if self.snickers == 0:
            alarms.append(f'Snickers {stock_empty}')
        if self.twix == 0:
            alarms.append(f'Twix {stock_empty}')
        if self.bounty == 0:
            alarms.append(f'Bounty {stock_empty}')
        alarm_rows = [[
            current_date_time[0],
            current_date_time[1],
            item, self.address
            ] for item in alarms]
        return alarm_rows

    def update_alarms(self):
        """
        Update the alarm sheet from the alarm rows list
        """
        try:
            current_vm = ALARM_SHEET.worksheet(self.name)
            rows = self.check_stock()
            for row in rows:
                current_vm.append_row(row)
        except gspread.exceptions.WorksheetNotFound as e:
            print('Trying to open non-existent sheet.')
            print(
                f'Please verify that the worksheet {e}' +
                ' exists in the Alarms spread sheet.')
            sleep(5)

    def create_vm(self, address):
        """
        Create new sheets in the machines, sales and alarm sheets
        """
        def responce(e, sheet_name):
            """
            Form the responce to return depending on the spread sheet error
            """
            print(f'An error occurred in the {sheet_name} spread sheet:\n{e}')
            sleep(5)
            return (
                f'\n With error in the {sheet_name}' +
                ' spread sheet:\n{str(e)}')
        name_index = self.name_avaliable_check()
        self.address = address
        self.name = name_index[0]
        try:
            MACHINES_SHEET.duplicate_sheet(
                0,
                new_sheet_name=f'{name_index[0]}',
                insert_sheet_index=name_index[1]
                )
            machines = MACHINES_SHEET.worksheet(name_index[0])
            machines.update_acell('B1', address)
        except gspread.exceptions.APIError as e:
            return (responce(e, 'VendingMachine'))
        try:
            SALES_SHEET.duplicate_sheet(
                0,
                new_sheet_name=f'{name_index[0]}',
                insert_sheet_index=name_index[1]
                )
            sales = SALES_SHEET.worksheet(name_index[0])
            sales.update_acell('B1', address)
        except gspread.exceptions.APIError as e:
            return (responce(e, 'VendingSales'))
        try:
            ALARM_SHEET.duplicate_sheet(
                0,
                new_sheet_name=f'{name_index[0]}',
                insert_sheet_index=name_index[1]
                )
            alarms = ALARM_SHEET.worksheet(name_index[0])
            alarms.update_acell('B1', address)
        except gspread.exceptions.APIError as e:
            return (responce(e, 'Alarm'))
        self.update_vm('initialize')
        self.get_data(name_index[0])
        return ('')

    def delete_vm(self, name):
        """
        Delete sheets in the machines, sales and alarm sheets
        """
        try:
            worksheet_to_del = MACHINES_SHEET.worksheet(f'{name}')
            MACHINES_SHEET.del_worksheet(worksheet_to_del)
        except gspread.exceptions.WorksheetNotFound as e:
            print('Trying to open non-existent sheet.')
            print(
                f'Please verify that the worksheet {e}' +
                ' exists in the VendingMachine spread sheet.')
            sleep(5)
            return (f'\nWith error: worksheet {e}' +
                    ' in the VendingMachine spread sheet not found.')
        try:
            worksheet_to_del = SALES_SHEET.worksheet(f'{name}')
            SALES_SHEET.del_worksheet(worksheet_to_del)
        except gspread.exceptions.WorksheetNotFound as e:
            print('Trying to open non-existent sheet.')
            print(
                f'Please verify that the worksheet {e}' +
                ' exists in the VendingSales spread sheet.')
            sleep(5)
            return (f'\nWith error: worksheet {e}' +
                    ' in the VendingSales spread sheet not found.')
        try:
            worksheet_to_del = ALARM_SHEET.worksheet(f'{name}')
            ALARM_SHEET.del_worksheet(worksheet_to_del)
        except gspread.exceptions.WorksheetNotFound as e:
            print('Trying to open non-existent sheet.')
            print(
                f'Please verify that the worksheet {e}' +
                ' exists in the Alarms spread sheet.')
            sleep(5)
            return (f'\nWith error: worksheet {e}' +
                    ' in the Alarms spread sheet not found.')
        return ('')

    def name_avaliable_check(self):
        """
        Check the avaliablity of machine names
        """
        vm_list = self.get_vm_list()
        i = 1
        while (True):
            current_name = f'vm{"0" + str(i) if i < 10 else i}'
            if current_name not in vm_list:
                return [current_name, i]
            i += 1


# Admin class ------------------------------------------------------------
class Admin():
    def __init__(self, ui, vm_logic):
        self.ui = ui
        self.vm_logic = vm_logic

    def admin_machines(self):
        """
        The logic behind admin options (creating, deleting)
        """
        option = self.ui.admin_menu()
        if option == "1":
            address = self.ui.address()
            exception = self.vm_logic.create_vm(address)
            self.ui.feed_back('add', exception)
        else:
            avaliable_machines = self.vm_logic.get_vm_list()
            vm_name = self.ui.select_machine(avaliable_machines)
            exception = self.vm_logic.delete_vm(vm_name)
            self.ui.feed_back('', exception)


# VendingMachine class ---------------------------------------------------
class VendingMachine():
    def __init__(self, ui, vm_logic):
        self.ui = ui
        self.vm_logic = vm_logic

    def sell(self):
        """
        The logic behind buying items
        """
        current_vm = self.ui.select_machine(self.vm_logic.get_vm_list())
        if current_vm is not False:
            self.vm_logic.get_data(current_vm)
            vm_option = self.ui.machine_menu()
            if vm_option == '5':
                maintain_option = self.ui.maintenance_menu()
                self.maintain(maintain_option)
            else:
                if vm_option == '1':
                    if self.vm_logic.mars != 0:
                        self.vm_logic.mars -= 1
                        self.vm_logic.cash += PRICE_MARS
                        state = 'buy'
                    else:
                        state = 'out'
                if vm_option == '2':
                    if self.vm_logic.snickers != 0:
                        self.vm_logic.snickers -= 1
                        self.vm_logic.cash += PRICE_SNICKERS
                        state = 'buy'
                    else:
                        state = 'out'
                if vm_option == '3':
                    if self.vm_logic.twix != 0:
                        self.vm_logic.twix -= 1
                        self.vm_logic.cash += PRICE_TWIX
                        state = 'buy'
                    else:
                        state = 'out'
                if vm_option == '4':
                    if self.vm_logic.bounty != 0:
                        self.vm_logic.bounty -= 1
                        self.vm_logic.cash += PRICE_BOUNTY
                        state = 'buy'
                    else:
                        state = 'out'
                if vm_option == '6':
                    state = 'exit'
                if state == 'buy':
                    self.vm_logic.update_vm('sell')
                    self.vm_logic.update_sales()
                    self.vm_logic.update_alarms()
                    # ---------------------------
                self.ui.outro(state)

    def maintain(self, option):
        """
        The actions taken when choosing the admin options of vending machine
        """
        if option == '1':
            self.vm_logic.update_vm('topup')
            self.ui.outro('maintain topup')
        if option == '2':
            self.vm_logic.update_vm('cashing')
            self.ui.outro('maintain cash')
        

# VM_UI ------------------------------------------------------------------
class VM_UI():
    def __init__(self):
        self.name = ''

    def clear(self):
        """
        Clear the terminal
        """
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def intro(self):
        """
        Show intro and information about the app
        """
        self.clear()
        print('Welcome to VenderApp.')
        print('VenderApp is an application that imitates the work')
        print('of several vending machines connected to a database.')
        print('The user can create and service vending machines,')
        print('check stock and sales information,')
        print('and receive alarms')
        user_input = ' '
        while user_input != '':
            user_input = input('To start hit Enter\n')

    def outro(self, op_type):
        """
        Show outro when the interaction is finished
        """
        self.clear()
        if op_type == "buy":
            print('Thank You, for your purchase.')
            print('Have a nice day')
            sleep(3)
        if op_type == "maintain topup":
            print('Maintenence finished')
            print('Vending Machine topped-up')
            print('Back to main menu')
            sleep(3)
        if op_type == "maintain cash":
            print('Maintenence finished')
            print('Vending Machine Cashed')
            print('Back to main menu')
            sleep(3)
        if op_type == "out":
            print('Sorry!')
            print('We are out of stock.')
            sleep(3)
        if op_type == "exit":
            print('Back to main menu')
            sleep(3)

    def role(self):
        """
        Show the option of what role the user wants
        """
        self.clear()
        print('Choose an option:\n')
        print('1- Vending machine')
        print('2- Admin\n')
        while (True):
            user_input = input('Enter 1 or 2\n')
            for i in range(1, 3):
                if user_input.isnumeric() and int(user_input) == i:
                    return user_input

    def select_machine(self, avaliable_machines):
        """
        Show a list of avaliable machines to the user to choose from
        """
        self.clear()
        if len(avaliable_machines) != 0:
            print('Select a vending machine')
            print('Just type the machine name (example vm01)')
            print('These are the machines avaliable at the moment:')
            print(avaliable_machines)
            while (True):
                user_input = input('\nEnter machine name:\n')
                for name in avaliable_machines:
                    if name == user_input:
                        self.name = user_input
                        return user_input
                print('Please, choose a name from the list.')
        else:
            print(
                'There are no machines found.\nYou can' +
                ' create new machines as an Admin'
                )
            sleep(3)
            return False

    def machine_menu(self):
        """
        Show the options of the current machine to choose from
        """
        self.clear()
        print(f'Vending machine {self.name}\n')
        print('Select a product:\n')
        print(f'1- Mars -------- {PRICE_MARS}$')
        print(f'2- Snickers ---- {PRICE_SNICKERS}$')
        print(f'3- Twix -------- {PRICE_TWIX}$')
        print(f'4- Bounty ------ {PRICE_BOUNTY}$')
        print('5- Maintenance\n')
        print('6- Exit\n')
        while (True):
            user_input = input('Enter 1 - 6:\n')
            for i in range(1, 7):
                if user_input.isnumeric() and int(user_input) == i:
                    return user_input
            print('Please, choose from the menu.')

    def maintenance_menu(self):
        """
        Show the maintenence menu to choose from
        """
        self.clear()
        print('Select:\n')
        print(f'1- Topup')
        print(f'2- Cashing\n')
        while (True):
            user_input = input('Enter 1 or 2\n')
            for i in range(1, 3):
                if user_input.isnumeric() and int(user_input) == i:
                    return user_input
            print('Please, choose from the menu.')

    def admin_menu(self):
        """
        Show the admin menu to shoose from
        """
        self.clear()
        print('Choose an option:\n')
        print('1- Create new vending machine')
        print('2- Delete a vending machine\n')
        while (True):
            user_input = input('Enter 1 or 2\n')
            for i in range(1, 3):
                if user_input.isnumeric() and int(user_input) == i:
                    return user_input
            print('Please, choose from the menu.')

    def address(self):
        """
        Ask the user for adress input
        """
        self.clear()
        while (True):
            user_input = input('Enter an address.\n')
            if user_input.strip() != '':
                return user_input
        print('Enter valid address, please.')

    def feed_back(self, option, exception):
        """
        Give feedback when the operation is finished
        """
        self.clear()
        if option == 'add':
            print('Vending machine added successfully.' + exception)
            sleep(5)
        else:
            print('Vending machine deleted successfully.' + exception)
            sleep(5)


def main():
    """
    The main function to initialize the code
    """
    ui = VM_UI()
    ui.intro()
    while (True):
        vm_logic = VM_Logic()
        admin = Admin(ui, vm_logic)
        vm = VendingMachine(ui, vm_logic)
        user_input = ui.role()
        if user_input == '1':
            vm.sell()
        else:
            admin.admin_machines()


main()
