use std::fs;
use clap::Parser;

use aoc2023::aoc::{get_example_path, get_input_path, Aoc23Solution};
use aoc2023::day01::Day01;
use aoc2023::day02::Day02;
use aoc2023::day03::Day03;
use aoc2023::day04::Day04;
use aoc2023::day05::Day05;
use aoc2023::day20::Day20;

use aoc2023::cli::Args;

// use aoc2023::tests::test;

fn main() {
    println!("AoC 2023 !");
    let args: Args = Args::parse();
    // println!("Args: {args:?}");

    // Build array of solvers
    let mut solvers: Vec<Box<dyn Aoc23Solution>> = vec![
        Box::new(Day01::default()),
        Box::new(Day02::default()),
        Box::new(Day03::default()),
        Box::new(Day04::default()),
        Box::new(Day05::default()),
        Box::new(Day20::default()),
    ];

    // Solve each day
    for solver in solvers.iter_mut() {
        let day_number: usize = solver.get_day_number();
        if args.day == 0 || args.day == day_number {
            run_solver(day_number, solver, args.use_tests);
        };
    }
}

fn run_solver(day_number: usize, solver: &mut Box<dyn Aoc23Solution>, is_test: bool) {

    let input_path: String = match is_test {
        false => get_input_path(day_number),
        true  => get_example_path(day_number),
    };
    solver.parse_input_file(
        fs::read_to_string(input_path).expect("File error")
    );

    let sol1: i128 = solver.solve_part_one();
    let sol2: i128 = solver.solve_part_two();

    if sol2 == 0 {
        println!("Day {day_number} - part 1: {sol1}");
    } else {
        println!("Day {day_number} - part 1: {sol1} / part 2: {sol2}");
    }
}
