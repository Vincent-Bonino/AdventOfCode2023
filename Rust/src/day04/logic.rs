use std::collections::HashMap;
use crate::day04::models::Scratchcard;

pub fn solve_day04_part1(data: &Vec<Scratchcard>) -> i128 {
    let result: u32 = data.iter().map(|card| card.get_points()).sum();
    result as i128
}

pub fn solve_day04_part2(data: &Vec<Scratchcard>) -> i128 {
    let mut card_counter: HashMap<u32, u32> = HashMap::new();

    for card in data.iter() {
        let index: u32 = card.card_id;

        let mult: u32 = match card_counter.get(&index) {
            None => 1,
            Some(v) => *v,
        };
        let match_number: u32 = card.get_matching_numbers();

        // Push mult to current index, for later accounting
        card_counter.insert(index, mult);

        // Update next cards
        for next_index in (index+1)..(index+1+match_number) {
            card_counter.insert(
                next_index,
                match card_counter.get(&next_index) {
                    None => 1 + mult,
                    Some(v) => v + mult,
                }
            );
        }
    }

    let result: u32 = card_counter.values().sum();
    result as i128
}
