from prices_printer import prices_view as pr_view
import ujson
import os


def save_price_data(data: pr_view.PriceData):
    try:
        os.stat("data")
    except OSError:
        os.mkdir("data")

    raw = {
        "name": data.name,
        "base_price": {
            "price": data.base_price.price,
            "kopecks": data.base_price.kopecks
        },
        "discount": None
    }

    if data.discount_data is not None:
        raw["discount"] = {
            "sale_price": {
                "price": data.discount_data.sale_price.price,
                "kopecks": data.discount_data.sale_price.kopecks
            },
            "discount": data.discount_data.discount
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

    base_price_raw = raw["base_price"]
    base_price = pr_view.PriceVal(
        base_price_raw["price"],
        base_price_raw["kopecks"]
    )

    discount_data = None
    if "discount" in raw and raw["discount"] is not None:
        try:
            d = raw["discount"]
            sp = d["sale_price"]
            sale_price = pr_view.PriceVal(
                sp["price"],
                sp["kopecks"]
            )
            discount_data = pr_view.DiscountData(
                sale_price,
                d["discount"]
            )
        except:
            return None

    return pr_view.PriceData(
        raw["name"],
        base_price,
        discount_data
    )


def main():
    data = load_price_data()
    if data is not None:
        pr_view.view_price_data(data)


if __name__ == "__main__":
    main()
