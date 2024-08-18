use std::collections::HashMap;
use nom::branch::alt;
use nom::bytes::complete::tag;
use nom::character::complete::alpha1;
use nom::combinator::opt;
use nom::IResult;
use nom::multi::separated_list1;
use nom::sequence::tuple;

use crate::day20::models::{Broadcaster, Conjunction, FlipFlop, Module};

pub fn parse_file(data: &str) -> Vec<Box<dyn Module>> {
    let mut result: Vec<Box<dyn Module>> = Vec::new();

    // Module: [input_module, ...]
    let mut backward_connections_mapping: HashMap<String, Vec<String>> = HashMap::new();

    for line in data.lines() {
        let (_, (mod_type, mod_name, _, mod_con)) = parse_line(line).unwrap();

        let name: String = mod_name.to_string();
        let forward_connections: Vec<String> = mod_con.iter().map(|val| val.to_string()).collect();

        result.push(
                match mod_type {
                None => Box::new(Broadcaster::new(name, forward_connections)),
                Some("%") => Box::new(FlipFlop::new(name, forward_connections)),
                Some("&") => Box::new(Conjunction::new(name, forward_connections)),
                _ => unreachable!()
            }
        );

        // Add it to mapping
        let fwd_connections: Vec<String> = mod_con.iter().map(|val| val.to_string()).collect();

        for fwd_con in fwd_connections {
            let input_vec: Option<&mut Vec<String>> = backward_connections_mapping.get_mut(&fwd_con);
            if let None = input_vec {
                backward_connections_mapping.insert(fwd_con, vec![mod_name.to_string()]);
            } else {
                input_vec.unwrap().push(mod_name.to_string());
            }
        }
    }

    // Compute input modules (for conjunction modules)
    for module in result.iter_mut() {
        module.set_input_modules(backward_connections_mapping.get(&module.get_name()));
    }

    result
}


fn parse_line(line: &str) -> IResult<&str, (Option<&str>, &str, &str, Vec<&str>)> {
    tuple(
        (parse_module_type, parse_module_name, parse_separator, parse_module_connections)
    )(line)
}

fn parse_module_type(input: &str) -> IResult<&str, Option<&str>> {
    opt(
        alt((tag("%"), tag("&")))
    )(input)
}

fn parse_module_name(input: &str) -> IResult<&str, &str> {
    alpha1(input)
}

fn parse_separator(input: &str) -> IResult<&str, &str> {
    tag(" -> ")(input)
}

fn parse_module_connections(input: &str) -> IResult<&str, Vec<&str>> {
    separated_list1(
        tag(", "),
        alpha1
    )(input)
}
