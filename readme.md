# TradingProject

This Django project provides functionality to process CSV files containing financial data and convert candlestick data into a specified timeframe.

## Requirements

- Python 3.x
- Django

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/TradingProject.git
    cd TradingProject
    ```

2. Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run migrations:

    ```bash
    python manage.py migrate
    ```

## Usage

1. Start the Django development server:

    ```bash
    python manage.py runserver
    ```

2. Access the application in your web browser at `http://localhost:8000`.

3. Upload a CSV file containing financial data and specify the desired timeframe in minutes to convert the candlestick data.

## File Structure

- `TradingProject/`: Django project root directory.
- `MainApp/`: Django app for processing CSV files and candlestick data.
    - `models.py`: Defines the Candle model.
    - `views.py`: Contains the view logic for file upload and data processing.
    - `templates/`: HTML templates for rendering the UI.
    - `media/`: Directory for storing uploaded CSV files and generated JSON files.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).
