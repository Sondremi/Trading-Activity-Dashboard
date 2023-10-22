from analyse import Analyse

def hovedprogram(inp):
    """
    Main program for analyzing trading transaction data.

    This program uses the Analyse class to perform various analyses and display the results based on user input.

    Args:
        inp (int): User input to select the type of analysis to perform.
            1: Dynamic analysis
            2: Static and monthly analysis
            3: Total transaction summary

    Returns:
        None
    """
    prog = Analyse()

    if inp == 1:
        # Dynamic stats
        # Stats like this week and this month
        print("-"*40)
        print(prog)
        print("Dagens dato: ", prog.dags_dato())
        print("P/L i dag: ", prog.sum_dager_tilbake(0), "kr")
        print("P/L denne uken: ", prog.denne_uken(), "kr")
        print("P/L denne mnd: ", prog.denne_mnd(), "kr")
        print("P/L i år: ", prog.dette_året(), "kr")
        print("P/L totalt: ", prog.sum_totalt(), "kr")
        print("-"*40)
        
    elif inp == 2:
        # Static stats
        # Stats like 1 week back, or 1 month back
        print("-"*40)
        print(prog)
        print("Dagens dato: ", prog.dags_dato())
        print("P/L i dag: ", prog.sum_dager_tilbake(0), "kr")
        print("P/L 1 uke: ", prog.sum_dager_tilbake(7), "kr")
        print("P/L 1 mnd: ", prog.sum_mnd_tilbake(1), "kr")
        print("P/L 3 mnd: ", prog.sum_mnd_tilbake(3), "kr")
        print("P/L 6 mnd: ", prog.sum_mnd_tilbake(6), "kr")
        print("P/L totalt: ", prog.sum_totalt(), "kr")
        print("-"*40)

    elif inp == 3:
        # Extra stats
        # Total trades, win and loss
        # And P/L ratio in %
        print("-"*40)
        print(prog)
        print("Balance: ", prog.balance(), "kr")
        print("Trades totalt: ", prog.total_trades())
        print("Price totalt: ", round(sum(prog._tot_dep), 2), "kr")
        print("Loss totalt: ", round(sum(prog._tot_wit), 2), "kr")
        print("P/L % ratio: ", prog.ratio(), "%")
        # Keep in mind that the P/L ratio will be affected by overnight fees
        print("-"*40)
    

def kjor_hovedprogram():
    """
    Secondary main program for running the original program.
    
    Calls main program with args selected by user
    
    Args:
        None
    
    Returns:
        None
    """
    print("Velg et alternativ: ")
    print("1. Dynamic stats")
    print("2. Static stats")
    print("3. Extra stats")
    print("4. All stats")
    inp = int(input("Valg: "))

    assert inp in [1, 2, 3, 4], "Velg alternativ (1-4)"
    
    if inp != 4:
        hovedprogram(inp)
    else:
        for i in range(4):
            hovedprogram(i)

kjor_hovedprogram()
