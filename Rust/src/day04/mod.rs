mod logic;
mod models;
mod parsing;

use crate::aoc::Aoc23Solution;

use logic::{solve_day04_part1,solve_day04_part2};
use models::Scratchcard;
use parsing::parse_input_line;


#[derive(Default)]
pub struct Day04 {
    parsed_data: Vec<Scratchcard>,
}

impl Aoc23Solution for Day04 {
    fn get_day_number(self: &Self) -> usize { 4 }

    fn parse_input_file(&mut self, data: String) {
        self.parsed_data = data.lines().map(|line| parse_input_line(line)).collect();
    }

    fn solve_part_one(&mut self) -> i128 {
        solve_day04_part1(&self.parsed_data)
    }

    fn solve_part_two(&mut self) -> i128 {
        solve_day04_part2(&self.parsed_data)
    }
}
