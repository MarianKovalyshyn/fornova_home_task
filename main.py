import json


with open("Python-task.json", "r") as input_file:
    data = json.load(input_file)
    hotels = data["assignment_results"]
    min_price = float("inf")
    number_of_guests = 0
    room_type_to_return = ""
    total_prices = dict()

    for hotel in hotels:
        for room_type, shown_price in hotel["shown_price"].items():
            shown_price = float(shown_price)
            room_type = room_type[:room_type.find("-") - 1]

            if shown_price < min_price:
                min_price = shown_price
                number_of_guests = hotel["number_of_guests"]
                room_type_to_return = room_type

        total_prices[hotel["hotel_name"]] = dict()

        for room_type, net_price in hotel["net_price"].items():
            net_price = float(net_price)
            room_type = room_type[:room_type.find("-") - 1]

            if room_type not in total_prices[hotel["hotel_name"]].keys():
                total_prices[hotel["hotel_name"]][room_type] = net_price
            else:
                total_prices[hotel["hotel_name"]][room_type] += net_price

    result = {
        "the cheapest (lowest) shown price": min_price,
        "room_type": room_type_to_return,
        "number_of_guests": number_of_guests,
        "total price": total_prices
    }
    json_object = json.dumps(result, indent=4)

    with open("Python-task-result.json", "w") as output_file:
        output_file.write(json_object)
