import sys

class Arguments:
    def __init__(self):
        self._parse_args()

    def _parse_args(self):
        args = sys.argv[1:]
        for arg in args:
            if arg.startswith("--"):
                key, eq, value = arg[2:].partition("=")
                if eq:  # has value (--key=value)
                    value = self._detect_type(value)
                else:   # flag only (--key)
                    value = True
                setattr(self, key, value)

    def _detect_type(self, value: str):
        """Try to cast value to int, float, bool, else str"""
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
        return value  # keep as string

    def get(self, key, default=None):
        """Getter method with default fallback"""
        return getattr(self, key, default)


# Example usage
if __name__ == "__main__":
    args = Arguments()
    print("Mode:", args.get("mode", "prod"))
    print("CSS:", args.get("css", False))
    print("DB:", args.get("db", True))
    print("Port:", args.get("port", 8080))
    print("Factor:", args.get("factor", 1.0))
    print("Debug:", args.get("debug", False))
