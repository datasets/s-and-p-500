import pandas as pd

def process():
    # Load data
    print("Loading data...")
    df_shiller = pd.read_excel('archive/shiller.xls', sheet_name='Data', index_col= 1)
    print("Data loaded successfully")
    # Data Manipulation
    df_sliced = df_shiller.iloc[6:,:]
    df_sliced.columns = df_sliced.iloc[0]
    df_sliced = df_sliced[1:]
    df_sliced['Date'] = df_sliced['Date'].astype(str).str.replace('.','-') + '-01'
    df_sliced['Date'] = df_sliced['Date'].astype(str).str.replace('-1-','-01-')
    df_sliced = df_sliced.loc[:, ~df_sliced.columns.duplicated()]
    print(f"Shape of the data: {df_sliced.shape}")
    header = [
        'Date',
        'SP500',
        'Dividend',
        'Earnings',
        'Consumer Price Index',
        'Long Interest Rate',
        'Real Price',
        'Real Dividend',
        'Real Earnings',
        'PE10'
        ]
    header_original = [
        'Date',
        'P',
        'D',
        'E',
        'CPI',
        'Rate GS10',
        'Price',
        'Dividend',
        'Earnings',
        'TR CAPE'
    ]
    df_sliced['P'] = df_sliced.index
    print("Saving data...")
    # Change the column headers
    print("Changing column headers...")
    df_sliced = df_sliced[header_original]
    df_sliced.columns = header
    df_sliced = df_sliced.reset_index(drop=True)
    ## Remove the footnote and fill the missing values with empty string
    round_cols = ['Dividend',
        'Consumer Price Index',
        'Long Interest Rate',
        'Real Price',
        'Real Dividend',
        'Real Earnings',
        'PE10']
    df_sliced.drop(df_sliced.tail(1).index,inplace=True)
    df_sliced.loc[:, df_sliced.columns != 'Date'] = df_sliced.loc[:, df_sliced.columns != 'Date'].apply(pd.to_numeric)
    df_sliced = df_sliced.infer_objects().fillna(0)
    for col in round_cols:
        df_sliced[col] = df_sliced[col].astype(float).round(2)
    df_sliced.to_csv('data/data.csv', index=False)
    print("Data saved successfully")

if __name__ == '__main__':
    process()