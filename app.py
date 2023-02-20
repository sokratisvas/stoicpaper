from flask import Flask, render_template
import requests
import json

app = Flask(__name__)
COUNTS = {"Marcus Aurelius": 0, "Seneca": 0, "Epictetus": 0, "Cato": 0, "Zeno": 0}


@app.route("/")
def index():
    return render_template("pick_philosopher.html")


@app.route("/philosophers/<philosopher>")
def get_philosopher_quote(philosopher):
    COUNTS[philosopher] += 1
    philosopher_tag = (
        "Marcus%20Aurelius" if philosopher == "Marcus Aurelius" else philosopher
    )
    philosopher_quotes_json = json.loads(
        requests.get(f"https://stoicquotesapi.com/v1/api/quotes/{philosopher_tag}").text
    )

    philosopher_quotes = [quote["body"] for quote in philosopher_quotes_json["data"]]
    last_page = philosopher_quotes_json["last_page"]
    total_quotes = philosopher_quotes_json["total"]
    for i in range(2, last_page + 1):
        philosopher_quotes_json = json.loads(
            requests.get(
                f"http://stoicquotesapi.com/v1/api/quotes/{philosopher}?page={i}"
            ).text
        )
        philosopher_quotes.extend(
            quote["body"] for quote in philosopher_quotes_json["data"]
        )

    quote = philosopher_quotes[COUNTS[philosopher] % total_quotes]

    return f"<h2>{philosopher}</h2><p>{quote}</p>"


if __name__ == "__main__":
    app.run()
