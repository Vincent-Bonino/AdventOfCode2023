mod logic;
mod models;
mod parsing;

use std::collections::HashMap;

use crate::aoc::Aoc23Solution;
use crate::day20::logic::{solve_day20_part1, solve_day20_part2};
use crate::day20::models::Module;
use crate::day20::parsing::parse_file;

#[derive(Default)]
pub struct Day20 {
    parsed_data: Vec<Box<dyn Module>>,
}

impl Aoc23Solution for Day20 {
    fn get_day_number(self: &Self) -> usize { 20 }

    fn parse_input_file(&mut self, data: String) {
        self.parsed_data = parse_file(&data)
    }

    fn solve_part_one(&mut self) -> i128 {
        solve_day20_part1(&mut self.parsed_data) as i128
    }

    fn solve_part_two(self: &mut Self) -> i128 {
        solve_day20_part2(&mut self.parsed_data) as i128
    }
}
