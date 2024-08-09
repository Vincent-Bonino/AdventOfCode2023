pub fn solve_day01_part1(input: &str) -> i128 {
    let mut total: i128 = 0;

    for line in input.lines() {
        if line.len() == 0 { continue }  // Ignore empty lines

        let mut first: Option<char> = None;
        let mut last: Option<char> = None;

        for character in line.chars() {
            if character.is_ascii_digit() {
                if first.is_none() {
                    first = Some(character);
                } else {
                    last = Some(character);
                }
            }
        }

        // In case of only one digit, it is considered as the first and last one
        if last.is_none() { last = first }

        let first_int_val: i128 = first.expect("First val empty").to_digit(10).unwrap() as i128;
        let last_int_val: i128 = last.expect("Last val empty").to_digit(10).unwrap() as i128;
        total += 10 * first_int_val + last_int_val;
    }
    total
}

pub fn solve_day01_part2(input: &str) -> i128 {
    let input: String = input
        .replace("zero", "zero0zero")
        .replace("one", "one1one")
        .replace("two", "two2two")
        .replace("three", "three3three")
        .replace("four", "four4four")
        .replace("five", "five5five")
        .replace("six", "six6six")
        .replace("seven", "seven7seven")
        .replace("eight", "eight8eight")
        .replace("nine", "nine9nine");

    solve_day01_part1(&input)
}
