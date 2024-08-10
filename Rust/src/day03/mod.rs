mod logic;
mod models;
mod parsing;

use crate::aoc::Aoc23Solution;
use crate::day03::models::Schematic;
use crate::day03::parsing::parse_lines;
use logic::{solve_day03_part1,solve_day03_part2};

#[derive(Default)]
pub struct Day03 {
    parsed_data: Schematic,
}

impl Aoc23Solution for Day03 {
    fn get_day_number(self: &Self) -> usize { 3 }

    fn parse_input_file(&mut self, data: String) {
        self.parsed_data = parse_lines(&data)
    }
    fn solve_part_one(&mut self) -> i128 {
        solve_day03_part1(&self.parsed_data)
    }
    fn solve_part_two(&mut self) -> i128 {
        solve_day03_part2(&self.parsed_data)
    }
}
