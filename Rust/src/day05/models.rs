#[derive(Clone, Debug, PartialEq)]
pub struct Range {
    pub start: i64,
    pub end: i64,  // Note that the end value is NOT included
}

#[derive(Clone, Debug)]
pub struct Mapping {
    src_range: Range,
    dst_range: Range,
    length: i64,
}

#[derive(Debug)]
pub struct MappingSet {
    pub name: String,
    pub mappings: Vec<Mapping>,
}

#[derive(Debug, Default)]
pub struct Almanac {
    pub input_seeds: Vec<i64>,
    pub input_seed_ranges: Vec<Range>,
    pub mapping_sets: Vec<MappingSet>,
}


// Implementations

impl Range {
    pub fn new(start: i64, end: i64) -> Self {
        if start > end { panic!("Invalid range {start}-{end}") }
        Range { start, end }
    }

    pub fn from_length(start: i64, len: i64) -> Self {
        if len < 0 { panic!("Invalid range {start}->{len}") }
        Range { start, end: start+len }
    }

    pub fn length(self: &Self) -> i64 {
        self.end - self.start
    }

    pub fn contain_seed(self: &Self, seed: i64) -> bool {
        self.start <= seed && seed < self.end  // Note the '<=' then the '<'
    }

    // Range-Range operations

    pub fn includes(self: &Self, other: &Self) -> bool {
        self.start <= other.start && other.end <= self.end
    }

    pub fn overlap_with(self: &Self, other: &Self) -> bool {
        !(self.end <= other.start || other.end <= self.start)
    }

    pub fn shift_with(self: &Self, other: &Self) -> i64 {
        (self.start - other.start).abs()
    }
}

impl Mapping {
    pub fn new(dst_start: i64, src_start: i64, length: i64) -> Self {
        Mapping {
            src_range: Range::new(src_start, src_start + length),
            dst_range: Range::new(dst_start, dst_start + length),
            length,
        }
    }

    pub fn map_seed(self: &Self, seed: i64) -> i64 {
        if !self.src_range.contain_seed(seed) {
            seed
        } else {
            let distance: i64 = seed - self.src_range.start;
            self.dst_range.start + distance
        }
    }

    // Only a range included in self.src_range
    fn map_range(self: &Self, range: &Range) -> Range {
        if !self.src_range.includes(range) { panic!("Mapping not included range ({:?} -> {:?}", self.src_range, range) };

        Range::from_length(
            self.dst_range.start + self.src_range.shift_with(range),
            range.length(),
        )
    }

    // Returns (Vec<Range>, Vec<Range>)
    // First vec being not mapped values, second being mapped values
    pub fn map_seed_range(self: &Self, range: Range) -> (Vec<Range>, Vec<Range>) {
        // 4 possibles cases:
        //  1. src_range and range do not overlap   => no mapping, returning
        //  2. src_range includes range             => everything is mapped
        //  3. range includes src_range             => before and after is not mapped
        //  4. Partially overlap

        // 1.
        if !self.src_range.overlap_with(&range) {
            return ( vec![range], vec![] )
        }

        // 2.
        if self.src_range.includes(&range) {
            return ( vec![], vec![self.map_range(&range)])
        }

        // 3.
        if range.includes(&self.src_range) {
            let before_range: Range = Range::new(range.start, self.src_range.start);
            let mapped_range: Range = self.map_range(&self.src_range);
            let after_range: Range = Range::new(self.src_range.end, range.end);

            return ( vec![before_range, after_range], vec![mapped_range])
        }

        // 4.
        let to_map_range: Range;
        let not_mapped_range: Range;

        if self.src_range.start < range.start {
            to_map_range = Range::new(range.start, self.src_range.end);
            not_mapped_range = Range::new(self.src_range.end, range.end);
        } else {
            to_map_range = Range::new(self.src_range.start, range.end);
            not_mapped_range = Range::new(range.start, self.src_range.start);
        }

        // 'mapped_range' not mapped yet
        let mapped_range: Range = self.map_range(&to_map_range);
        (vec![not_mapped_range], vec![mapped_range])
    }
}

impl Almanac {
    pub fn new(seeds: Vec<i64>, mapping_sets: Vec<MappingSet>) -> Self {
        let mut seed_ranges: Vec<Range> = Vec::new();

        for ind in 0..(seeds.len()/2) {
            seed_ranges.push(
                Range {
                    start: seeds[2*ind],
                    end: seeds[2*ind] + seeds[2*ind+1],
                }
            )
        }

        Almanac {
            input_seeds: seeds,
            input_seed_ranges: seed_ranges,
            mapping_sets
        }
    }
}
