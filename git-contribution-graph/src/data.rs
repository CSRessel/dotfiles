use anyhow::{Context, Result};
use chrono::{Duration, Local, NaiveDate};
use serde::Deserialize;
use std::collections::HashMap;
use std::fs;
use std::path::Path;
use std::process::Command;
use which::which;

pub fn get_contributions(weeks: usize) -> Result<HashMap<NaiveDate, usize>> {
    // Try GH CLI first
    if which("gh").is_ok() {
        if let Ok(data) = get_contributions_from_gh() {
            return Ok(data);
        }
    }

    // Fallback to local scan
    get_contributions_from_local(weeks)
}

#[derive(Deserialize)]
struct GhContributionDay {
    #[serde(rename = "contributionCount")]
    contribution_count: usize,
    date: String,
}

#[derive(Deserialize)]
struct GhWeek {
    #[serde(rename = "contributionDays")]
    contribution_days: Vec<GhContributionDay>,
}

#[derive(Deserialize)]
struct GhCalendar {
    weeks: Vec<GhWeek>,
}

#[derive(Deserialize)]
struct GhCollection {
    #[serde(rename = "contributionCalendar")]
    contribution_calendar: GhCalendar,
}

#[derive(Deserialize)]
struct GhViewer {
    #[serde(rename = "contributionsCollection")]
    contributions_collection: GhCollection,
}

#[derive(Deserialize)]
struct GhData {
    viewer: GhViewer,
}

#[derive(Deserialize)]
struct GhResponse {
    data: GhData,
}

fn get_contributions_from_gh() -> Result<HashMap<NaiveDate, usize>> {
    let query = "query { viewer { contributionsCollection { contributionCalendar { weeks { contributionDays { date contributionCount } } } } } }";

    let output = Command::new("gh")
        .args(&["api", "graphql", "-f", &format!("query={}", query)])
        .output()
        .context("Failed to execute gh api")?;

    if !output.status.success() {
        anyhow::bail!("gh api failed");
    }

    let response: GhResponse = serde_json::from_slice(&output.stdout)?;
    let mut map = HashMap::new();

    for week in response.data.viewer.contributions_collection.contribution_calendar.weeks {
        for day in week.contribution_days {
            if let Ok(date) = NaiveDate::parse_from_str(&day.date, "%Y-%m-%d") {
                map.insert(date, day.contribution_count);
            }
        }
    }

    Ok(map)
}

fn get_contributions_from_local(weeks: usize) -> Result<HashMap<NaiveDate, usize>> {
    let home = dirs::home_dir().context("Could not find home directory")?;
    let docs = home.join("Documents");

    let mut map = HashMap::new();

    // Check if Documents exists
    if !docs.exists() {
        return Ok(map);
    }

    // Get user email
    let email_output = Command::new("git")
        .args(&["config", "--get", "user.email"])
        .output()
        .context("Failed to get git user.email")?;

    let email = String::from_utf8_lossy(&email_output.stdout).trim().to_string();
    if email.is_empty() {
        // If no email configured, we can't reliably filter, but we'll try to proceed or return empty
        // Or we could list all commits, but contribution graph is usually per user.
        // Let's assume we need an email.
        return Ok(map);
    }

    // Calculate start date
    let start_date = Local::now().date_naive() - Duration::weeks(weeks as i64 + 1); // +1 buffer

    visit_dirs(&docs, &email, &start_date, &mut map)?;

    Ok(map)
}

fn visit_dirs(dir: &Path, email: &str, start_date: &NaiveDate, map: &mut HashMap<NaiveDate, usize>) -> Result<()> {
    if dir.is_dir() {
        if dir.join(".git").exists() {
            process_repo(dir, email, start_date, map)?;
            // Don't recurse into repos usually? Or should we?
            // "checking commit counts in all ~/Documents/ repos" implies recursion or flat list.
            // Repos usually aren't nested, but let's assume standard structure.
            // If we found a repo, we process it and stop recursion in this branch.
            return Ok(());
        }

        for entry in fs::read_dir(dir)? {
            let entry = entry?;
            let path = entry.path();
            if path.is_dir() {
                visit_dirs(&path, email, start_date, map)?;
            }
        }
    }
    Ok(())
}

fn process_repo(repo_path: &Path, email: &str, start_date: &NaiveDate, map: &mut HashMap<NaiveDate, usize>) -> Result<()> {
    let branches = ["main", "master", "dev"];

    for branch in branches {
        // Check if branch exists
        let check_branch = Command::new("git")
            .current_dir(repo_path)
            .args(&["rev-parse", "--verify", branch])
            .output();

        if let Ok(output) = check_branch {
            if output.status.success() {
                 let log_output = Command::new("git")
                    .current_dir(repo_path)
                    .args(&[
                        "log",
                        branch,
                        &format!("--author={}", email),
                        &format!("--since={}", start_date.format("%Y-%m-%d")),
                        "--format=%as" // YYYY-MM-DD
                    ])
                    .output();

                if let Ok(output) = log_output {
                    let stdout = String::from_utf8_lossy(&output.stdout);
                    for line in stdout.lines() {
                        if let Ok(date) = NaiveDate::parse_from_str(line, "%Y-%m-%d") {
                            *map.entry(date).or_insert(0) += 1;
                        }
                    }
                }
            }
        }
    }
    Ok(())
}
