mod logic;

use crate::aoc::Aoc23Solution;

use logic::solve_day01_part1;
use crate::day01::logic::solve_day01_part2;

#[derive(Default)]
pub struct Day01 {
    parsed_data: String,
}

impl Aoc23Solution for Day01 {
    fn get_day_number(self: &Self) -> usize { 1 }
    fn parse_input_file(&mut self, data: String) {
        self.parsed_data = data;
    }

    fn solve_part_one(&mut self) -> i128 {
        solve_day01_part1(&self.parsed_data)
    }

    fn solve_part_two(&mut self) -> i128 {
        solve_day01_part2(&self.parsed_data)
    }
}
