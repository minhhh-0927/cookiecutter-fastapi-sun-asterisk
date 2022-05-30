def get_has_more(limit: int,
                 offset: int,
                 total_count: int) -> bool:
    if not limit or not offset:
        return False
    if limit + offset > total_count:
        return False
    return True
