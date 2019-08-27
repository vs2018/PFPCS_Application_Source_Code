# [1] Adapted from: Author:phihag, Date:Sep 6 '12 at 22:23, URL:https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
# [2] Adapted from: Author:lcastillov, Date:Jul 28 '16 at 18:53, URL:https://stackoverflow.com/questions/38644480/reading-json-file-with-python-3
# [3] Adapted from: Author: abarnert, Date:Jun 22 '13 at 0:55, URL:https://stackoverflow.com/questions/17246260/python-readlines-usage-and-efficient-practice-for-reading
# [4] Source: Author: Ignacio Vazquez-Abrams, Date:Dec 24 '10 at 19:51,  URL:https://stackoverflow.com/questions/4528099/convert-string-to-json-using-python
# [5] Adapted from: Author: Nader Hisham, Date:Oct 5 '17 at 3:53, URL:https://stackoverflow.com/questions/18837262/convert-python-dict-into-a-dataframe
# [6] Adapted from: Author: Gustavo Bezerra, Date:Aug 4 '17 at 3:40, URL:https://stackoverflow.com/questions/45497835/how-to-drop-duplicates-based-on-two-or-more-subsets-criteria-in-pandas-data-fram
# [7] Adapted from: Author: EdChum, Date:Jun 13 '16 at 10:45, URL:https://stackoverflow.com/questions/37787698/how-to-sort-pandas-dataframe-from-one-column
# [8] Adapted from: Author:EdChum, Date:Aug 25 '15 at 12:58, URL:https://stackoverflow.com/questions/32204631/how-to-convert-string-to-datetime-format-in-pandas-python
# [9] Adapted from: Author: Michael Hoff, Date:Jul 23 '16 at 13:42, URL:https://stackoverflow.com/questions/38542419/could-pandas-use-column-as-index
# [10] Pandas library used for creating a DataFrame, URL: https://pandas.pydata.org/pandas-docs/stable/

import datetime
import pandas as pd  # [10]
import json


class Utility:
    @staticmethod
    def get_today_date():
        today = datetime.date.today()
        return str(today)
        # return "2019-08-07"

    @staticmethod
    def save_file(api, data):  # [1]
        date = Utility.get_today_date()
        with open(f"{api}-{date}.json", "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=2)

    @staticmethod
    def save_no_date(name, data):  # [1]
        with open(f"{name}.json", "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=2)

    @staticmethod
    def open(api):  # [2]
        date = Utility.get_today_date()
        with open(f"{api}-{date}.json", "r") as handle:
            return json.load(handle)

    @staticmethod
    def open_no_date(name):  # [2]
        with open(f"{name}.json", "r") as handle:
            return json.load(handle)

    @staticmethod
    def read(file):
        arr = []
        with open(file, "r") as f:  # [3]
            x = f.readlines()
        for ls in x:
            d = json.loads(ls)  # [4]
            arr.append(d)
        return arr

    @staticmethod
    def to_uppercase(post_code):
        if post_code != None:
            return post_code.upper()
        return None

    @staticmethod
    def to_dataframe(obj):  # [5]
        return pd.DataFrame(obj)

    @staticmethod
    def drop_duplicate(df, columns):  # [6]
        return df.drop_duplicates(subset=columns)

    @staticmethod
    def sort_columns(df, cols):  # [7]
        return df.sort_values(cols)

    @staticmethod
    def to_datetimeindex(data):
        df = Utility.to_dataframe(data)
        df["Date"] = pd.to_datetime(df["Date"])  # [8]
        df = df.set_index("Date")  # [9]
        return df
