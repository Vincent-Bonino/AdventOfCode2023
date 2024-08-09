/// Define a trait shared by all solutions
pub trait Aoc23Solution {
    fn get_day_number(self: &Self) -> usize;
    fn parse_input_file(self: &mut Self, data: String);
    fn solve_part_one(self: &mut Self) -> i128 { 0 }
    fn solve_part_two(self: &mut Self) -> i128 { 0 }
}

/// Build path to the input file
pub fn get_input_path(day_nbr: usize) -> String {
    format!("input/day{day_nbr:0>2}.txt")
}

/// Build path to the example file
pub fn get_example_path(day_nbr: usize) -> String {
    format!("examples/day{day_nbr:0>2}.txt")
}
