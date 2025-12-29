import pandas as pd

def merge_and_compute(df_orders, df_customers):
    merged = pd.merge(
        df_orders,
        df_customers,
        how='left',
        left_on='customer_id',
        right_on='id'
    )

    merged = merged.dropna(subset=['customer_id'])
    merged['total_price'] = merged['quantity'] * merged['unit_price']
    filtered = merged[merged['status'] == 'completed']
    filtered = filtered.reset_index(drop=True)

    return filtered