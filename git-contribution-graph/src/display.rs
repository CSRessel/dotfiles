use anyhow::{Context, Result};
use chrono::{Datelike, Local, NaiveDate};
use std::collections::HashMap;

pub fn print_graph(
    data: &HashMap<NaiveDate, usize>,
    weeks: usize,
    color_hex: &str,
) -> Result<()> {
    // 1. Parse color
    let end_color = parse_hex(color_hex).context("Invalid hex color")?;
    // GitHub empty color (approximate gray)
    let start_color = (235, 237, 240); // #ebedf0

    // 2. Generate palette (0..=4)
    // Level 0 is always the background gray for 0 commits.
    // Level 1-4 are shades for >0 commits.
    // But GitHub logic is: 0 commits -> Level 0.
    // >0 commits -> map to Level 1-4 based on quartiles.
    // For simplicity, we can do linear interpolation for the colors.
    // Level 0: start_color
    // Level 4: end_color

    let palette = interpolate_colors(start_color, end_color, 5);

    // 3. Determine max commits to scale the graph
    let max_commits = *data.values().max().unwrap_or(&0);

    // 4. Print Graph
    // Columns: weeks
    // Rows: 7 days (Sun-Sat)

    let today = Local::now().date_naive();
    let days_from_sun = today.weekday().num_days_from_sunday();
    let start_date = today - chrono::Duration::days(days_from_sun as i64) - chrono::Duration::weeks((weeks - 1) as i64);

    // We'll buffer the output to print row by row
    let mut grid: Vec<Vec<String>> = vec![vec![String::new(); weeks]; 7];

    for w in 0..weeks {
        for d in 0..7 {
            let date = start_date + chrono::Duration::weeks(w as i64) + chrono::Duration::days(d as i64);
            if date > today {
                grid[d][w] = "  ".to_string(); // Future days blank
                continue;
            }

            let count = *data.get(&date).unwrap_or(&0);
            let level = if count == 0 {
                0
            } else if max_commits <= 0 {
                0
            } else {
                // Map 1..max to 1..4
                // A simple bucketing:
                // 1..max/4 -> 1
                // ...
                // But often max is small.
                // If max < 4, just map count to count?
                if max_commits < 4 {
                    count.min(4)
                } else {
                     // Normalize count (1..max) to (0..1) then * 3 then + 1
                     let normalized = (count as f64 - 1.0) / (max_commits as f64 - 1.0);
                     (normalized * 3.0).round() as usize + 1
                }
            };

            let color_rgb = palette[level.min(4)];
            let ansi_code = rgb_to_ansi256(color_rgb.0, color_rgb.1, color_rgb.2);

            // Block char with color
            // \x1b[38;5;{code}m for foreground
            // \x1b[48;5;{code}m for background
            // We use a block character '■' or just space with background?
            // GitHub uses colored squares. Space with background is easiest for "square" look.
            // But typical terminal fonts are tall. Two spaces?
            grid[d][w] = format!("\x1b[48;5;{}m  \x1b[0m", ansi_code);
        }
    }

    // Print to stdout
    // Maybe print day names?
    let days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    for (i, row) in grid.iter().enumerate() {
        print!("{} ", days[i]); // simple label
        for cell in row {
            print!("{}", cell);
        }
        println!();
    }

    Ok(())
}

fn parse_hex(hex: &str) -> Result<(u8, u8, u8)> {
    let hex = hex.trim_start_matches('#');
    if hex.len() != 6 {
        anyhow::bail!("Hex color must be 6 chars");
    }
    let r = u8::from_str_radix(&hex[0..2], 16)?;
    let g = u8::from_str_radix(&hex[2..4], 16)?;
    let b = u8::from_str_radix(&hex[4..6], 16)?;
    Ok((r, g, b))
}

fn interpolate_colors(start: (u8, u8, u8), end: (u8, u8, u8), steps: usize) -> Vec<(u8, u8, u8)> {
    let mut colors = Vec::new();
    if steps == 0 { return colors; }
    if steps == 1 {
        colors.push(start);
        return colors;
    }

    for i in 0..steps {
        let t = i as f64 / (steps - 1) as f64;
        let r = (start.0 as f64 + t * (end.0 as f64 - start.0 as f64)).round() as u8;
        let g = (start.1 as f64 + t * (end.1 as f64 - start.1 as f64)).round() as u8;
        let b = (start.2 as f64 + t * (end.2 as f64 - start.2 as f64)).round() as u8;
        colors.push((r, g, b));
    }
    colors
}

fn rgb_to_ansi256(r: u8, g: u8, b: u8) -> u8 {
    // 6x6x6 Color Cube: 16 + 36*R + 6*G + B
    // where R,G,B are 0..5
    // Map 0..255 to 0..5
    // Thresholds: 0, 95, 135, 175, 215, 255 (standard xterm)
    // But simple linear division is okay for approximation:
    // val / 51? 255/51 = 5.

    // Better mapping logic for xterm 256 colors
    let to_cube = |x: u8| -> u8 {
        if x < 48 { 0 }
        else if x < 115 { 1 }
        else { (x - 35) / 40 }
    };

    let r_idx = to_cube(r);
    let g_idx = to_cube(g);
    let b_idx = to_cube(b);

    16 + 36 * r_idx + 6 * g_idx + b_idx
}
