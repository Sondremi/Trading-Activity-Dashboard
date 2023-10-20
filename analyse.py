import datetime as dt
import csv

class Analyse:
    """
    Analyse class for processing trading transaction data.

    Keep in mind that:
    - csv file reads as 'TransactionHistory.csv'
    - you have to export the file as a csv file
    - csv file uses delimiter ';'
    - Date is formatted 'dd/mm/yyyy'
    - P/L from transaction is index 8 and date is index 0 from file
    """
    def __init__(self):
        """
        Initialize the Analyse object.

        This method initializes the object and loads data from the 'TransactionHistory.csv' file.
        It also separates transactions into different categories (total, deposit, withdrawal, bank transfers).

        Args:
            None

        Returns:
            None
        """
        self._fil = "TransactionHistory.csv"
        self._data = [] # All data from file
        self._trans = [] # All transactions
        self._tot_dep = [] # Total deposit
        self._tot_wit = [] # Total withdrawal
        self._bank_trans = [] # All bank transfers
        self._antall_ikke_trades = 0
        self.les_fra_fil()
    
    def __str__(self):
        """
        Return a string representation of the Analyse object.

        Args:
            None

        Returns:
            str: A string representation of the object.
        """
        return "Oversikt over trading transaksjoner"
    
    def les_fra_fil(self):
        """
        Read data from the CSV file and categorize transactions.

        This method reads data from the 'TransactionHistory.csv' file, separates transactions into different categories, 
        and stores them in respective lists.

        Args:
            None

        Returns:
            None
        """
        for linje in open(self._fil, encoding='utf-8'):
            data = linje.strip().split(';')

            if not data[0].startswith("Transaction Date"): # Skip header
                self._data.append(data)

                transaksjon_tall = (float(data[8])) # Save transaction P/L as number
                self._trans.append(transaksjon_tall) # All transactions P/L goes here
                
                if data[3] == 'Online Transfer Cash In' or data[3] == 'Online Transfer Cash Out':
                    self._bank_trans.append(transaksjon_tall) # Adding bank transfers
                elif data[8][0] == "-":
                    self._tot_wit.append(transaksjon_tall) # Adding loss
                else:
                    self._tot_dep.append(transaksjon_tall) # Adding win

    def dags_dato(self):
        """
        Get today's date.

        Returns the current date in the format 'dd/mm/yyyy'.

        Args:
            None

        Returns:
            str: Today's date in the format 'dd/mm/yyyy'.
        """
        dags_dato = str(dt.datetime.now()).strip().split()
        dags_dato = dags_dato[0].split('-')
        dags_dato = f"{dags_dato[2]}/{dags_dato[1]}/{dags_dato[0]}"
        return dags_dato

    def sum_totalt(self):
        """
        Calculate the total sum of all transactions.

        Returns the sum of all transactions minus bank transfers.

        Args:
            None

        Returns:
            float: The sum of all transactions minus bank transfers.
        """
        return round(sum(self._trans) - (sum(self._bank_trans)), 2)

    def sum_dager_tilbake(self, dager_tilbake):
        """ 
        Collects all transactions from the current date up to dager_tilbake days back and 
        adds the value of the transactions to a list.

        Args:
            dager_tilbake (int): Total days counting back.

        Returns:
            float: Sum of transactions within the specified days.

        Works for any date within the given range.
        """
        transaksjoner_dager_tilbake = [] # List holds all transactions args days back
        dags_dato = dt.datetime.now()  # Get the current date
        cutoff_date = dags_dato - dt.timedelta(days=dager_tilbake)  # Calculate the cutoff date

        for transaksjon in self._data:
            transaksjon_tall = float(transaksjon[8])
            transaksjon_dato = dt.datetime.strptime(transaksjon[0].split()[0], '%d/%m/%Y')  # Split and take only the date part, not time

            # Check if the transaction date is within the specified range
            # Also leaves out any bank-transfers
            if transaksjon_dato >= cutoff_date and transaksjon[3] != 'Online Transfer Cash In' and transaksjon[3] != 'Online Transfer Cash Out':
                transaksjoner_dager_tilbake.append(transaksjon_tall)

        return round(sum(transaksjoner_dager_tilbake), 2)
      
    def sum_mnd_tilbake(self, måneder_tilbake):
        """ 
        Collects all transactions from the current date up to måneder_tilbake months back and 
        adds the value of the transactions to a list.

        Args:
            måneder_tilbake (int): Total months counting back.

        Returns:
            float: Sum of transactions within the specified months.

        Works for any date within the given range.
        """
        transaksjoner_mnd_tilbake = [] # List holds all transactions args months back
        dags_dato = dt.datetime.now()  # Get the current date
        cutoff_date = dags_dato - dt.timedelta(days=måneder_tilbake * 30)  # Calculate the cutoff date

        for transaksjon in self._data:
            transaksjon_tall = float(transaksjon[8])
            transaksjon_dato = dt.datetime.strptime(transaksjon[0].split()[0], '%d/%m/%Y') # Split and take only the date part, not time

            # Check if the transaction date is within the specified range
            # Also leaves out any bank-transfers
            if transaksjon_dato >= cutoff_date and transaksjon[3] != 'Online Transfer Cash In' and transaksjon[3] != 'Online Transfer Cash Out':
                transaksjoner_mnd_tilbake.append(transaksjon_tall)

        return round(sum(transaksjoner_mnd_tilbake), 2)
      
    def denne_uken(self):
        """
        Calculate the sum of transactions for the current week.

        Returns the sum of transactions for the current week.

        Args:
            None

        Returns:
            float: Sum of transactions for the current week.
        """
        date = dt.datetime.now() # Monday is weekday 0, etc.
        ukedag = date.weekday()
        return self.sum_dager_tilbake(ukedag+1)

    def denne_mnd(self):
        """
        Calculate the sum of transactions for the current month.

        Returns the sum of transactions for the current month.

        Args:
            None

        Returns:
            float: Sum of transactions for the current month.
        """
        dags_dato = self.dags_dato().split('/')
        return self.sum_dager_tilbake(int(dags_dato[0]))
    
    def dette_året(self):
        """
        Calculate the sum of transactions for the current year.

        Returns the sum of transactions for the current year.

        Args:
            None

        Returns:
            float: Sum of transactions for the current year.
        """
        dags_dato = self.dags_dato().split('/')
        transaksjoner_dette_året = []

        for transaksjon in self._data:
            transaksjon_tall = float(transaksjon[8])
            transaksjon_dato = transaksjon[0][0:10].split('/')
            

            # Check if year match
            # And ignores bannk-transfers
            if dags_dato[2] == transaksjon_dato[2] and transaksjon[3] != 'Online Transfer Cash In' and transaksjon[3] != 'Online Transfer Cash Out': 
                transaksjoner_dette_året.append(transaksjon_tall)
               
        return round(sum(transaksjoner_dette_året), 2)
    
    def balance(self):
        """
        Calculate the current bank balance.

        Returns the current bank balance.

        Args:
            None

        Returns:
            float: current bank balance.
        """
        return self._data[0][10]

    def ratio(self):
        """
        Calculate the win/loss ratio of all trades.

        Returns the win/loss ratio of all trades.

        Args:
            None

        Returns:
            float: win/loss ratio.
        """
        price, loss = 0, 0

        for transaksjon in self._data:
            if transaksjon[2] == 'Trade Receivable':
                price += 1
            elif transaksjon[2] == 'Trade Payable':
                loss += 1
        
        return round((loss / price), 2)
    
    def total_trades(self):
        """
        Calculate the amount of trades done.

        Returns the amount of trades.

        Args:
            None

        Returns:
            float: amount of trades.
        """
        for transaksjon in self._data:
            # checks overnight-fees and bank-transfers
            if transaksjon[2] != 'Trade Receivable' and transaksjon[2] != 'Trade Payable':
                self._antall_ikke_trades += 1
        return len(self._trans) - self._antall_ikke_trades
