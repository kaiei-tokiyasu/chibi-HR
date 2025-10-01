import math
import pandas as pd
from tabulate import tabulate

from config import ConfigManager

class lib:
    def __init__(self):
        return

    def extractToDF(self, df, filename, sheetname, atRows, columns=None):
        df = pd.read_excel(filename, sheet_name=sheetname, skiprows=atRows, usecols=columns)
        return df

    def show_df_page(self, df):
        if df is None:
            return
        total_rows = len(df)
        if total_rows <= 0:
            print("no data available.")
            return

        page_size = ConfigManager().get("settings", "default_page_size")
        total_pages = math.ceil(total_rows/page_size)

        while True:
            try:
                u_input = input(f"\nEnter page number (1-{total_pages}, or 'q' to quit: ")
                if u_input.lower() == 'q':
                    break

                page = int(u_input)
                if 1 <= page <= total_pages:
                    start = (page-1) * page_size
                    end = start + page_size
                    print(f"\nPage {page}/{total_pages}")
                    printdf = df.iloc[start:end]
                    print(tabulate(printdf, headers='keys', tablefmt='pretty', showindex=False))
                else:
                    print(f"Invalid page number. Please enter a number between 1 and {total_pages}.")
            except ValueError:
                print("Invalid input. Please enter a valid number or 'q' to quit.")
