Login_User_id = ''
def get_id():
    try:
        with open('Customer.txt', 'r') as file:
            lines = file.readlines()
            
            if not lines:
                return 1001
            line = lines[-1]
            #print(line)
            last_id = int(line.split(',')[2])
            return last_id + 1
            #print(lines)
            
    except FileNotFoundError:
        return 1001
#print(get_id())

def get_accountnumber():
    try:
        with open('Customer.txt', 'r') as file:
            lines = file.readlines()
            
            if not lines:
                return 100000001
            line = lines[-1]
            last_accountnumber = int(line.split(',')[1])
            return last_accountnumber + 1
            #print(lines)
            
    except FileNotFoundError:
        return 100000001


def check_username():
    global Login_User_id
    while True:
        user_name = input('Enter your user_name:')
        user_found = False
        try:
            with open('customer.txt', 'r') as file:
                
                for line in file:
                    details = line.strip().split(',')
                    if len(details) >= 5:
                        userid = details[2]
                        username = details[3]
                        password = details[4]
                        if user_name == username:
                            user_found = True
                            for attempt in range (3):
                                user_password = input('Enter your user_password:')
                                if user_password == password:
                                    print('Access Successful!')
                                    Login_User_id = userid
                                    return

                                print(f'Incorrect password. Attempts left: {2 - attempt}')
                            print('Access Denied! Too many failed attempts.')
                            login()
                            break
                    break                            
            if not user_found:
                print('Customer not found.')
                print('1. Try again')
                print('2. Create customer')
                print('3. Exit ')
                choice = input('Enter number 1 or 3 :')
                if choice == '1':
                    continue
                elif choice == '2':
                    create_customer()
                elif choice == '3':
                    print('Exiting...')
                    login()
                    return
        except FileNotFoundError:
            print("Customer file not found.")
            return
        
    

#print(get_accountnumber())


def unique_username():
    while True:
        try:
            use_name = input('Enter username: ')
            username_exists = False

            try:
                with open('user_name.txt', 'r') as file:
                    for line in file:
                        user_name = line.strip().split(',')
                        if use_name == user_name[0]:
                            username_exists = True
                            break
            except FileNotFoundError:
                # If file doesn't exist, assume no users yet
                pass

            if username_exists:
                print('Username already exists! Enter another username.')
            else:
                with open('user_name.txt','a')as file:
                    file.write(f'{use_name}\n')
                    return use_name

        except Exception as e:
            print(f"An error occurred: {e}")
            break


def create_customer():
    name = input('Enter name:')
    nic_number = input('Enter your NIC_Number:')
    user_id = get_id()
    accountnumber = get_accountnumber()
    use_name =unique_username()
    password = input('Enter user password: ')
    
    while True:
        try:
            balance = float(input('Enter initial balance: '))
            if balance <= 0:
                print('Balance must be greater than 0!')
            else:
                break
        except ValueError:
            print('Enter number only!')

        
    while True:
        account_type = input('Enter account_type as(savings_account or current_account: )').strip().lower()
        if account_type == 'savings_account':
            statement = 'savings_account'
            break
        elif account_type == 'current_account':
            statement = 'current_account'
            break
        else:
            print("Invalid account type. Please enter 'savings_account' or 'current_account'.")
 
    with open('Customer.txt', 'a') as file:
        file.write(f'{name},{accountnumber},{user_id},{use_name},{password},\n')
    with open('balance.txt','a')as file:
        file.write(f'{user_id},{balance},{statement}\n')
    with open('nic.txt','a')as file:
        file.write(f'{user_id},{nic_number},\n')
    
    print(f"Customer account created successfully. Assigned accountnumber: {accountnumber}.Assigned user_ID:{user_id}")


def action_deposit():
    global Login_User_id
    if Login_User_id is None:
        print("Please log in first!")
        return

    action = 'deposit'
    while True:
        try:
            amount = float(input('Enter the deposit amount: '))
            if amount <= 0:
                print('Deposit amount must be greater than 0.')
            else:
                break
        except ValueError:
            print('Invalid input! Please enter a valid number for the deposit.')

    try:
        # Read balance file and update the balance
        with open('balance.txt', 'r') as ffile:
            lines = ffile.readlines()
        
        updated = False
        for i, line in enumerate(lines):
            datas = line.strip().split(',')
            if len(datas) >= 3:
                bal_user_id = datas[0]
                balance = float(datas[1])
                statement = datas[2]
                
                if Login_User_id == bal_user_id:
                    balance += amount
                    lines[i] = f'{bal_user_id},{balance},{statement}\n'
                    updated = True
                    print('Deposit successful!')
                    break
        
        # If the user was found, write the updated data back to balance.txt
        if updated:
            with open('balance.txt', 'w') as ffile:
                ffile.writelines(lines)
            
            # Write the transaction to the transaction file
            from datetime import datetime
            with open('transactions.txt', 'a') as file:
                date_time = datetime.now().strftime('%d-%m-%Y %A %I.%M %p')
                file.write(f'{Login_User_id},{date_time},{action},{amount}\n')
        else:
            print('User not found in balance file.')

    except Exception as e:
        print(f"An error occurred: {e}")
        

def action_withdrow():
    action = 'withdraw'
    while True:
        try:
            amount = float(input('Enter the withdrawl amount: '))
            if amount <= 0:
                print('Withdrawl amount must be greater than 0.')

            else:
                #break
            # Read balance file and update the balance
                with open('balance.txt', 'r') as ffile:
                    lines = ffile.readlines()
                
                updated = False
                for i, line in enumerate(lines):
                    datas = line.strip().split(',')
                    if len(datas) >= 3:
                        bal_user_id = datas[0]
                        balance = float(datas[1])
                        statement = datas[2]
                        if amount > balance:
                            print('Invalid Withdrawal! Your withdrawl amount is greater than your balance.')
                            #return
                        else:
                            if Login_User_id == bal_user_id:
                                balance -= amount
                                lines[i] = f'{bal_user_id},{balance},{statement}\n'
                                updated = True
                                print('Withdrow successful!')
                                break
                break
        except ValueError:
            print('Invalid input! Please enter a valid number for the withdrow.')

    # If the user was found, write the updated data back to balance.txt
    if updated:
        with open('balance.txt', 'w') as ffile:
            ffile.writelines(lines)
        
        # Write the transaction to the transaction file
        from datetime import datetime
        with open('transactions.txt', 'a') as file:
            date_time = datetime.now().strftime('%d-%m-%Y %A %I.%M %p')
            file.write(f'{Login_User_id},{date_time},{action},{amount}\n')
    else:
        print('User not found in balance file.')

    

def view_balance():
    global Login_User_id
    try:
        with open('balance.txt','r')as ffile:
            for file_line in ffile:
                datas = file_line.strip().split(',')
                if len(datas) >= 3:
                    bal_user_id = datas[0]
                    balance = datas[1]
                    statement = datas[2]
                    if Login_User_id == bal_user_id:
                        print(f'Your balance is {balance} in {statement}\n')
                        return
        print('User data not found!')
    except FileNotFoundError:
        return None
    

def transaction_history():
    global Login_User_id
    try:
        with open('transactions.txt','r')as file:
            details = file.readlines()
            for i, line in enumerate(details):
                data = line.strip().split(',')
                if len(data) >= 4:
                    userid = data[0]
                    date = data[1]
                    action = data[2]
                    amount = data[3]
                    if Login_User_id in userid:
                        print(f'{date} : {action} : {amount}\n')
    except FileNotFoundError:
        return None
    
def admin_menu():
    while True:
        print('\nADMIN MENU')
        print('1. Create Customer')
        print('2. Deposit Money')
        print('3. Withdraw Money')
        print('4. View Balance')
        print('5. View Transactions')
        print('6. Exit')
        choice = input('Enter a number (1-6): ')
        if choice == '1':
            create_customer()
        elif choice == '2':
            check_username()
            action_deposit()
        elif choice == '3':
            check_username()
            action_withdrow()
        elif choice == '4':
            check_username()
            view_balance()
        elif choice == '5':
            check_username()
            transaction_history()
        elif choice == '6':
            print('Exiting...')
            login()
            break
        else:
            print('Invalid option. Please enter a number from 1 to 6.')

def customer_menu():
    while True:
        print('\nCUSTOMER MENU')
        print('1. Deposit Money')
        print('2. Withdraw Money')
        print('3. View Balance')
        print('4. View Transactions')
        print('5. Exit')
        choice = input('Enter a number (1-5): ')
        if choice == '1':
            action_deposit()

        elif choice == '2':
            action_withdrow()

        elif choice == '3':
            view_balance()
        
        elif choice == '4':
            transaction_history()
            
        elif choice == '5':
            print('Exiting...')
            login()
            break
           
        else:
            print('Invalid option. Please enter a number from 1 to 5.')
                           

                           



with open('user.txt','w')as file:
    file.write(f'admin,1234\n')



def login():
    print('======login======')
    print('1. Admin')
    print('2. Customer')      
    print('3. Exit') 

    login = input('Enter number(1-3):').strip()
    while True:
        if login == '1':
            user_name = input('Enter user name:')
            user_password = input('Enter password:')
            log_in = False
            with open ('user.txt','r')as file:
                for line in file:
                    username,password = line.strip().split(',')
                    if username == user_name and password == user_password:
                        print('Admin login sucessful!')
                        log_in = True
                        admin_menu()
                        break
                        
            if not log_in:
                print('Admin login failed. Invalid username or password.')

        elif login == '2':
            check_username()
            customer_menu()
            break
        elif login == '3':
            print('Exiting...')
            exit()
            break
        break
login()
                    




    





        
