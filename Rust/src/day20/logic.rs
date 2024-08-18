///! Could be optimized and factored a bit

use std::cell::RefCell;
use std::collections::{HashMap, VecDeque};
use std::fs::File;
use std::io::Read;

use clap::builder::Str;
use num::FromPrimitive;
use num::integer::lcm;
use petgraph::dot::{Dot, Config};
use petgraph::Graph;
use petgraph::graph::NodeIndex;

use crate::day20::models::{EmittedSignal, Module, Pulse};

static MANUAL_INPUT: &str = "_start";

pub fn solve_day20_part1(data: &mut Vec<Box<dyn Module>>) -> u64 {
    let mut data: Vec<Box<dyn Module>> = data.clone();  // Modules will be changed, to not interfere

    let mut low_pulse_counter: u64 = 0;
    let mut high_pulse_counter: u64 = 0;
    let mut signal_queue: VecDeque<EmittedSignal> = VecDeque::new();

    let mut indexed_data: HashMap<String, usize> = HashMap::new();
    for (index, module) in data.iter().enumerate() {
        indexed_data.insert(module.get_name(), index);
    }

    for _ in 0..1000 {

        // Manual input
        signal_queue.push_back(
            EmittedSignal::new(MANUAL_INPUT, "broadcaster", Pulse::Low)
        );

        while !signal_queue.is_empty() {
            let signal: EmittedSignal = signal_queue.pop_front().unwrap();

            // First, count pulses
            match signal.pulse {
                Pulse::Low => low_pulse_counter += 1,
                Pulse::High => high_pulse_counter += 1,
            };

            // Then apply it and retrieve signals sent in consequence
            let dst_module_index: usize = match indexed_data.get(&signal.dst_module) {
                None => continue,  // Module with no behaviour
                Some(x) => *x,
            };

            let dst_module: &mut Box<dyn Module> = data.get_mut(dst_module_index).unwrap();
            let emitted_signals: Vec<EmittedSignal> = dst_module.process_and_emit(signal);

            for emitted_signal in emitted_signals {
                signal_queue.push_back(emitted_signal);
            }
        }
    }

    low_pulse_counter * high_pulse_counter
}


fn count_for_conjunctions(data: &mut Vec<Box<dyn Module>>, conjunctions: Vec<String>) -> Vec<u64> {
    let mut data: Vec<Box<dyn Module>> = data.clone();  // Modules will be changed, to not interfere

    let mut result: Vec<u64> = Vec::new();
    let mut signal_queue: VecDeque<EmittedSignal> = VecDeque::new();

    let mut indexed_data: HashMap<String, usize> = HashMap::new();
    for (index, module) in data.iter().enumerate() {
        indexed_data.insert(module.get_name(), index);
    }

    for press_count in 1..5000 {  // Hypothesis: will happen in the 5000 first presses

        // Manual input
        signal_queue.push_back(
            EmittedSignal::new(MANUAL_INPUT, "broadcaster", Pulse::Low)
        );

        while !signal_queue.is_empty() {
            let signal: EmittedSignal = signal_queue.pop_front().unwrap();

            if conjunctions.contains(&signal.src_module) && signal.pulse == Pulse::High {
                println!("[{}] {}", press_count, signal);
                result.push(press_count)
            }

            // Then apply it and retrieve signals sent in consequence
            let dst_module_index: usize = match indexed_data.get(&signal.dst_module) {
                None => continue,  // Module with no behaviour
                Some(x) => *x,
            };

            let dst_module: &mut Box<dyn Module> = data.get_mut(dst_module_index).unwrap();
            let emitted_signals: Vec<EmittedSignal> = dst_module.process_and_emit(signal);

            for emitted_signal in emitted_signals {
                signal_queue.push_back(emitted_signal);
            }
        }
    }

    result
}


pub fn solve_day20_part2(data: &mut Vec<Box<dyn Module>>) -> u64 {
    // Visualizing a graph representation of the modules links shows 4 distinct parts,
    // each one being linked to "rx" by a conjunction module "zh".
    // This transform the problem into:
    // > How many pressed to have all these 4 parts send a H to "zh" at the same time ?
    // Which is simpler: it is the least common multiple of the four !

    // Identify the four: (done on graph) "bh", "dl", "ns" and "vd"
    let switching_modules: Vec<String> = vec![
        String::from("bh"),
        String::from("dl"),
        String::from("ns"),
        String::from("vd"),
    ];
    let high_conjunction_indexes: Vec<u64> = count_for_conjunctions(data, switching_modules);

    // Return their LCM
    let result: u64 = high_conjunction_indexes.into_iter()
        .reduce(|acc: u64, elem: u64| {
            lcm::<u64>(
                FromPrimitive::from_u64(acc).unwrap(),
                FromPrimitive::from_u64(elem).unwrap(),
            )
        })
        .unwrap();

    result
}
