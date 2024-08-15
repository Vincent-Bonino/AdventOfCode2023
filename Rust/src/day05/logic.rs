use crate::day05::models::{Almanac, Range};

pub fn solve_day05_part1(data: &Almanac) -> i128 {
    let mut results: Vec<i64> = Vec::new();

    for seed in data.input_seeds.iter() {
        let mut mapped_seed: i64 = *seed;

        for map_set in data.mapping_sets.iter() {
            let mut tmp_mapped_seed: i64 = mapped_seed;

            for mapping in map_set.mappings.iter() {
                tmp_mapped_seed = mapping.map_seed(mapped_seed);
                if tmp_mapped_seed != mapped_seed { break }  // Mapping occurred !
            }

            mapped_seed = tmp_mapped_seed;
        }

        results.push(mapped_seed);
    }

    let result: i64 = *results.iter().min().expect("Unable to compute minimum");
    result as i128
}

pub fn solve_day05_part2(data: &Almanac) -> i128 {
    let mut mapped_ranges: Vec<Range> = data.input_seed_ranges.clone();

    for mapping_set in data.mapping_sets.iter() {
        let mut to_map_ranges: Vec<Range> = mapped_ranges.clone();  // Ranges not yet mapped during this mapping_set
        mapped_ranges.clear();

        for mapping in mapping_set.mappings.iter() {
            let mut unmapped_by_mapping: Vec<Range> = Vec::new();

            while !to_map_ranges.is_empty() {
                let range: Range = to_map_ranges.pop().unwrap();
                let (unmapped, mapped) = mapping.map_seed_range(range.clone());
                unmapped_by_mapping.extend(unmapped);
                mapped_ranges.extend(mapped);
            }

            to_map_ranges = unmapped_by_mapping;

            if to_map_ranges.is_empty() { break }
        }

        // All mappings done, all ranges in 'tmp_current_seed_ranges' are unmapped, adding them for next mapping_set
        mapped_ranges.extend(to_map_ranges.clone());
        to_map_ranges.clear();
    }

    let result: i64 = mapped_ranges.iter().map(|range: &Range| range.start).min().unwrap();
    result as i128
}
