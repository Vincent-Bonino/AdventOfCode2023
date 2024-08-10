use std::io::BufRead;
use crate::common::coordinates::XYCoordinates;

#[derive(Default)]
pub struct Schematic {
    pub numbers: Vec<SchematicNumber>,
    pub symbols: Vec<SchematicSymbol>,
}

#[derive(Debug)]
pub struct SchematicNumber {
    pub line: u32,
    pub col: u32,
    pub len: u32,
    pub value: u32,
}
impl SchematicNumber {
    pub fn get_tiles(self: &Self) -> Vec<XYCoordinates> {
        let mut result: Vec<XYCoordinates> = Vec::new();
        for i in 0..self.len {
            result.push(XYCoordinates { x: self.line as usize, y: (self.col + i) as usize });
        }
        result
    }
}

#[derive(Debug)]
pub struct SchematicSymbol {
    pub line: u32,
    pub col: u32,
    pub value: char,
}
impl SchematicSymbol {
    pub fn get_position(self: &Self) -> XYCoordinates {
        XYCoordinates { x: self.line as usize, y: self.col as usize }
    }
}
