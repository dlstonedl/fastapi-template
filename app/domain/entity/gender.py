from enum import Enum, verify, UNIQUE

@verify(UNIQUE)
class Gender(Enum):
    MALE = (1, "男性")
    FEMALE = (2, "女性")

    def __init__(self, code, description):
        self.code = code
        self.description = description

if __name__ == "__main__":
    print(Gender.MALE.name, " ", Gender.MALE.value, " ",Gender.MALE.code, " ", Gender.MALE.description)