def time_to_milliseconds(time_str):
    # Convert time string to milliseconds
    milliseconds = (
        int(time_str[:2]) * 3600 * 1000
        + int(time_str[2:4]) * 60 * 1000
        + int(time_str[4:6]) * 1000
        + int(time_str[6:])
    )
    return milliseconds
