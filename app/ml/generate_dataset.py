import random
import pandas as pd


def generate_invoice_dataset():
    data = []

    # Generate normal invoices
    for _ in range(500):

        total_amount = round(random.uniform(200, 10000), 2)

        gst_amount = round(total_amount * random.uniform(0.05, 0.18), 2)

        discount = round(total_amount * random.uniform(0, 0.10), 2)

        payable_amount = round(
            total_amount + gst_amount - discount,
            2
        )

        received_amount = payable_amount

        item_count = random.randint(1, 12)

        data.append({
            "total_amount": total_amount,
            "gst_amount": gst_amount,
            "discount": discount,
            "payable_amount": payable_amount,
            "received_amount": received_amount,
            "item_count": item_count
        })

    # Generate unusual invoices
    for _ in range(20):

        total_amount = round(random.uniform(50000, 200000), 2)

        gst_amount = round(total_amount * random.uniform(0.20, 0.40), 2)

        discount = round(total_amount * random.uniform(0.40, 0.70), 2)

        payable_amount = round(
            total_amount + gst_amount - discount,
            2
        )

        received_amount = round(
            payable_amount * random.uniform(0.2, 0.5),
            2
        )

        item_count = random.randint(30, 100)

        data.append({
            "total_amount": total_amount,
            "gst_amount": gst_amount,
            "discount": discount,
            "payable_amount": payable_amount,
            "received_amount": received_amount,
            "item_count": item_count
        })

    df = pd.DataFrame(data)

    return df


if __name__ == "__main__":

    df = generate_invoice_dataset()

    output_path = "sample_data/invoices.csv"

    df.to_csv(output_path, index=False)

    print(f"Dataset created: {output_path}")
    print(f"Rows: {len(df)}")
    print("\nFirst 5 rows:")
    print(df.head())

    print("\nDataset statistics:")
    print(df.describe())