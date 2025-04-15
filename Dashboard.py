from Analysis import Analysis

def show_daily_and_running_stats(analyzer):
    print("-" * 40)
    print("📊 Daglig og løpende oversikt")
    print("Dagens dato:", analyzer.todays_date_str())
    print("P/L i dag:", analyzer.sum_days_back(0), "kr")
    print("P/L denne uken:", analyzer.this_week(), "kr")
    print("P/L denne måneden:", analyzer.this_month(), "kr")
    print("P/L i år:", analyzer.this_year(), "kr")
    print("P/L totalt:", analyzer.sum_total(), "kr")

def show_historical_stats(analyzer):
    print("-" * 40)
    print("📆 Historisk oversikt")
    print("Dagens dato:", analyzer.todays_date_str())
    print("P/L i dag:", analyzer.sum_days_back(0), "kr")
    print("P/L siste uke:", analyzer.sum_days_back(7), "kr")
    print("P/L siste måned:", analyzer.sum_months_back(1), "kr")
    print("P/L siste 3 måneder:", analyzer.sum_months_back(3), "kr")
    print("P/L siste 6 måneder:", analyzer.sum_months_back(6), "kr")
    print("P/L totalt:", analyzer.sum_total(), "kr")

def show_summary(analyzer):
    print("-" * 40)
    print("📈 Total oppsummering")
    print("Kontobalanse:", analyzer.balance(), "kr")
    print("Totalt antall trades:", analyzer.total_trades())
    print("Antall overnight-fees:", analyzer.overnight_fees()[0])
    print("Sum overnight-fees:", analyzer.overnight_fees()[1], "kr")
    print("Sum innskudd:", round(sum(analyzer._tot_dep), 2), "kr")
    print("Sum uttak:", round(sum(analyzer._tot_wit), 2), "kr")
    print("Win-rate:", analyzer.win_ratio(), "%")

def main():
    """
    Main program for analyzing trading transactions.

    Uses the Analysis class to display different types of analyses based on user selection.

    The user is presented with the following options:
        1: Daily and running statistics (day, week, month, year, total)
        2: Historical statistics (1 week, 1-6 months, total)
        3: Total summary (trades, deposits, withdrawals, P/L ratio)
        4: Shows all statistics combined

    Returns:
        None
    """

    analysis = Analysis()

    print("Velg visning:")
    print("1. Daglig og løpende statistikk")
    print("2. Historisk statistikk")
    print("3. Total oppsummering")
    print("4. Vis alt")
    choice = int(input("Valg (1-4): "))

    if choice < 1 or choice > 4:
        print("Ugyldig valg, vennligst velg mellom 1 og 4.")
        return
    
    if choice == 1:
        show_daily_and_running_stats(analysis)
    elif choice == 2:
        show_historical_stats(analysis)
    elif choice == 3:
        show_summary(analysis)
    elif choice == 4:
        show_daily_and_running_stats(analysis)
        show_historical_stats(analysis)
        show_summary(analysis)

if __name__ == "__main__":
    main()
