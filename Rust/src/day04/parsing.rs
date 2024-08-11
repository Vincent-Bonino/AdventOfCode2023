use nom::branch::alt;
use nom::bytes::complete::tag;
use nom::character::complete::{digit1, space1};
use nom::multi::separated_list1;
use nom::sequence::tuple;
use nom::IResult;

use crate::day04::models::Scratchcard;

// Example:
// Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
pub fn parse_input_line(input: &str) -> Scratchcard {
    let (input, (_, _, card_id, _, _)) = parse_header(input).unwrap();
    let (_, (winning_numbers, _, numbers)) = parse_card(input).unwrap();

    Scratchcard {
        card_id: u32::from_str_radix(card_id, 10).unwrap(),
        winning_numbers: winning_numbers.iter().map(|val| u32::from_str_radix(val, 10).unwrap()).collect(),
        numbers: numbers.iter().map(|val| u32::from_str_radix(val, 10).unwrap()).collect(),
    }
}


fn parse_header(input: &str) -> IResult<&str, (&str, &str, &str, &str, &str)> {
    tuple(
        (tag("Card"), space1, digit1, tag(":"), space1)
    )(input)
}

fn parse_card(input: &str) -> IResult<&str, (Vec<&str>, &str, Vec<&str>)> {
    let input = input.trim();
    tuple(
        (parse_numbers, tag(" | "), parse_numbers)
    )(input)
}

fn parse_numbers(input: &str) -> IResult<&str, Vec<&str>> {
    separated_list1(
        space1,  // Separator
        digit1
    )(input.trim())
}
