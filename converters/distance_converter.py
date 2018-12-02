def convert(distance):
    try:
        return int(distance)
    except ValueError:
        return int(distance * 1000)

