from typing import Any, Mapping, Sequence


class SeveralUtils:
    @staticmethod
    def set_objet_properties(
        obj: Any, mapper: Mapping[str, Any], case_sensitive: bool = False
    ) -> None:
        props: Sequence[str] = [
            prop
            for prop in dir(obj)
            if not prop.startswith("_") and not prop.endswith("_")
        ]

        for prop in props:
            for mapper_prop, mapper_value in mapper.items():
                if case_sensitive:
                    prop = prop.upper()
                    mapper_prop = mapper_prop.upper()

                if mapper_prop == prop:
                    setattr(obj, mapper_prop, mapper_value)
