import glob
import pandas as pd
from statistics import stdev

CSV_DIRECTORY = "Concussion Subject Data/*"
PROCESSED_CSV_TITLE = "processed_data"

FILES = glob.glob(f"{CSV_DIRECTORY}/*.csv")
DATAFRAMES = [pd.read_csv(filename) for filename in FILES]


def abs_diff(dataframe, column_name: str) -> list:
    """Return the absolute difference of values
    between each row in a given column.
    """
    column_data = dataframe[column_name].tolist()
    abs_diff_column = []
    for i in range(1, len(column_data)):
        abs_diff = abs(column_data[i] - column_data[i - 1])
        abs_diff_column.append(abs_diff)
    return abs_diff_column


def get_results(column_name: str):
    abs_diff_sum = []
    standard_deviation = []
    for frame in DATAFRAMES:
        frame = abs_diff(frame, column_name)
        abs_diff_sum.append(sum(frame))
        standard_deviation.append(stdev(frame))
    return abs_diff_sum, standard_deviation


CoPx_abs_diff_sum, CoPx_abs_diff_stdev = get_results("CoPx")
CoPy_abs_diff_sum, CoPy_abs_diff_stdev = get_results("CoPy")

subject, filename, condition, trial_number = ([] for _ in range(4))

for file_name in sorted(FILES):
    file_name = file_name.rsplit('/', 1)[-1].split('.')[0].split('_', 1)[-1]
    filename.append(file_name)
    subject.append(file_name.split('_', 1)[0])
    condition.append(file_name.rsplit('_', 1)[0].split('_', 1)[-1])
    trial_number.append(
        ''.join(s for s in file_name.split('_') if s.isdigit()))


columns = {
    'Subject': subject, 'Condition': condition, 'Trial No.': trial_number,
    'CoPx Excursion': CoPx_abs_diff_sum, 'CoPx SD': CoPx_abs_diff_stdev,
    'CoPy Excursion': CoPy_abs_diff_sum, 'CoPy SD': CoPy_abs_diff_stdev
}

new_dataframe = pd.DataFrame()
for column_name, column_data in columns.items():
    new_dataframe[column_name] = column_data

new_dataframe.to_csv(f"{CSV_DIRECTORY.split('/')[0]}/{PROCESSED_CSV_TITLE}.csv",
                     index=False, index_label=False)
