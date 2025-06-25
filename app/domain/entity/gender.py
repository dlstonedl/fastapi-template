from enum import Enum, verify, UNIQUE

@verify(UNIQUE)
class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
