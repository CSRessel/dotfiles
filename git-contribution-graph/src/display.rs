use anyhow::Result;
use chrono::{Datelike, Local, NaiveDate};
use std::collections::HashMap;

#[allow(clippy::too_many_arguments)]
pub fn print_graph(
    data: &HashMap<NaiveDate, usize>,
    start_date: NaiveDate,
    weeks: usize,
    tile_mode: bool,
    all_labels: bool,
    black_background: bool,
    all_squares: bool,
    month_labels: bool,
    total_count: Option<usize>,
) -> Result<()> {
    // Background colors
    let bg_rgb = (13, 17, 23); // #0d1117 - Surround background
    let bg_ansi = rgb_to_ansi256(bg_rgb.0, bg_rgb.1, bg_rgb.2);

    // Text color (light gray)
    let text_rgb = (201, 209, 217); // #c9d1d9
    let text_ansi = rgb_to_ansi256(text_rgb.0, text_rgb.1, text_rgb.2);

    // 2. Hardcoded Palette - using RGB values that map to distinct ANSI256 codes
    let palette = [
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

    let mut grid: Vec<Vec<String>> = vec![vec![String::new(); weeks]; 7];

    for w in 0..weeks {
        for (d, items) in grid.iter_mut().enumerate().take(7) {
            let date =
                start_date + chrono::Duration::weeks(w as i64) + chrono::Duration::days(d as i64);

            // For future dates, show empty space unless all_squares is set
            let is_future = date > today;
            if is_future && !all_squares {
                items[w] = if tile_mode {
                    if black_background {
                        "\x1b[48;5;16m  ".to_string()
                    } else {
                        "  ".to_string()
                    }
                } else {
                    format!("\x1b[48;5;{}m  ", bg_ansi)
                };
                continue;
            }

            let count = *data.get(&date).unwrap_or(&0);
            let level = if count == 0 {
                0
            } else {
                let c = count as f64;
                if c <= t25 {
                    1
                } else if c <= t50 {
                    2
                } else if c <= t75 {
                    3
                } else {
                    4
                }
            };
            let color_rgb = palette[level];

            let ansi_code = rgb_to_ansi256(color_rgb.0, color_rgb.1, color_rgb.2);
            items[w] = if tile_mode {
                // Tile mode: single block with space after
                if black_background {
                    format!("\x1b[48;5;16;38;5;{}m■ ", ansi_code)
                } else {
                    format!("\x1b[38;5;{}m■ ", ansi_code)
                }
            } else {
                // Background mode: colored background with spaces
                format!("\x1b[48;5;{}m  ", ansi_code)
            };
        }
    }

    // 5. Print
    // By default only show Mon/Wed/Fri; with all_labels show all days
    let days: [&str; 7] = if all_labels {
        ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    } else {
        ["", "Mon", "", "Wed", "", "Fri", ""]
    };
    let left_pad = "  ";
    let right_pad = "  ";
    let total_content_width = left_pad.len() + 4 + (weeks * 2) + right_pad.len();

    // Determine background: black if requested or background mode, otherwise no background
    let use_bg = black_background || !tile_mode;
    let print_bg = if !tile_mode { bg_ansi } else { 16 }; // GitHub dark or black

    let bg_line = |width: usize| {
        if use_bg {
            format!("\x1b[48;5;{}m{}\x1b[0m", print_bg, " ".repeat(width))
        } else {
            format!("{}\x1b[0m", " ".repeat(width))
        }
    };

    // Build month header if enabled
    let count_str = total_count.map(|c| c.to_string()).unwrap_or_default();
    if month_labels {
        let months = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        ];

        // Find which column each month starts in (column where 1st of month appears)
        let mut month_positions: Vec<(usize, &str)> = Vec::new();
        for w in 0..weeks {
            for d in 0..7 {
                let date = start_date
                    + chrono::Duration::weeks(w as i64)
                    + chrono::Duration::days(d as i64);
                if date.day() == 1 {
                    month_positions.push((w, months[date.month0() as usize]));
                    break; // Only need first day of week containing the 1st
                }
            }
        }

        // Build the header line
        let mut header = String::new();
        let mut last_col = 0;
        for (col, month) in &month_positions {
            // Add spaces to reach this column (each column is 2 chars wide)
            let spaces_needed = (col * 2).saturating_sub(last_col);
            header.push_str(&" ".repeat(spaces_needed));
            header.push_str(month);
            last_col = col * 2 + month.len();
        }

        // Print month header row
        if use_bg {
            print!("\x1b[48;5;{}m{}", print_bg, left_pad);
        } else {
            print!("{}", left_pad);
        }
        print!("\x1b[38;5;{}m{: <4}", text_ansi, count_str); // Show count if present
        print!("\x1b[38;5;{}m{}", text_ansi, header);
        let remaining = (weeks * 2).saturating_sub(last_col);
        if use_bg {
            println!(
                "\x1b[48;5;{}m{}{}\x1b[0m",
                print_bg,
                " ".repeat(remaining),
                right_pad
            );
        } else {
            println!("{}{}\x1b[0m", " ".repeat(remaining), right_pad);
        }
    } else if total_count.is_some() {
        if use_bg {
            print!("\x1b[48;5;{}m{}", print_bg, left_pad);
        } else {
            print!("{}", left_pad);
        }
        print!("\x1b[38;5;{}m{: <4}", text_ansi, count_str);
        let remaining = weeks * 2;
        if use_bg {
            println!(
                "\x1b[48;5;{}m{}{}\x1b[0m",
                print_bg,
                " ".repeat(remaining),
                right_pad
            );
        } else {
            println!("{}{}\x1b[0m", " ".repeat(remaining), right_pad);
        }
    } else {
        println!("{}", bg_line(total_content_width));
    }
    for (i, row) in grid.iter().enumerate() {
        if use_bg {
            print!("\x1b[48;5;{}m{}", print_bg, left_pad);
        } else {
            print!("{}", left_pad);
        }
        print!("\x1b[38;5;{}m{: <4}", text_ansi, days[i]);
        for cell in row {
            print!("{}", cell);
        }
        if use_bg {
            println!("\x1b[48;5;{}m{}\x1b[0m", print_bg, right_pad);
        } else {
            println!("{}\x1b[0m", right_pad);
        }
    }
    println!("{}", bg_line(total_content_width));

    Ok(())
}

fn rgb_to_ansi256(r: u8, g: u8, b: u8) -> u8 {
    let mut best_idx = 16;
    let mut min_dist = f64::MAX;
    for i in 16..=255 {
        let (cr, cg, cb) = ansi256_to_rgb(i);
        let dist = (r as f64 - cr as f64).powi(2)
            + (g as f64 - cg as f64).powi(2)
            + (b as f64 - cb as f64).powi(2);
        if dist < min_dist {
            min_dist = dist;
            best_idx = i;
        }
    }
    best_idx
}

fn ansi256_to_rgb(idx: u8) -> (u8, u8, u8) {
    if idx < 16 {
        return (0, 0, 0);
    }
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
