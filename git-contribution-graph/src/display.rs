use anyhow::Result;
use chrono::{Datelike, Local, NaiveDate};
use std::collections::HashMap;

pub fn print_graph(
    data: &HashMap<NaiveDate, usize>,
    weeks: usize,
    tile_mode: bool,
) -> Result<()> {
    // Background colors
    let bg_rgb = (13, 17, 23);    // #0d1117 - Surround background
    let bg_ansi = rgb_to_ansi256(bg_rgb.0, bg_rgb.1, bg_rgb.2);

    // Text color (light gray)
    let text_rgb = (201, 209, 217); // #c9d1d9
    let text_ansi = rgb_to_ansi256(text_rgb.0, text_rgb.1, text_rgb.2);

    // 2. Hardcoded Palette - using RGB values that map to distinct ANSI256 codes
    let palette = vec![
        (21, 27, 35),   // Level 0 (No commits) -> ANSI 234
        (0, 95, 0),     // Level 1 -> ANSI 22 (darkest green in ANSI256)
        (0, 135, 0),    // Level 2 -> ANSI 28
        (0, 175, 95),   // Level 3 -> ANSI 35
        (86, 211, 100), // Level 4 -> ANSI 77
    ];

    // 3. Determine thresholds based on percentiles of non-zero contributions
    let mut counts: Vec<usize> = data.values().cloned().filter(|&c| c > 0).collect();
    counts.sort_unstable();

    let (t25, t50, t75) = if counts.is_empty() {
        (0.0, 0.0, 0.0)
    } else {
        let percentile = |p: f64| -> f64 {
            if counts.len() == 1 {
                return counts[0] as f64;
            }
            let rank = p * (counts.len() - 1) as f64;
            let lower = rank.floor() as usize;
            let upper = rank.ceil() as usize;
            let weight = rank - lower as f64;
            counts[lower] as f64 * (1.0 - weight) + counts[upper] as f64 * weight
        };
        (percentile(0.25), percentile(0.50), percentile(0.75))
    };

    // 4. Setup Grid
    let today = Local::now().date_naive();
    let days_from_sun = today.weekday().num_days_from_sunday();
    let start_date = today - chrono::Duration::days(days_from_sun as i64) - chrono::Duration::weeks((weeks - 1) as i64);

    let mut grid: Vec<Vec<String>> = vec![vec![String::new(); weeks]; 7];

    for w in 0..weeks {
        for d in 0..7 {
            let date = start_date + chrono::Duration::weeks(w as i64) + chrono::Duration::days(d as i64);
            
            let color_rgb = if date > today {
                bg_rgb
            } else {
                let count = *data.get(&date).unwrap_or(&0);
                let level = if count == 0 {
                    0
                } else {
                    let c = count as f64;
                    if c <= t25 { 1 }
                    else if c <= t50 { 2 }
                    else if c <= t75 { 3 }
                    else { 4 }
                };
                palette[level]
            };

            let ansi_code = rgb_to_ansi256(color_rgb.0, color_rgb.1, color_rgb.2);
            grid[d][w] = if tile_mode {
                // Tile mode: single block with black space after
                format!("\x1b[48;5;16;38;5;{}m■ ", ansi_code)
            } else {
                // Normal mode: colored background with spaces
                format!("\x1b[48;5;{}m  ", ansi_code)
            };
        }
    }

    // 5. Print
    let days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    let left_pad = "  ";
    let right_pad = "  ";
    let total_content_width = left_pad.len() + 4 + (weeks * 2) + right_pad.len();

    // In tile mode, use pure black background; otherwise use the GitHub dark background
    let print_bg = if tile_mode { 16 } else { bg_ansi }; // ANSI 16 = black

    let bg_line = |width: usize| {
        format!("\x1b[48;5;{}m{}\x1b[0m", print_bg, " ".repeat(width))
    };

    println!("{}", bg_line(total_content_width));
    for (i, row) in grid.iter().enumerate() {
        print!("\x1b[48;5;{}m{}", print_bg, left_pad);
        print!("\x1b[38;5;{}m{: <4}", text_ansi, days[i]);
        for cell in row {
            print!("{}", cell);
        }
        println!("\x1b[48;5;{}m{}\x1b[0m", print_bg, right_pad);
    }
    println!("{}", bg_line(total_content_width));

    Ok(())
}

fn rgb_to_ansi256(r: u8, g: u8, b: u8) -> u8 {
    let mut best_idx = 16;
    let mut min_dist = f64::MAX;
    for i in 16..=255 {
        let (cr, cg, cb) = ansi256_to_rgb(i);
        let dist = (r as f64 - cr as f64).powi(2) + (g as f64 - cg as f64).powi(2) + (b as f64 - cb as f64).powi(2);
        if dist < min_dist {
            min_dist = dist;
            best_idx = i;
        }
    }
    best_idx
}

fn ansi256_to_rgb(idx: u8) -> (u8, u8, u8) {
    if idx < 16 { return (0,0,0); }
    if idx < 232 {
        let i = idx - 16;
        let r = i / 36;
        let g = (i % 36) / 6;
        let b = i % 6;
        let map = |x| if x == 0 { 0 } else { 55 + x * 40 };
        return (map(r), map(g), map(b));
    }
    let i = idx - 232;
    let v = i * 10 + 8;
    (v, v, v)
}