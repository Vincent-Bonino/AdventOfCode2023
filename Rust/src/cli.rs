use clap::Parser;

#[derive(Parser, Debug)]
pub struct Args {
    // Number of day to run, 0 for all
    #[arg(default_value_t = 0)]
    pub day: usize,

    // Test mode
    #[arg(short, long, default_value_t = false)]
    pub use_tests: bool,
}
