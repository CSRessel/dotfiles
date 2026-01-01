mod data;
mod display;

use clap::{Parser, ValueEnum};
use anyhow::Result;

#[derive(Debug, Clone, Copy, Default, ValueEnum)]
enum ColorMode {
    /// Use foreground colored blocks on black background
    #[default]
    Tile,
    /// Use background colored cells
    Background,
}

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Number of weeks to display
    #[arg(short, long, default_value_t = 4)]
    weeks: usize,

    /// Color rendering mode
    #[arg(short, long, value_enum, default_value_t = ColorMode::Tile)]
    color: ColorMode,
}

fn main() -> Result<()> {
    let args = Args::parse();

    let data = data::get_contributions(args.weeks)?;
    let tile_mode = matches!(args.color, ColorMode::Tile);
    display::print_graph(&data, args.weeks, tile_mode)?;

    Ok(())
}
