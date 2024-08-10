use crate::day02::models::{Bag, Game};

pub fn solve_day02_part1(data: &Vec<Game>) -> i128 {
    // only 12 red cubes, 13 green cubes, and 14 blue cubes
    let maximum_bag: Bag = Bag::new(12, 13, 14);

    let result: u32 = data.iter()
        .filter(|game| { game.is_valid(&maximum_bag) })
        .map(|game| { game.id })
        .sum();
    result as i128
}

pub fn solve_day02_part2(data: &Vec<Game>) -> i128 {
    let result: u32 = data.iter()
        .map(|game| { game.hypothetical_min_bag().power() })
        .sum();
    result as i128
}
