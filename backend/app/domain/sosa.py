import math


def generation_from_sosa(sosa: int) -> int:
    return int(math.log2(sosa)) + 1


def validate_sex_vs_sosa(sex: str, sosa: int) -> bool:
    if sosa == 1:
        return True
    if sex == "M" and sosa % 2 != 0:
        return False
    if sex == "F" and sosa % 2 != 1:
        return False
    return True
