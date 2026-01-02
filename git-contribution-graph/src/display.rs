use anyhow::Result;
use chrono::{Datelike, Local, NaiveDate};
use owo_colors::{OwoColorize, Rgb};
use std::collections::HashMap;

const BG: Rgb = Rgb(13, 17, 23);
const TEXT: Rgb = Rgb(201, 209, 217);
const LEVELS: [Rgb; 5] = [
    Rgb(21, 27, 35),   // Level 0 (No commits)
    Rgb(0, 95, 0),     // Level 1
    Rgb(0, 135, 0),    // Level 2
    Rgb(0, 175, 95),   // Level 3
    Rgb(86, 211, 100), // Level 4
];

pub struct DisplayConfig {
    pub start_date: NaiveDate,
    pub weeks: usize,
    pub tile_mode: bool,
    pub all_labels: bool,
    pub black_background: bool,
    pub all_squares: bool,
    pub month_labels: bool,
    pub total_count: Option<usize>,
}

pub fn print_graph(data: &HashMap<NaiveDate, usize>, cfg: &DisplayConfig) -> Result<()> {
    let thresholds = compute_thresholds(data);
    let today = Local::now().date_naive();
    let use_bg = cfg.black_background || !cfg.tile_mode;
    let bg_color = if cfg.tile_mode { Rgb(0, 0, 0) } else { BG };

    let days: [&str; 7] = if cfg.all_labels {
        ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    } else {
        ["", "Mon", "", "Wed", "", "Fri", ""]
    };

    // Header row (month labels or count or blank line)
    print_header(cfg, use_bg, bg_color);

    // Grid rows
    for (d, day_label) in days.iter().enumerate() {
        print_row_start(use_bg, bg_color);
        print!("{}", format!("{:<4}", day_label).color(TEXT));

        for w in 0..cfg.weeks {
            let date = cfg.start_date
                + chrono::Duration::weeks(w as i64)
                + chrono::Duration::days(d as i64);

            if date > today && !cfg.all_squares {
                print_empty_cell(cfg.tile_mode, use_bg, bg_color);
            } else {
                let count = *data.get(&date).unwrap_or(&0);
                let level = get_level(count, &thresholds);
                print_cell(cfg.tile_mode, use_bg, bg_color, LEVELS[level]);
            }
        }
        print_row_end(use_bg, bg_color);
    }

    // Bottom padding
    print_blank_line(cfg.weeks, use_bg, bg_color);
    Ok(())
}

fn compute_thresholds(data: &HashMap<NaiveDate, usize>) -> (f64, f64, f64) {
    let mut counts: Vec<usize> = data.values().cloned().filter(|&c| c > 0).collect();
    counts.sort_unstable();

    if counts.is_empty() {
        return (0.0, 0.0, 0.0);
    }
    if counts.len() == 1 {
        let v = counts[0] as f64;
        return (v, v, v);
    }

    let percentile = |p: f64| {
        let rank = p * (counts.len() - 1) as f64;
        let lo = rank.floor() as usize;
        let hi = rank.ceil() as usize;
        let w = rank - lo as f64;
        counts[lo] as f64 * (1.0 - w) + counts[hi] as f64 * w
    };
    (percentile(0.25), percentile(0.50), percentile(0.75))
}

fn get_level(count: usize, (t25, t50, t75): &(f64, f64, f64)) -> usize {
    if count == 0 {
        0
    } else {
        let c = count as f64;
        if c <= *t25 {
            1
        } else if c <= *t50 {
            2
        } else if c <= *t75 {
            3
        } else {
            4
        }
    }
}

fn print_header(cfg: &DisplayConfig, use_bg: bool, bg_color: Rgb) {
    let left_pad = "  ";
    let right_pad = "  ";

    if use_bg {
        print!("{}", left_pad.on_color(bg_color));
    } else {
        print!("{}", left_pad);
    }

    let count_str = cfg
        .total_count
        .map(|c| format!("{:<4}", c))
        .unwrap_or_else(|| "    ".into());
    print!("{}", count_str.color(TEXT));

    if cfg.month_labels {
        print_month_labels(cfg, use_bg, bg_color);
    } else {
        let spaces = " ".repeat(cfg.weeks * 2);
        if use_bg {
            print!("{}", spaces.on_color(bg_color));
        } else {
            print!("{}", spaces);
        }
    }

    if use_bg {
        println!("{}\x1b[0m", right_pad.on_color(bg_color));
    } else {
        println!("{}\x1b[0m", right_pad);
    }
}

fn print_month_labels(cfg: &DisplayConfig, use_bg: bool, bg_color: Rgb) {
    const MONTHS: [&str; 12] = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    ];

    let mut positions: Vec<(usize, &str)> = Vec::new();
    for w in 0..cfg.weeks {
        for d in 0..7 {
            let date = cfg.start_date
                + chrono::Duration::weeks(w as i64)
                + chrono::Duration::days(d as i64);
            if date.day() == 1 {
                positions.push((w, MONTHS[date.month0() as usize]));
                break;
            }
        }
    }

    let mut header = String::new();
    let mut last_col = 0;
    for (col, month) in &positions {
        let spaces = (col * 2).saturating_sub(last_col);
        header.push_str(&" ".repeat(spaces));
        header.push_str(month);
        last_col = col * 2 + month.len();
    }
    let remaining = (cfg.weeks * 2).saturating_sub(last_col);
    header.push_str(&" ".repeat(remaining));

    if use_bg {
        print!("{}", header.color(TEXT).on_color(bg_color));
    } else {
        print!("{}", header.color(TEXT));
    }
}

fn print_row_start(use_bg: bool, bg_color: Rgb) {
    if use_bg {
        print!("{}", "  ".on_color(bg_color));
    } else {
        print!("  ");
    }
}

fn print_row_end(use_bg: bool, bg_color: Rgb) {
    if use_bg {
        println!("{}\x1b[0m", "  ".on_color(bg_color));
    } else {
        println!("  \x1b[0m");
    }
}

fn print_empty_cell(tile_mode: bool, use_bg: bool, bg_color: Rgb) {
    if tile_mode {
        if use_bg {
            print!("{}", "  ".on_color(bg_color));
        } else {
            print!("  ");
        }
    } else {
        print!("{}", "  ".on_color(bg_color));
    }
}

fn print_cell(tile_mode: bool, use_bg: bool, bg_color: Rgb, color: Rgb) {
    if tile_mode {
        if use_bg {
            print!("{}", "■ ".color(color).on_color(bg_color));
        } else {
            print!("{}", "■ ".color(color));
        }
    } else {
        print!("{}", "  ".on_color(color));
    }
}

fn print_blank_line(weeks: usize, use_bg: bool, bg_color: Rgb) {
    let width = 4 + 4 + weeks * 2 + 2; // left_pad + label + cells + right_pad
    if use_bg {
        println!("{}\x1b[0m", " ".repeat(width).on_color(bg_color));
    } else {
        println!("{}\x1b[0m", " ".repeat(width));
    }
}
