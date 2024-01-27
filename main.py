import json


INPUT_FILE = "Python-task.json"
OUTPUT_FILE = "Python-task-result.json"


def find_min_price_room_type_and_number_of_guests(
    current_hotel: dict, min_price: float
) -> tuple[float, str, int]:
    """Find the cheapest (lowest) shown price,
     room type and number of guests for this price."""

    current_number_of_guests = 0
    room_type_to_return = ""

    for current_room, shown_price in current_hotel["shown_price"].items():
        shown_price = float(shown_price)
        current_room_type = extract_room_type(current_room)

        if shown_price < min_price:
            min_price = shown_price
            current_number_of_guests = current_hotel["number_of_guests"]
            room_type_to_return = current_room_type

    return min_price, room_type_to_return, current_number_of_guests


def extract_room_type(current_room_type):
    """Extract room type from room name."""

    current_room_type = current_room_type[: current_room_type.find("-") - 1]

    return current_room_type


def count_total_price(current_hotel: dict) -> dict[str, float]:
    """Count total price for each room type."""

    current_hotel["hotel_name"] = dict()

    for current_room, net_price in current_hotel["net_price"].items():
        net_price = float(net_price)
        price_with_taxes = net_price + count_taxes(
            current_hotel["ext_data"]["taxes"]
        )
        current_room_type = extract_room_type(current_room)

        if current_room_type not in current_hotel["hotel_name"].keys():
            current_hotel["hotel_name"][current_room_type] = price_with_taxes
        else:
            current_hotel["hotel_name"][current_room_type] += price_with_taxes

    return current_hotel["hotel_name"]


def count_taxes(taxes_str: str) -> float:
    """Convert taxes from string to float and count sum of all taxes."""

    json_data = json.loads(taxes_str)
    taxes_float = 0.0

    for tax in json_data.values():
        taxes_float += float(tax)

    return taxes_float


def print_result_to_file(
    lowest_price: float,
    room_type: str,
    number_of_guests: int,
    total_price: dict[str, dict[str, float]],
):
    """Print all results to file."""

    result = {
        "the cheapest (lowest) shown price": lowest_price,
        "room_type": room_type,
        "number_of_guests": number_of_guests,
        "total price": total_price,
    }
    json_object = json.dumps(result, indent=4)

    with open(OUTPUT_FILE, "w") as output_file:
        output_file.write(json_object)


def main():
    with open(INPUT_FILE, "r") as input_file:
        data = json.load(input_file)
        hotels = data["assignment_results"]
        lowest_price = float("inf")
        total_prices = dict()

        for hotel in hotels:
            (
                lowest_price,
                room_type,
                number_of_guests,
            ) = find_min_price_room_type_and_number_of_guests(
                hotel, lowest_price
            )
            total_prices.update(count_total_price(hotel))

        print_result_to_file(
            lowest_price, room_type, number_of_guests, total_prices
        )


if __name__ == "__main__":
    main()
