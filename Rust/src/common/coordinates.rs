#[derive(Eq, PartialEq, Debug)]
pub struct XYCoordinates {
    pub x: usize,
    pub y: usize,
}

impl XYCoordinates {
    pub fn get_neighbours4(self: &Self) -> Vec<XYCoordinates> {
        Vec::from([
            XYCoordinates { x: self.x + 0, y: self.y + 1},
            XYCoordinates { x: self.x + 0, y: self.y - 1},
            XYCoordinates { x: self.x + 1, y: self.y + 0},
            XYCoordinates { x: self.x - 1, y: self.y + 0},
        ])
    }

    pub fn get_neighbours8(self: &Self) -> Vec<XYCoordinates> {
        Vec::from([
            XYCoordinates { x: self.x - 1, y: self.y - 1},
            XYCoordinates { x: self.x - 1, y: self.y + 0},
            XYCoordinates { x: self.x - 1, y: self.y + 1},
            XYCoordinates { x: self.x + 0, y: self.y - 1},
            XYCoordinates { x: self.x + 0, y: self.y + 1},
            XYCoordinates { x: self.x + 1, y: self.y - 1},
            XYCoordinates { x: self.x + 1, y: self.y + 0},
            XYCoordinates { x: self.x + 1, y: self.y + 1},
        ])
    }
}
