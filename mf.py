import pandas as pd
from datetime import datetime

class MutualFundMonitor:
    def __init__(self, data_path):
        """
        Initialize the Mutual Fund Monitor framework.

        :param data_path: Path to the mutual fund allocation dataset (CSV/Excel file).
        """
        self.data_path = data_path
        self.data = self._load_data()

    def _load_data(self):
        """
        Load the dataset into a pandas DataFrame.

        :return: pandas DataFrame containing the dataset.
        """
        try:
            return pd.read_csv(self.data_path) if self.data_path.endswith(".csv") else pd.read_excel(self.data_path)
        except Exception as e:
            raise FileNotFoundError(f"Error loading file: {e}")

    def preprocess_data(self):
        """
        Preprocess the dataset to ensure proper formats and structures.
        """
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data.sort_values(by=['Date'], inplace=True)

    def get_all_columns(self):
        """
        Get a list of all columns in the dataset.

        :return: List of column names.
        """
        return self.data.columns.tolist()

    def filter_data(self, start_date, end_date):
        """
        Filter the dataset based on a date range.

        :param start_date: Start date (string in 'YYYY-MM-DD' format).
        :param end_date: End date (string in 'YYYY-MM-DD' format).
        :return: Filtered DataFrame.
        """
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        return self.data[(self.data['Date'] >= start_date) & (self.data['Date'] <= end_date)]

    def summarize_changes(self, filtered_data, metric):
        """
        Summarize changes in the specified metric by month.

        :param filtered_data: DataFrame filtered by date range.
        :param metric: Column name to summarize (e.g., 'Net Asset Value', 'Return', 'Expense Ratio').
        :return: Summary DataFrame.
        """
        if metric not in filtered_data.columns:
            raise ValueError(f"Metric '{metric}' not found in the dataset.")

        filtered_data['Month'] = filtered_data['Date'].dt.to_period('M')
        summary = filtered_data.groupby('Month').agg({metric: ['mean', 'std']}).reset_index()
        summary.columns = ['Month', f'Average {metric}', f'Standard Deviation {metric}']
        return summary

    def display_summary(self, summary):
        """
        Display the summary data.

        :param summary: Summary DataFrame.
        """
        print(summary.to_string(index=False))

# Example Usage
if __name__ == "__main__":
    # Initialize the framework
    monitor = MutualFundMonitor("mutual_funds.csv")

    # Preprocess the data
    monitor.preprocess_data()

    # Display available columns
    columns = monitor.get_all_columns()
    print("Available Metrics:", columns)

    # User input for filtering
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    metric = input(f"Enter metric to monitor ({', '.join(columns[1:])}): ")

    # Filter and summarize
    filtered_data = monitor.filter_data(start_date, end_date)
    summary = monitor.summarize_changes(filtered_data, metric)

    # Display the summary
    monitor.display_summary(summary)
