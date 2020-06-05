import json

import requests
import spacy


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
            return api
        else:
            return {}

    def date_suffix(self, date) -> str:
        """Adding suffix to the date"""
        formatted_date = str(date)
        if date == 1 or date == 21 or date == 31:
            formatted_date += "st"
        elif date == 2 or date == 22:
            formatted_date += "nd"
        elif date == 3 or date == 23:
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

        # Formatting for free events
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

        # Formatting for paid events
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

        # Cleaning Data
        del data["display_paid"]
        del data["display_free"]

        # Storing the list of dictionaries
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

    def identify_duplicates(self, data) -> list:
        """
        To list out the duplicate values present in the list
        :param data: 
        :return: 
        """
        dup = []
        for i in range(len(data) - 1):
            if data[i] in data[i + 1 :]:
                dup.append(data[i])
            else:
                pass
        return dup

    def sort_data(self, data) -> list:
        """
        Sorting data based on their start Time
        key: sortDateValue
        :return list:
        """
        events = sorted(data, key=lambda i: i["sortDateValue"], reverse=True)
        return events

    def task1(self, data) -> list:
        """
        To print the data in human readable format in txt file
        :param data: 
        :return:
        :File Saved: human_readable.txt
        """
        f = open("human_readable.txt", "w")
        human_readable = []
        for event in data:
            temp = []
            temp.append(event["confName"].strip())
            temp.append(event["confStartDate"].strip())
            temp.append(event["city"].strip())
            temp.append(event["state"].strip())
            temp.append(event["country"].strip())
            temp.append(event["entryType"].strip())
            temp.append(event["confUrl"].strip())
            f.write(", ".join(temp))
            f.write("\n")
            human_readable.append(temp)
        f.close()
        return human_readable

    def task2(self, data) -> list:
        """
        To print the duplicates from the list and saving it in txt file
        :param data:
        :return:
        :File Saved: exact_duplicates.txt
        """
        f = open("exact_duplicates.txt", "w")
        removed_dup = []
        for i in range(len(data) - 1):
            if data[i] in data[i + 1 :]:
                f.write(", ".join(data[i]))
                f.write("\n")
                removed_dup.append(data[i])
            else:
                pass
        f.close()

        return removed_dup

    def task3(self, data) -> None:
        """
        To identify semantic duplicates from the list
        :param data:
        :return:
        :File Saved: semantic_duplicates.txt
        """

        # Loading the model,is downloaded with the requirements.txt
        nlp = spacy.load("en_core_web_md")
        f = open("semantic_duplicates.txt", "w")

        # track is used to reduce duplicate entries
        track = []
        for i in range(len(data) - 1):
            first_event = nlp(data[i][0])
            temp = []
            for j in range(i + 1, len(data)):
                second_event = nlp(data[j][0])

                # Comparing the strings
                rank = first_event.similarity(second_event)
                if rank > 0.95:
                    temp.append(data[j])

            # Writing to the file only if they are found similar
            if len(temp) > 0:
                if data[i] not in track:
                    track.append(data[i])
                    f.write(", ".join(data[i]))
                    f.write("\n")
                    for event in temp:
                        if event not in track:
                            track.append(event)
                            f.write(", ".join(event))
                            f.write("\n")
                        else:
                            pass
                    f.write("\n")
                else:
                    pass
        f.close()
        return


if __name__ == "__main__":
    api = APIWrapper()
    fetched_data = api.fetch_api()
    formatted_date = api.format_date(fetched_data)
    merged_data = api.merge_paid_n_free(formatted_date)
    removed_duplicates = api.remove_duplicates(merged_data)
    sorted_data = api.sort_data(removed_duplicates)

    task1 = api.task1(merged_data)
    task2 = api.task2(task1)

    # Delete duplicates
    for i in range(len(task2)):
        task1.remove(task2[i])

    api.task3(task1)
