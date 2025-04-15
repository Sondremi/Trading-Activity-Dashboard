import datetime as dt
import csv

class Analysis:
    """
    Analysis class for processing trading transaction data.

    Keep in mind that:
    - csv file reads as 'TransactionHistory.csv'
    - you have to export the file as a csv file
    - csv file uses delimiter ';'
    - Date is formatted 'dd/mm/yyyy'
    - P/L from transaction is index 8 and date is index 0 from file
    """

    def __init__(self):
        self._fil = "TransactionHistory.csv"
        self._data = [] # All data from file
        self._trans = [] # All transactions
        self._tot_dep = [] # Total deposit
        self._tot_wit = [] # Total withdrawal
        self._bank_trans = [] # All bank transfers
        self.fees = 0

        self.amount_index = None
        self.desc_index = None
        self.date_index = None
        self.type_index = None
        self.balance_index = None

        self.read_from_file()
    
    def __str__(self):
        return f"Analyse av transaksjoner fra {self._fil}"
    
    def read_from_file(self):
        """
        Reads and categorizes transactions from the CSV file.
        This method reads data from 'TransactionHistory.csv', dynamically identifies relevant columns 
        based on their header names, and sorts transactions into appropriate categories.
        """

        with open(self._fil, encoding='utf-8') as fil:
            reader = csv.reader(fil, delimiter=';')
            headers = next(reader)

            self.amount_index = headers.index("Amount") if "Amount" in headers else headers.index("Profit")
            self.desc_index = headers.index("Description")
            self.date_index = headers.index("Transaction Date")
            self.type_index = headers.index("Action")
            self.balance_index = headers.index("Balance")

            for data in reader:
                if not data:
                    continue

                self._data.append(data)

                try:
                    transaksjon_tall = float(data[self.amount_index])
                except ValueError:
                    continue

                self._trans.append(transaksjon_tall)
                desc = data[self.desc_index]

                if desc in ['Online Transfer Cash In', 'Online Transfer Cash Out']:
                    self._bank_trans.append(transaksjon_tall)
                elif transaksjon_tall < 0:
                    self._tot_wit.append(transaksjon_tall)
                else:
                    self._tot_dep.append(transaksjon_tall)

    def todays_date_str(self):
        todays_dato = str(dt.datetime.now()).strip().split()[0].split('-')
        return f"{todays_dato[2]}/{todays_dato[1]}/{todays_dato[0]}"

    def sum_total(self):
        return round(sum(self._trans) - (sum(self._bank_trans)), 2)

    def sum_days_back(self, days_back):
        """ 
        Collects all transactions from the current date up to days_back and 
        adds the value of the transactions to a list.

        Args:
            days_back (int): Total days counting back.

        Returns:
            float: Sum of transactions within the specified days.
        """

        transactions_days_back = []
        todays_date = dt.datetime.now()
        cutoff_date = todays_date - dt.timedelta(days=days_back)

        for transaction in self._data:
            try:
                transaction_amount = float(transaction[self.amount_index])
                transaction_date = dt.datetime.strptime(transaction[self.date_index].split()[0], '%d/%m/%Y')
                if transaction_date >= cutoff_date and transaction[self.desc_index] not in ['Online Transfer Cash In', 'Online Transfer Cash Out']:
                    transactions_days_back.append(transaction_amount)
            except (ValueError, IndexError):
                continue

        return round(sum(transactions_days_back), 2)
      
    def sum_months_back(self, months_back):
        """ 
        Collects all transactions from the current date up to months_back and 
        adds the value of the transactions to a list.

        Args:
            måneder_tilbake (int): Total months counting back.

        Returns:
            float: Sum of transactions within the specified months.
        """

        transactions_months_back = []
        todays_date = dt.datetime.now()
        cutoff_date = todays_date - dt.timedelta(days=months_back * 30)

        for transaction in self._data:
            try:
                transaksjon_amount = float(transaction[self.amount_index])
                transaction_date = dt.datetime.strptime(transaction[self.date_index].split()[0], '%d/%m/%Y')
                if transaction_date >= cutoff_date and transaction[self.desc_index] not in ['Online Transfer Cash In', 'Online Transfer Cash Out']:
                    transactions_months_back.append(transaksjon_amount)
            except (ValueError, IndexError):
                continue

        return round(sum(transactions_months_back), 2)
      
    def this_week(self):
        date = dt.datetime.now()
        weekday = date.weekday()
        return self.sum_days_back(weekday + 1)

    def this_month(self):
        todays_date = int(self.todays_date_str().split('/')[0])
        return self.sum_days_back(todays_date)
    
    def this_year(self):
        todays_date = self.todays_date_str().split('/')
        transactions_this_year = []

        for transaction in self._data:
            try:
                transaction_amount = float(transaction[self.amount_index])
                transaction_date = transaction[self.date_index].split('/')

                if todays_date[2] == transaction_date[2] and transaction[self.desc_index] not in ['Online Transfer Cash In', 'Online Transfer Cash Out']:
                    transactions_this_year.append(transaction_amount)
            except (ValueError, IndexError):
                continue

        return round(sum(transactions_this_year), 2)
    
    def balance(self):
        return self._data[0][self.balance_index]

    def win_ratio(self):
        price, loss = 0, 0
        for transaction in self._data:
            if transaction[self.type_index] == 'Trade Receivable':
                price += 1
            elif transaction[self.type_index] == 'Trade Payable':
                loss += 1

        return round((loss / price), 2)
    
    def total_trades(self):
        for transaction in self._data:
            if transaction[self.type_index] not in ['Trade Receivable', 'Trade Payable']:
                self.fees += 1
        return len(self._trans) - self.fees
    
    def overnight_fees(self):
        total_overnight_fees = 0
        sum_fees = 0.0

        fee_types = ["Funding Charges", "Funding Refund", "Trading Adjustment(Div)"]

        for transaction in self._data:
            try:
                transaction_amount = float(transaction[self.amount_index])
                transaction_type = transaction[self.desc_index]

                if transaction_type in fee_types:
                    total_overnight_fees += 1
                    sum_fees += transaction_amount
            except (ValueError, IndexError):
                continue

        return total_overnight_fees, round(sum_fees, 2)
