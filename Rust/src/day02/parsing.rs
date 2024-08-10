use nom::branch::alt;
use nom::bytes::complete::tag;
use nom::character::complete::{digit1, space1};
use nom::multi::separated_list1;
use nom::sequence::tuple;
use nom::IResult;

use crate::day02::models::{Bag, Game};


// Example:
// Game 1: 2 red, 2 green; 1 red, 1 green, 2 blue; 3 blue, 3 red, 3 green; 1 blue, 3 green, 7 red; 5 red, 3 green, 1 blue

pub fn parse_input_line(input: &str) -> Game {
    let (input, (_, game_id, _)) = parse_header(input).unwrap();
    let (_, draws) = parse_draws(input).unwrap();

    let mut bags: Vec<Bag> = Vec::new();

    for draw in draws {
        for color in draw {
            let (quantity, _, color) = color;
            bags.push(build_bag(quantity, color));
        }
    }

    Game {
        id: u32::from_str_radix(game_id, 10).unwrap(),
        bags,
    }
}

fn parse_header(input: &str) -> IResult<&str, (&str, &str, &str)> {
    tuple(
        (tag("Game "), digit1, tag(": "))
    )(input)
}

fn parse_draws(input: &str) -> IResult<&str, Vec<Vec<(&str, &str, &str)>>> {
    separated_list1(
        tag("; "),  // Separator
        parse_draw,
    )(input)
}

fn parse_draw(input: &str) -> IResult<&str, Vec<(&str, &str, &str)>> {
    separated_list1(
        tag(", "),  // Separator
        parse_color,
    )(input)
}

fn parse_color(input: &str) -> IResult<&str, (&str, &str, &str)> {
    tuple(
        (digit1, space1, alt((tag("red"), tag("green"), tag("blue"))))
    )(input)
}

fn build_bag(quantity: &str, color: &str) -> Bag {
    let quantity: u32 = u32::from_str_radix(quantity, 10).expect("Bad quantity");
    match color {
        "red" => Bag::from_red(quantity),
        "green" => Bag::from_green(quantity),
        "blue" => Bag::from_blue(quantity),
        _ => unreachable!(),
    }
}
