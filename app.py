from flask import Flask
from api_wrapper import *
from flask import render_template

app = Flask(__name__)


@app.route("/")
def home():
    api = APIWrapper()
    fetched_data = api.fetch_api()
    formatted_date = api.format_date(fetched_data)
    merged_data = api.merge_paid_n_free(formatted_date)
    removed_duplicates = api.remove_duplicates(merged_data)
    sorted_data = api.sort_data(removed_duplicates)

    return render_template("index.html", context={"events": sorted_data})


if __name__ == "__main__":
    app.run(debug=True)
