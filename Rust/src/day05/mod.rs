mod logic;
mod models;
mod parsing;
mod test;

use crate::aoc::Aoc23Solution;

use crate::day05::models::Almanac;
use crate::day05::parsing::parse_file;
use logic::{solve_day05_part1};
use crate::day05::logic::solve_day05_part2;

#[derive(Default)]
pub struct Day05 {
    parsed_data: Almanac,
}

impl Aoc23Solution for Day05 {
    fn get_day_number(self: &Self) -> usize { 5 }

    fn parse_input_file(&mut self, data: String) {
        self.parsed_data = parse_file(&data);
    }
    fn solve_part_one(&mut self) -> i128 {
        solve_day05_part1(&self.parsed_data)
    }
    fn solve_part_two(&mut self) -> i128 {
        solve_day05_part2(&self.parsed_data)
    }
}
