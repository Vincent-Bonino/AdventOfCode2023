import re


def part_one() -> int:
    total_sum: int = 0

    with open("input.txt", mode='r') as f_input:
        for line in f_input.readlines():
            # Remove all none-digit characters
            s_value: str = re.sub(r'[^0-9]+', "", line).strip()
            # Looking for 2-digit long integer so keeping only first and last ones
            s_value = f"{s_value[0]}{s_value[-1]}"
            # Make it an int
            i_value: int = int(s_value)
            total_sum += i_value

    return total_sum


def part_two() -> int:
    total_sum: int = 0

    with open("input.txt", mode='r') as f_input:
        for line in f_input.readlines():
            # The trick here is letter-written digits sharing a letter.
            # I basically wrote them all
            # And I assume it won't happen with 3 digits...
            s_value: str = (
                line.strip()
                .replace("oneight", "18")
                .replace("twone", "21")
                .replace("threeight", "38")
                .replace("fiveight", "58")
                .replace("sevenine", "79")
                .replace("eightwo", "82")
                .replace("eighthree", "82")
                .replace("nineight", "98")
                .replace("one", "1")
                .replace("two", "2")
                .replace("three", "3")
                .replace("four", "4")
                .replace("five", "5")
                .replace("six", "6")
                .replace("seven", "7")
                .replace("eight", "8")
                .replace("nine", "9")
            )

            s_value = re.sub(r'[^0-9]+', "", s_value)
            s_value = f"{s_value[0]}{s_value[-1]}"

            i_value: int = int(s_value)
            total_sum += i_value
    return total_sum

print(part_one())
print(part_two())
