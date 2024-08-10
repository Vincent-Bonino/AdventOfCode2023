mod logic;
mod models;
mod parsing;

use crate::aoc::Aoc23Solution;

use logic::{solve_day02_part1,solve_day02_part2};
use models::Game;
use parsing::parse_input_line;

#[derive(Default)]
pub struct Day02 {
    parsed_data: Vec<Game>,
}

impl Aoc23Solution for Day02 {
    fn get_day_number(self: &Self) -> usize { 2 }

    fn parse_input_file(&mut self, data: String) {
        self.parsed_data = data.lines()
            .into_iter()
            .filter(|line| { line.len() != 0 })
            .map(|line| { parse_input_line(line) })
            .collect()
    }

    fn solve_part_one(&mut self) -> i128 {
        solve_day02_part1(&self.parsed_data)
    }

    fn solve_part_two(&mut self) -> i128 {
        solve_day02_part2(&self.parsed_data)
    }
}
