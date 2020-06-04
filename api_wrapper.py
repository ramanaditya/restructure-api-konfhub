import requests
import json


class APIWrapper:
    def __init__(self) -> None:
        self.URL = "https://o136z8hk40.execute-api.us-east-1.amazonaws.com/dev/get-list-of-conferences"

    def fetch_api(self) -> dict:
        """
        Fetching API using GET method
        :return: dict
        """
        api = requests.get(self.URL)
        headers = api.headers
        if api.status_code == 200:
            text = api.text

            # Loading as JSON
            api = json.loads(text)
            print(len(api["free"]), len(api["paid"]))
            return api
        else:
            return {}

    def date_suffix(self, date) -> str:
        """Adding suffix to the date"""
        formatted_date = str(date)
        if date % 10 == 1:
            formatted_date += "st"
        elif date % 10 == 2:
            formatted_date += "nd"
        elif date % 10 == 3:
            formatted_date += "rd"
        else:
            formatted_date += "th"
        return formatted_date

    def format_date(self, data) -> dict:
        """
        Converting date to human readable format
        Also added sortDateValue key for sorting the data
        """
        month_dict = {
            "jan": "January",
            "feb": "February",
            "mar": "March",
            "apr": "April",
            "may": "May",
            "jun": "June",
            "jul": "July",
            "aug": "August",
            "sep": "September",
            "oct": "October",
            "nov": "November",
            "dec": "December",
        }
        month_num_dict = {
            "jan": "01",
            "feb": "02",
            "mar": "03",
            "apr": "04",
            "may": "05",
            "jun": "06",
            "jul": "07",
            "aug": "08",
            "sep": "09",
            "oct": "10",
            "nov": "11",
            "dec": "12",
        }
        for i in range(len(data["free"])):
            start_date = data["free"][i].get("confStartDate", -1)
            end_date = data["free"][i].get("confEndDate", -1)
            data["free"][i]["sortDateValue"] = int(
                start_date[-4:]
                + month_num_dict.get(start_date[3:6].lower(), 0)
                + start_date[:2]
            )
            if start_date != -1:
                date = int(end_date[:2])
                month = end_date[3:6]
                year = end_date[-4:]
                formatted_date = self.date_suffix(date)
                formatted_month = month_dict.get(
                    month.lower(), month.lower().capitalize()
                )
                data["free"][i]["confStartDate"] = (
                    formatted_month + " " + formatted_date + ", " + year
                )
            if end_date != -1:
                date = int(end_date[:2])
                month = end_date[3:6]
                year = end_date[-4:]
                formatted_date = self.date_suffix(date)
                formatted_month = month_dict.get(
                    month.lower(), month.lower().capitalize()
                )
                data["free"][i]["confEndDate"] = (
                    formatted_month + " " + formatted_date + ", " + year
                )
            else:
                pass

        for i in range(len(data["paid"])):
            start_date = data["paid"][i].get("confStartDate", -1)
            end_date = data["paid"][i].get("confEndDate", -1)
            data["paid"][i]["sortDateValue"] = int(
                start_date[-4:]
                + month_num_dict.get(start_date[3:6].lower(), 0)
                + start_date[:2]
            )
            if start_date != -1:
                date = int(end_date[:2])
                month = end_date[3:6]
                year = end_date[-4:]
                formatted_date = self.date_suffix(date)
                formatted_month = month_dict.get(
                    month.lower(), month.lower().capitalize()
                )
                data["paid"][i]["confStartDate"] = (
                    formatted_month + " " + formatted_date + ", " + year
                )
            if end_date != -1:
                date = int(end_date[:2])
                month = end_date[3:6]
                year = end_date[-4:]
                formatted_date = self.date_suffix(date)
                formatted_month = month_dict.get(
                    month.lower(), month.lower().capitalize()
                )
                data["paid"][i]["confEndDate"] = (
                    formatted_month + " " + formatted_date + ", " + year
                )
            else:
                pass
        return data

    def merge_paid_n_free(self, data) -> list:
        """
        The events should be displayed on the basis of their startDate and not on the basis of entryType
        """
        del data["display_paid"]
        del data["display_free"]
        events = data["free"]
        events.extend(data["paid"])
        return events

    def remove_duplicates(self, data) -> list:
        """
        Removed similar duplicates
        :param data:
        :return list:
        """
        removed_dup = {frozenset(event.items()): event for event in data}.values()
        return removed_dup

    def removed_semantic(self, data) -> list:
        """
        Two events can be said same if
            - They occur on the same day and
            - Their location remains same
        :param data:
        :return:
        """
        pass

    def sort_data(self, data) -> list:
        """
        Sorting data based on their start Time
        key: sortDateValue
        :return list:
        """
        events = sorted(data, key=lambda i: i["sortDateValue"], reverse=True)
        return events

    def print_data(self, data):
        pass


if __name__ == "__main__":
    api = APIWrapper()
    fetched_data = api.fetch_api()
    formatted_date = api.format_date(fetched_data)
    merged_data = api.merge_paid_n_free(formatted_date)
    removed_duplicates = api.remove_duplicates(merged_data)
    sorted_data = api.sort_data(removed_duplicates)
