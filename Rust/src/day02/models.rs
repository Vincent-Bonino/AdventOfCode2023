#[derive(Clone)]
pub struct Game {
    pub id: u32,
    pub bags: Vec<Bag>,
}

impl Game {
    pub fn is_valid(self: &Self, reference_bag: &Bag) -> bool {
        let mut result: bool = true;
        for bag in self.bags.iter() {
            result &= bag.le(reference_bag);
        };
        result
    }
    
    pub fn hypothetical_min_bag(self: &Self) -> Bag {
        Bag {
            red: self.bags.iter().map(|bag| { bag.red }).max().unwrap(),
            green: self.bags.iter().map(|bag| { bag.green }).max().unwrap(),
            blue: self.bags.iter().map(|bag| { bag.blue }).max().unwrap(),
        }
    }
}

#[derive(Copy, Clone)]
pub struct Bag {
    red: u32,
    green: u32,
    blue: u32,
}

impl Bag {
    pub fn new(red: u32, green: u32, blue: u32) -> Self {
        Bag { red, green, blue }
    }

    pub fn from_red(quantity: u32) -> Self {
        Bag { red: quantity, green: 0, blue: 0 }
    }
    pub fn from_green(quantity: u32) -> Self {
        Bag { red: 0, green: quantity, blue: 0 }
    }
    pub fn from_blue(quantity: u32) -> Self {
        Bag { red: 0, green: 0, blue: quantity }
    }

    pub fn power(self: &Self) -> u32 {
        self.red * self.green * self.blue
    }

    // Comparison
    pub fn le(self: &Self, other: &Self) -> bool {
        self.red <= other.red && self.green <= other.green && self.blue <= other.blue
    }
}
