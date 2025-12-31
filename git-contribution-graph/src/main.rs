mod data;
mod display;

use clap::Parser;
use anyhow::Result;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Number of weeks to display
    #[arg(short, long, default_value_t = 4)]
    weeks: usize,

    /// Hex color for the most active tile
    #[arg(short, long, default_value = "#56d364")]
    color: String,
}

fn main() -> Result<()> {
    let args = Args::parse();

    let data = data::get_contributions(args.weeks)?;
    display::print_graph(&data, args.weeks, &args.color)?;

    Ok(())
}
