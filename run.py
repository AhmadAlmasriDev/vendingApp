import gspread
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import datetime as dt
from os import system, name
from time import sleep
# Constants------------------------------------------------------------------------------
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
# TEMP_KEY={
#   "type": "service_account",
#   "project_id": "vendingapp-392515",
#   "private_key_id": "0be6093985315d571ba283c2a56b664a13b22a27",
#   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCxqxU67nXgJqKg\nYgilePd673K/8QA6EWnl3kRSxjOyDxK+0LWBUDmtVqHOEiZk92fRJPBs9crQ00GR\nWcYB3IK7xtKuE2RYJJbMDscrgfpHISsCBn9ChqEyz4LfUSM+lO7GFANxg3FBWpO4\nX75oiUpGQyE+oNZa3pCDlEuuQyF4DyehlFbpdFfiXcDjlgibUEQHvF3VzU3rzWW1\nahAzoB8zjOhCMZ3noUmnwkzPKAxb84nZCHLsZIPKlaVeQnJUs3NV6G3IniZPOByl\n7bEveZj5tRNNZZHseMRxrslAYsNalQcCagRr5mB9asxDxz2WBoSbxDuCj7W3k4D1\nQpZRKC7nAgMBAAECggEATmkWdA1EyZnTgRvy+/CArGlcB9j5hCcmSPRIzA08SHO9\njqg2yqzY36bRv0wkVMAZueRnFXd+vJ3XnKn1qOGkcvIDDh9x1DLFuKY3AX0aM2Uw\ngXLTnE0lfHK3rA43k0mQfavcfy8G/1RVyHO86Y7Z0FuVIvpB0BXUyrValzx6W2z8\niudwPeTfs89jfdGFen452QaQwlIsvDsKRTf0zBa936gTTfSB7jbI6DZKACNyn6k8\nve4wQCqbjx6wUowqTXI0O6yQ/ItNjOYEtO/qfTSJiZIUSOaLA/YuSuWhNls0kTSE\nGk6o8TIdpnUyLDjQyGHTeCPxdORHJKVlUDhcq9jB9QKBgQDXwg/uxfBuIsNmGEzv\nmT0K1QcX4oat+cSIJXMJihyzy2JRrvKChIZJM20Wh9KG4oAoiWPVZ7ZqWnLYq4O7\n2oHL/p2AAxrYwRgboymr9nuDkBOYwYWkE9RZ0cRwDySmZantfbUiyriQuUdZTEqA\nr67qIUu0N8y3VSMyvxMfvjpyowKBgQDSzlMOnzJ88TmTbMnWGW5PT1ZTpetXFdxb\nyaT8kBa1UmuJZDW6/VlLKAXVwEGInZO3xj8ErDtSqEVSvBQRb/iYM9nUg7C75MC/\nz4/czKFazG7HA6NjskfTGtZ/zN1q1j2DLrH+Zp3BUP06xv47P+G4Gk+ETmpBAHMc\nkxi2evKa7QKBgG0MpMjmOpMv9trPRXOEXBnxedhUogWky/SUGQSlTcSB83udlOzq\n1oSA/Y35sCqEqInUhyUBem1esdVZOwfjdN8KHcjpyNPtJKYzXYiQ1/SzCXSXu1gm\nvZl4MHUC8l832x8x/i9LjuV2/9zednl8Ukf79CtuWIYA/f1UHfJZT2lJAoGAMUCj\nhzcKxMZXfWpdffhTHZSbxs9tPNuOsKNcOOYxaAvptCAFrbqjsjuXoWlZ5mFqsfVP\no/fZpGZMTBhFWA2hN25l5pEeKcg4gJguNJha2qwI9daTxidRQLF0jEeBNAT6Ojwe\nuiGfmhsiDymPHKjARBNhoLfxe15vhq2XiIsRQ8ECgYEA0QmYmmoRG+wHTpzB41vG\nIJRY0Apdt4jaJ7DdNkAtl891kzDbQSWHbByGqEdr1+YW1sQ1faYg8xozGNcjfL8T\nIbiMAT5FtlMXFM9eMbwL/7ytX3mAgfdgTEtQ2PRtZ15gzp7brhujJcM1qCEAr6x7\nZbWfffwSUstX51/Tu168m+s=\n-----END PRIVATE KEY-----\n",
#   "client_email": "ahmad-991@vendingapp-392515.iam.gserviceaccount.com",
#   "client_id": "118193662085860412599",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ahmad-991%40vendingapp-392515.iam.gserviceaccount.com",
#   "universe_domain": "googleapis.com"
# }

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




class VM_Logic:
    def __init__(self):
        self.address = ""
        self.name = ""
        self.mars = 0
        self.snickers = 0
        self.twix = 0
        self.bounty = 0
        self.cash = 0
        self.date=""
        self.time=""

    def get_vm_list(self):
        """
        Return a list of the avaliable worksheets in VendingMachine workshhet (VM01) 
        """
        sheets_names=[]
        for spreadsheet in MACHINES_SHEET:
            sheets_names.append(spreadsheet.title) 
        v_machines_list = sheets_names[1:]
        v_machines_list.sort()
        return v_machines_list

    def get_date_time(self):
        date_time = dt.datetime.now()
        date = date_time.strftime("%Y-%m-%d")
        time = date_time.strftime("%H:%M")
        return [date,time]
    
    def update_vm(self, operation):
        def upload_data():
            current_row = [date_time[0], date_time[1], operation, self.mars, self.snickers, self.twix, self.bounty, self.cash]
            current_vm = MACHINES_SHEET.worksheet(self.name)
            current_vm.append_row(current_row) 

        # self.get_data(self.name)
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
            upload_data()
        elif operation == 'sell':
            upload_data()
        

        
    
    def count_sales(self,vm):
        current_date_time = self.get_date_time()
        raw_info = MACHINES_SHEET.worksheet(vm)
        data = raw_info.get_all_values()[3:]
        # print(data)
        for i in reversed(range(len(data))):
            prev_quantity = []
            data_slice = []
            if data[i][0] != current_date_time[0] or i == 0:
                # print(i)
                # print(data[i])
                data_slice = data[i:]
                count=[0 ,0 ,0 ,0]
                prev_quantity =[data[i][3],data[i][4],data[i][5],data[i][6],]
                temp_quantity =[]
                for i in range(len(data_slice)):
                    if data_slice[i][2] == 'topup':
                        temp_quantity = [data_slice[i-1][3], data_slice[i-1][4], data_slice[i-1][5], data_slice[i-1][6]]                        
                        for x in range(4):
                            count[x] += int(prev_quantity[x]) - int(temp_quantity[x])
                        prev_quantity =[MAX_STOCK, MAX_STOCK, MAX_STOCK, MAX_STOCK]
                    temp_quantity = [data_slice[i][3], data_slice[i][4], data_slice[i][5], data_slice[i][6]]    
                for i in range(4):
                    count[i] += int(prev_quantity[i]) - int(temp_quantity[i])
                
                return count

    def update_sales(self):
        def calculate_revenue():
            price = [PRICE_MARS, PRICE_SNICKERS, PRICE_TWIX, PRICE_BOUNTY]
            revenue = 0
            for item, price in zip(sales, price):
                revenue += item * price
            return revenue

        date_time = self.get_date_time()
        sales = self.count_sales(self.name)
        revenue = calculate_revenue()
        current_row = [date_time[0], sales[0], sales[1], sales[2], sales[3], revenue]
        current_vm = SALES_SHEET.worksheet(self.name)
        current_vm.append_row(current_row)      


    def get_data(self,vm):
        time_date = self.get_date_time()
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
        self.date = time_date[0]
        # self.time = time_date[1]
        
    def check_stock(self):
        alarms = []
        near_empty='stock near empty (5pcs)'
        stock_empty='stock empty'
        if self.mars == 5 :
           alarms.append(f'Mars {near_empty}')
        if self.snickers == 5 :
           alarms.append(f'Snickers {near_empty}')
        if self.twix == 5 :
           alarms.append(f'Twix {near_empty}')
        if self.bounty == 5 :
           alarms.append(f'Bounty {near_empty}')
        if self.mars == 0 :
           alarms.append(f'Mars {stock_empty}')
        if self.snickers == 0 :
           alarms.append(f'Snickers {stock_empty}')
        if self.twix == 0 :
           alarms.append(f'Twix {stock_empty}')
        if self.bounty == 0 :
           alarms.append(f'Bounty {stock_empty}')

        alarm_rows= [[self.date, self.time, item, self.address] for item in alarms]
        return alarm_rows

    def update_alarms(self):
        current_vm = ALARM_SHEET.worksheet('Alarms')
        rows = self.check_stock()
        for row in rows:
            current_vm.append_row(row)      


class VM_Admin(VM_Logic):
    def __init__(self):
        super()

    def create_vm(self,address):
        name_index = self.name_avaliable_check()
        self.address = address
        self.name = name_index[0]
        MACHINES_SHEET.duplicate_sheet(0,new_sheet_name=f'{name_index[0]}',insert_sheet_index = name_index[1])
        machines= MACHINES_SHEET.worksheet(name_index[0])
        machines.update('B1',address)

        SALES_SHEET.duplicate_sheet(0,new_sheet_name=f'{name_index[0]}',insert_sheet_index = name_index[1])
        sales= SALES_SHEET.worksheet(name_index[0])
        sales.update('B1',address)
        self.update_vm('initialize')
        self.get_data(name_index[0])
        

    
    def delete_vm(self, name):
        worksheet_to_del = MACHINES_SHEET.worksheet(f'{name}')
        MACHINES_SHEET.del_worksheet(worksheet_to_del)
    
    def name_avaliable_check(self):
        vm_list = self.get_vm_list()
        # print(len(vm_list))
        i = 1
        while (True):
            current_name = f'vm{"0" + str(i) if i < 10 else i}'
            
            if current_name not in vm_list:
                return [current_name , i]
            i += 1 

class VendingMachine():
    def __init__(self,ui,vm_logic):
        self.ui = ui
        self.vm_logic = vm_logic

    def sell(self):
        current_vm = self.ui.select_machine(self.vm_logic.get_vm_list())
        if current_vm != False:
            self.vm_logic.get_data(current_vm)
            vm_option = self.ui.machine_menu()
            if vm_option == '5':
                maintain_option = self.ui.maintenance_menu()
                self.maintain(maintain_option)
            else:
                if vm_option == '1':
                    self.vm_logic.mars -= 1
                if vm_option == '2':
                    self.vm_logic.snickers -= 1
                if vm_option == '3':
                    self.vm_logic.twix -= 1
                if vm_option == '4':
                    self.vm_logic.bounty -= 1
                self.vm_logic.update_vm('sell')
                self.vm_logic.update_sales()
                self.vm_logic.update_alarms()

    def maintain(self,option):                
        if option == '1':
            self.vm_logic.update_vm('topup')
        if option == '2':
            self.vm_logic.update_vm('cashing')

class UI():
    def __init__(self):
        self.vm =''
    
    def clear(self):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear') 

    def intro(self):
        self.clear()
        print('Welcome to VenderApp.')
        print('VenderApp as an application that imitates the work of several vending machines connected to a database.')
        print('The user can create vending machines, service them, check stock and sales informations, and get alarms')
        user_input = ' '
        while user_input != '':
            user_input= input('To start hit Enter\n')
        self.clear()

    def outro(self,op_type):
        if op_type == "buy":
            print('Thank You, for your purchase.')        
            print('Have a nice day')   
            sleep(3)
        if op_type == 'maintain':
            print('Maintenence finished')
            print('Back to main menu')
            sleep(3)
        # GO BACK TO MAIN MENU#    

    def role(self):
        print('Choose a role')
        print('1- User')
        print('2- Admin')
        while(True):
            user_input = input('Enter 1 or 2\n')
            if user_input == '1' or user_input == '2' :
                self.clear()
                self.vm = user_input
                return user_input

    def select_machine(self,avaliable_machines):
        
        if len(avaliable_machines) != 0 :
            print('Select a vending machine')
            print('Just input th machine name (example vm01)')
            print('These are the machines avaliable at the moment:') 
            print(avaliable_machines) 
            while(True):
                user_input = input ('Enter machine name\n')
                for name in avaliable_machines:
                    if name == user_input:
                        self.clear()
                        return user_input
                print ('Please, choose a name from the list.')
        else:
            print('There are no machines found.\nYou can create new machines as an Admin')
            sleep(3)
            return False

    def machine_menu(self):
        print(f'Vending machine {self.vm}') 
        print('Select a product:\n')
        print(f'1- Mars -------- {PRICE_MARS}$')
        print(f'2- Snickers ---- {PRICE_SNICKERS}$')
        print(f'3- Twix -------- {PRICE_TWIX}$')
        print(f'4- Bounty ------ {PRICE_BOUNTY}$')
        print('5- Maintenance\n')
        while(True):
            user_input = input('Enter 1 - 5\n')
            for i in range(1,6): 
                if int(user_input) == i:
                    self.clear()
                    return user_input
            print('Please, choose from the menu.')

    def maintenance_menu(self):
        print('Select:\n')
        print(f'1- Topup')
        print(f'2- Cashing\n')
        
        while(True):
            user_input = input('Enter 1 - 2\n')
            for i in range(1,2): 
                if int(user_input) == i:
                    self.clear()
                    return user_input
            print('Please, choose from the menu.')
ui = UI()
vm_logic = VM_Logic() 
cur_vm = VendingMachine(ui , vm_logic)
cur_vm.sell()


# vm = VM_Logic()
# print(test.get_vm_list())
# user = UI()
# user.intro()
# temp=user.machine_menu('vm01')
# user.outro("maintain")
# test2 = VM_Admin()
# test2.create_vm('new very long address')
# test2.get_data("vm01")
# test2.update_alarms()

# test2.update_vm('regular')
# test2.delete_vm(1)
# temp=test2.name_avaliable_check()

# print(temp)
# print(test2.get_vm_list())

# machines = MACHINES_SHEET.worksheet('vm01')

# data = machines.get_all_values()
# print(data[3:])