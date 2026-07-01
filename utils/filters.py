def sorted_options(dataframe, column):
    return sorted(dataframe[column].dropna().unique().tolist())


def normalize_date_range(selected_range, default_start, default_end):
    if not isinstance(selected_range, tuple):
        return default_start, default_end

    if len(selected_range) == 1:
        return selected_range[0], selected_range[0]

    if len(selected_range) >= 2:
        return selected_range[0], selected_range[1]

    return default_start, default_end
