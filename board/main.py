from prices_printer import prices_view as pr_view
import ujson
import os


def save_price_data(data):
    try:
        os.stat("data")
    except OSError:
        os.mkdir("data")

    raw = {
        "title": data.title,
        "price": data.price,
        "discount": None
    }

    if data.discount is not None:
        raw["discount"] = {
            "old_price": data.discount.old_price,
            "percent": data.discount.percent
        }

    with open("data/prices.json", "w") as f:
        ujson.dump(raw, f)


def load_price_data():
    path = "data/prices.json"

    try:
        os.stat(path)
    except OSError:
        return None

    with open(path, "r") as f:
        raw = ujson.load(f)

    discount = None
    if "discount" in raw and raw["discount"] is not None:
        d = raw["discount"]
        discount = pr_view.DiscountData(d["old_price"], d["percent"])

    return pr_view.PriceData(
        raw["title"],
        raw["price"],
        discount
    )


def main():
    data = load_price_data()
    if data is not None:
        pr_view.write_price_data(data)

if __name__ == "__main__":
    main()