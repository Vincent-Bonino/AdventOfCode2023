use regex::Regex;
use crate::day03::models::{Schematic,SchematicNumber,SchematicSymbol};

pub fn parse_lines(input: &str) -> Schematic {
    let sch_number: Regex = Regex::new(r"[0-9]+").unwrap();
    let sch_symbol: Regex = Regex::new(r"[^0-9.]").unwrap();

    let mut numbers: Vec<SchematicNumber> = Vec::new();
    let mut symbols: Vec<SchematicSymbol> = Vec::new();

    for (index, line) in input.lines().enumerate() {
        // Numbers
        for match_obj in sch_number.find_iter(line) {
            numbers.push(
                SchematicNumber {
                    line: index as u32,
                    col: match_obj.start() as u32,
                    len: match_obj.len() as u32,
                    value: u32::from_str_radix(match_obj.as_str(), 10).unwrap()
                }
            );
        }
        // Symbols
        for match_obj in sch_symbol.find_iter(line) {
            symbols.push(
                SchematicSymbol {
                    line: index as u32,
                    col: match_obj.start() as u32,
                    value: match_obj.as_str().chars().next().unwrap(),
                }
            )
        }
    };
    Schematic {
        numbers,
        symbols,
    }
}
