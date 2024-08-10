use std::collections::HashSet;
use crate::common::coordinates::XYCoordinates;
use crate::day03::models::Schematic;

pub fn solve_day03_part1(schematic: &Schematic) -> i128 {
    let mut result: Vec<u32> = Vec::new();

    // Loop on numbers first (and continue this loop to prevent counting them twice
    'num_loop: for number in schematic.numbers.iter() {
        let num_tiles: Vec<XYCoordinates> = number.get_tiles();

        for symbol in schematic.symbols.iter() {
            let symbol_tiles: Vec<XYCoordinates> = symbol.get_position().get_neighbours8();

            for tile in num_tiles.iter() {
                if symbol_tiles.contains(&tile) {
                    result.push(number.value);
                    continue 'num_loop;  // Just count this number, to the next one
                }
            }
        }
    };

    let total: u32 = result.iter().sum();
    total as i128
}

pub fn solve_day03_part2(schematic: &Schematic) -> i128 {
    let gear_symbol: char = '*';
    let mut total: i128 = 0;

    'sym_loop: for symbol in schematic.symbols.iter() {
        if symbol.value != gear_symbol { continue };

        let mut gear_counter: usize = 0;
        let mut gear_total: i128 = 1;
        let symbol_tiles: Vec<XYCoordinates> = symbol.get_position().get_neighbours8();

        'num_loop: for number in schematic.numbers.iter() {
            let num_tiles: Vec<XYCoordinates> = number.get_tiles();

            for tile in num_tiles.iter() {
                if symbol_tiles.contains(&tile) {
                    gear_counter += 1;
                    if gear_counter > 2 { continue 'sym_loop }

                    gear_total *= number.value as i128;
                    continue 'num_loop;  // Do not count a number more than once
                }
            }
        }
        if gear_counter == 2 { total += gear_total }
    }

    total
}
