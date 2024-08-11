pub struct Scratchcard {
    pub card_id: u32,
    pub winning_numbers: Vec<u32>,
    pub numbers: Vec<u32>,
}
impl Scratchcard {
    pub fn get_matching_numbers(self: &Self) -> u32 {
        let mut win_counter: u32 = 0;
        for num in self.numbers.iter() {
            if self.winning_numbers.contains(&num) { win_counter += 1; }
        }
        win_counter
    }
    pub fn get_points(self: &Self) -> u32 {
        match self.get_matching_numbers() {
            0 => 0,
            v => 2_u32.pow(v - 1)
        }
    }
}
