use nom::branch::alt;
use nom::bytes::complete::{is_not, tag};
use nom::character::complete::{alpha1, anychar, digit1, space1, i64 as i64_parser};
use nom::combinator::map_res;
use nom::multi::separated_list1;
use nom::sequence::{delimited, tuple};
use nom::IResult;

use crate::day05::models::{Almanac, Mapping, MappingSet};

pub fn parse_file(content: &str) -> Almanac {
    let mut seeds: Vec<i64> = Vec::new();
    let mut mapping_sets: Vec<MappingSet> = Vec::new();

    let mut current_name: &str = "";
    let mut current_mappings: Vec<Mapping> = Vec::new();

    for (index, line) in content.lines().enumerate() {
        // First line is special
        if index == 0 {
            let (_, (_, parsed_seeds)) = parse_seeds(line).unwrap();
            seeds = parsed_seeds;
            continue
        }
        // Second line is empty
        if index == 1 { continue }

        // --- Parse a MappingSet ---

        // Empty lines mark the end of a MappingSet
        if line.len() == 0 {
            mapping_sets.push(
                MappingSet {
                    name: String::from(current_name),
                    mappings: current_mappings.clone(),
                }
            );
            current_mappings.clear();
            current_name = ""
        }
        // This line is the name
        else if current_name == "" {
            let (_, (name, _)) = parse_category(line).unwrap();
            current_name = name;
        }
        // This line is a mapping
        else {
            let (_, (dst, _, src, _, len)) = parse_mapping(line).unwrap();
            current_mappings.push(
                Mapping::new(dst, src, len)
            )
        }
    }

    if !current_mappings.is_empty() {
        mapping_sets.push(
            MappingSet {
                name: String::from(current_name),
                mappings: current_mappings.clone(),
            }
        );
    }

    Almanac::new(seeds, mapping_sets)
}

fn parse_seeds(line: &str) -> IResult<&str, (&str, Vec<i64>)> {
    tuple(
        (tag("seeds: "), separated_list1(space1, i64_parser))
    )(line)
}

fn parse_category(line: &str) -> IResult<&str, (&str, &str)> {
    tuple(
        (is_not(" "), tag(" map:"))
    )(line)
}

fn parse_mapping(line: &str) -> IResult<&str, (i64, &str, i64, &str, i64)> {
    tuple(
        (i64_parser, space1, i64_parser, space1, i64_parser)
    )(line)
}
