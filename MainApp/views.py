import csv
import json
import asyncio
from django.shortcuts import render
from django.http import HttpResponse
from .models import Candle
from datetime import datetime, timedelta

# Create your views here.
async def process_candles(candles, timeframe):
    converted_data = []
    current_timeframe = timedelta(minutes=timeframe)
    previous_candle = None

    for candle in candles:
        if previous_candle:
            if candle.date == previous_candle.date and \
               candle.time - previous_candle.time <= current_timeframe:
                candle.high = max(candle.high, previous_candle.high)
                candle.low = min(candle.low, previous_candle.low)
                candle.open = previous_candle.open
            else:
                converted_data.append({
                    'date': candle.date.strftime('%Y%m%d'),
                    'open': candle.open,
                    'high': candle.high,
                    'low': candle.low,
                    'close': previous_candle.close
                })
        previous_candle = candle

    # Simulating asynchronous operation with a sleep
    await asyncio.sleep(1)  # Simulating some processing time

    return converted_data

def upload_csv(request):
    if request.method == 'POST' and request.FILES:
        csv_file = request.FILES['csv_file']
        timeframe = int(request.POST.get('timeframe'))

        # Store the uploaded CSV file on the Django server
        # Adjust 'media' folder location as per the settings
        with open(f'media/{csv_file.name}', 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)

        # Read CSV file and process data into candle objects
        candles = []
        with open(f'media/{csv_file.name}', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                candle = Candle(
                    # Populate candle attributes as per the CSV columns
                    open=row['OPEN'],
                    high=row['HIGH'],
                    low=row['LOW'],
                    close=row['CLOSE'],
                    date=datetime.strptime(row['DATE'] + row['TIME'], '%Y%m%d%H:%M'),
                )
                candles.append(candle)

        # Save candles to the database
        Candle.objects.bulk_create(candles)

        # Convert candles asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        converted_data = loop.run_until_complete(process_candles(candles, timeframe))

        # Store converted data in a JSON file
        filename = 'converted_data.json'
        with open(filename, 'w') as file:
            json.dump(converted_data, file)

        # Provide download link in the response
        response = HttpResponse(open(filename, 'rb').read())
        response['Content-Disposition'] = 'attachment; filename="converted_data.json"'
        return response
    else:
        return render(request, 'upload_csv.html')