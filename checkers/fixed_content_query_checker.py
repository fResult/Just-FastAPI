class FixedContentQueryChecker:
    def __init__(self, fixed_content: str) -> None:
        self.fixed_content = fixed_content

    def __call__(self, q: str = "") -> bool:
        if q:
            return q in self.fixed_content.lower()

        return False

