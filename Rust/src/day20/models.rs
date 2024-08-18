use std::collections::HashMap;
use std::fmt::{write, Display, Formatter, Result};

use dyn_clone::DynClone;

#[derive(Copy, Clone, PartialEq)]
/// Pulse send/received by logic elements
pub enum Pulse {
    High,
    Low,
}
impl Pulse {
    pub fn switch(self: &Self) -> Self {
        match self {
            Pulse::Low => Pulse::High,
            Pulse::High => Pulse::Low,
        }
    }
}
impl Display for Pulse {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        let str_value: String = match self {
            Pulse::High => String::from("high"),
            Pulse::Low => String::from("low"),
        };
        write!(f, "{}", str_value)
    }
}

#[derive(Clone)]
pub struct EmittedSignal {
    pub src_module: String,
    pub dst_module: String,
    pub pulse: Pulse,
}
impl EmittedSignal {
    pub fn new(src: &str, dst: &str, pulse: Pulse) -> Self {
        EmittedSignal {
            src_module: String::from(src),
            dst_module: String::from(dst),
            pulse,
        }
    }
}
impl Display for EmittedSignal {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        write!(f, "{} -{}-> {}", self.src_module, self.pulse, self.dst_module)
    }
}

/// Shared behavior between all modules
pub trait Module: DynClone {
    fn set_input_modules(self: &mut Self, _input_modules: Option<&Vec<String>>) {}
    fn get_full_name(self: &Self) -> String;
    fn get_name(self: &Self) -> String;
    fn get_output_modules(self: &Self) -> Vec<String>;
    fn process_and_emit(self: &mut Self, signal: EmittedSignal) ->  Vec<EmittedSignal>;
}

dyn_clone::clone_trait_object!(Module);


/// Module Flip-Flop (%):
/// Can flip between "on" state and "off" state, starts "off".
/// On H, does nothing.
/// On L, flips state.
///   - On "off"->"on": emits H
///   - On "on"->"off": emits L
#[derive(Clone)]
pub struct FlipFlop {
    name: String,
    output_indexes: Vec<String>,

    state: Pulse,  // Low for "off", High for "on"
    switched: bool
}
impl FlipFlop {
    pub fn new(name: String, output_indexes: Vec<String>) -> Self {
        FlipFlop {
            name,
            output_indexes,
            state: Pulse::Low,
            switched: false,
        }
    }
}
impl Module for FlipFlop {
    fn get_full_name(self: &Self) -> String {
        format!("%{}", self.get_name())
    }
    fn get_name(self: &Self) -> String {
        self.name.clone()
    }
    fn get_output_modules(self: &Self) -> Vec<String> {
        self.output_indexes.clone()
    }
    fn process_and_emit(self: &mut Self, signal: EmittedSignal) ->  Vec<EmittedSignal> {
        // Process
        if let Pulse::Low = signal.pulse {
            self.state = self.state.switch();
            self.switched = true
        }

        // Emit
        let mut result: Vec<EmittedSignal> = Vec::new();

        if self.switched {
            self.switched = false;
            for out_ind in self.output_indexes.iter() {
                result.push(
                    EmittedSignal::new(&self.name, out_ind, self.state)
                )
            }
        }

        result
    }
}

/// Module Conjunction (&):
/// Stores input from each incoming connections, starting at L.
/// On H/L, update its storage.
/// If only remembering H: emits L
/// Otherwise: emits H
#[derive(Clone)]
pub struct Conjunction {
    name: String,
    output_indexes: Vec<String>,

    storage: HashMap<String, Pulse>,
}
impl Conjunction {
    pub fn new(name: String, output_indexes: Vec<String>) -> Self {
        Conjunction {
            name,
            output_indexes,
            storage: HashMap::new(),
        }
    }
    fn has_only_high(self: &Self) -> bool {
        self.storage.iter().all(
            |(_key, value)| {
                match value {
                    Pulse::High => true,
                    Pulse::Low => false,
                }
            }
        )
    }
}
impl Module for Conjunction {
    fn set_input_modules(self: &mut Self, input_modules: Option<&Vec<String>>) {
        match input_modules {
            None => return,
            Some(vec) => {
                for input_mod in vec {
                    self.storage.insert(input_mod.clone(), Pulse::Low);
                }
            }
        };
    }
    fn get_full_name(self: &Self) -> String {
        format!("&{}", self.get_name())
    }
    fn get_name(self: &Self) -> String {
        self.name.clone()
    }
    fn get_output_modules(self: &Self) -> Vec<String> {
        self.output_indexes.clone()
    }
    fn process_and_emit(self: &mut Self, signal: EmittedSignal) -> Vec<EmittedSignal> {
        // Process
        self.storage.insert(signal.src_module.to_string(), signal.pulse);

        // Emit
        let pulse: Pulse = match self.has_only_high() {
            true => Pulse::Low,
            false => Pulse::High,
        };
        let mut result: Vec<EmittedSignal> = Vec::new();

        for out_ind in self.output_indexes.iter() {
            result.push(
                EmittedSignal::new(&self.name, out_ind, pulse)
            )
        };

        result
    }
}


/// Module Broadcaster:
/// Sends input to each outgoing connections.
/// On H/L, emits respectively H/L.
#[derive(Clone)]
pub struct Broadcaster {
    name: String,
    output_indexes: Vec<String>,

    state: Pulse,  // Last received pulse
}
impl Broadcaster {
    pub fn new(name: String, output_indexes: Vec<String>) -> Self {
        if name != String::from("broadcaster") { panic!("Unexpected name {name} for broadcaster") }
        Broadcaster {
            name,
            output_indexes,
            state: Pulse::Low,  // Init value does not matter
        }
    }
}
impl Module for Broadcaster {
    fn get_full_name(self: &Self) -> String {
        self.get_name()
    }
    fn get_name(self: &Self) -> String {
        self.name.clone()
    }
    fn get_output_modules(self: &Self) -> Vec<String> {
        self.output_indexes.clone()
    }
    fn process_and_emit(self: &mut Self, signal: EmittedSignal) -> Vec<EmittedSignal> {
        // Process
        self.state = signal.pulse;

        // Emit
        let mut result: Vec<EmittedSignal> = Vec::new();

        for out_ind in self.output_indexes.iter() {
            result.push(
                EmittedSignal::new(&self.name, out_ind, self.state)
            )
        }

        result
    }
}
