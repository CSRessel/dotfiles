mod data;
mod display;

use chrono::{Datelike, Local, NaiveDate};
use clap::{Parser, ValueEnum};
use anyhow::Result;

#[derive(Debug, Clone, Copy, Default, ValueEnum)]
enum ColorMode {
    /// Use foreground colored blocks
    #[default]
    Tile,
    /// Use background colored cells
    Background,
}

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Number of weeks to display (ignored if --year is set)
    #[arg(short, long, default_value_t = 4)]
    weeks: usize,

    /// Show contributions for a specific year (e.g., 2024)
    #[arg(short, long)]
    year: Option<i32>,

    /// Color rendering mode
    #[arg(short, long, value_enum, default_value_t = ColorMode::Tile)]
    color: ColorMode,

    /// Show all day-of-week labels (default shows only Mon/Wed/Fri)
    #[arg(short = 'a', long)]
    all_labels: bool,

    /// Use black background (default uses terminal background)
    #[arg(short = 'b', long)]
    black_background: bool,

    /// Show squares for future dates
    #[arg(short = 's', long)]
    all_squares: bool,

    /// Show month labels above columns
    #[arg(short = 'm', long)]
    month_labels: bool,

    /// Directory to scan for git repositories (overrides default behavior)
    #[arg(short, long)]
    dir: Option<String>,
}

fn main() -> Result<()> {
    let args = Args::parse();
    let today = Local::now().date_naive();

    // Calculate start_date and weeks based on year or weeks argument
    let (start_date, weeks) = if let Some(year) = args.year {
        let jan1 = NaiveDate::from_ymd_opt(year, 1, 1).unwrap();
        let dec31 = NaiveDate::from_ymd_opt(year, 12, 31).unwrap();

        // Start from the Sunday of the week containing Jan 1
        let days_from_sun = jan1.weekday().num_days_from_sunday();
        let start = jan1 - chrono::Duration::days(days_from_sun as i64);

        // Calculate weeks needed to cover the year
        let days_to_cover = (dec31 - start).num_days() + 1;
        let weeks = ((days_to_cover + 6) / 7) as usize;

        (start, weeks)
    } else {
        let days_from_sun = today.weekday().num_days_from_sunday();
        let start = today - chrono::Duration::days(days_from_sun as i64)
                         - chrono::Duration::weeks((args.weeks - 1) as i64);
        (start, args.weeks)
    };

    let dir = args.dir.map(std::path::PathBuf::from);
    let data = data::get_contributions(weeks, dir)?;
    let tile_mode = matches!(args.color, ColorMode::Tile);
    display::print_graph(
        &data,
        start_date,
        weeks,
        tile_mode,
        args.all_labels,
        args.black_background,
        args.all_squares,
        args.month_labels,
    )?;

    Ok(())
}
