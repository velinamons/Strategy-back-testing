import csv

import pandas as pd
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile


async def send_csv_content(message: types.Message, file_path: str, caption: str = None):
    try:
        # Open the CSV file
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            # Skip the header (first row)
            next(csv_reader)

            # Read all rows and convert them into a string (to send as text)
            csv_content = "\n".join([", ".join(row) for row in csv_reader])

        # Send the CSV content to the user as text
        if caption:
            # Send the CSV with the caption (as Markdown)
            await message.answer(f"{caption}\n\n{csv_content}", parse_mode=ParseMode.MARKDOWN)
        else:
            # Send the CSV content without caption
            await message.answer(csv_content, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await message.answer(f"An error occurred: {e}")


async def send_image(message: types.Message, file_path: str, caption: str = None):
    try:
        # Prepare the image file for sending
        image_file = FSInputFile(file_path)

        # Send the image to the user
        await message.answer_photo(image_file, caption=caption)

    except Exception as e:
        # Handle any errors that occur while sending the image
        await message.answer(f"An error occurred while sending the image: {e}")


def format_csv(stats_path: str) -> str:
    # Read the CSV file
    df = pd.read_csv(stats_path)

    # Extract column names (metrics)
    metrics = df.columns.tolist()

    # Initialize result text
    result_text = "Backtest Results:\n\n"

    # Iterate over each row (each asset's results)
    for _, row in df.iterrows():
        asset = row["Metric"]  # The asset name (BTCUSDT, ETHUSDT, etc.)
        result_text += f"Metric,{asset}\n"

        # Iterate over all metrics (skip "Metric" column itself)
        for metric in metrics[1:]:
            result_text += f"{metric},{row[metric]}\n"

        result_text += "\n"  # Add spacing between assets

    return result_text