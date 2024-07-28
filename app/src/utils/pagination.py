from fastapi import Query


class Paginator:
    def __init__(
        self,
        per_page: int = Query(default=50, alias='page[size]', ge=1, le=500),
            page: int = Query(default=1, alias='page[number]', ge=1),
    ):
        self.per_page = per_page
        self.page = page
