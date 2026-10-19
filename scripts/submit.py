#!/usr/bin/env python3
"""ACU CSE 101 - Student Practice Submission Launcher.

===================================================
Runs local test suites and prepares a clean submission branch and Pull Request
to the upstream course repository.

Usage:
    python3 scripts/submit.py
    python3 scripts/submit.py --week week_01_intro
    python3 scripts/submit.py --test-only
"""

import argparse
import glob
import json
import os
import subprocess
import sys
import tempfile

try:
    from .course_automation import COURSE_REPOSITORY, student_login
    from .sync_course import checked_git, switch_to_workspace, workspace_lock
except ImportError:
    from course_automation import COURSE_REPOSITORY, student_login
    from sync_course import checked_git, switch_to_workspace, workspace_lock

# Terminal styling constants
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def get_available_weeks(repo_dir: str) -> list[str]:
    """Discover all exercise week folders."""
    exercises_dir = os.path.join(repo_dir, "exercises")
    if not os.path.isdir(exercises_dir):
        return []
    weeks = [
        os.path.basename(d)
        for d in sorted(glob.glob(os.path.join(exercises_dir, "week_*")))
        if os.path.isdir(d)
    ]
    return weeks


def select_week(repo_dir: str, requested_week: str | None) -> str:
    """Select the target week via argument or interactive menu."""
    available = get_available_weeks(repo_dir)
    if not available:
        print(
            f"{RED}Error: No week directories found in exercises/{RESET}",
            file=sys.stderr,
        )
        sys.exit(1)

    if requested_week:
        # Match exact or partial
        for w in available:
            if requested_week == w or requested_week in w:
                return w
        print(
            f"{RED}Error: Week '{requested_week}' not found in {available}{RESET}",
            file=sys.stderr,
        )
        sys.exit(1)

    if len(available) == 1:
        return available[0]

    print(f"\n{BOLD}{CYAN}=== Select Week to Test / Submit ==={RESET}")
    for idx, w in enumerate(available, 1):
        print(f"  [{idx}] {w}")

    while True:
        try:
            choice = input(f"\nEnter choice [1-{len(available)}]: ").strip()
            if not choice:
                return available[0]
            val = int(choice)
            if 1 <= val <= len(available):
                return available[val - 1]
            print(
                f"{YELLOW}Please enter a number between 1 and {len(available)}.{RESET}"
            )
        except (ValueError, KeyboardInterrupt):
            print("\nAborted.")
            sys.exit(0)


def run_tests(repo_dir: str, week: str) -> bool:
    """Executes pytest for the specified week's challenge test suite."""
    week_dir = os.path.join("exercises", week)
    full_path = os.path.join(repo_dir, week_dir)

    if not os.path.isdir(full_path):
        print(
            f"{RED}Error: Week directory not found: {week_dir}{RESET}",
            file=sys.stderr,
        )
        return False

    challenge_test = os.path.join(week_dir, "test_challenge.py")
    if os.path.isfile(os.path.join(repo_dir, challenge_test)):
        target = challenge_test
        print(
            f"\n{BOLD}{CYAN}🧪 Running Automated Graded Challenge Tests ({challenge_test})...{RESET}\n"
        )
    else:
        target = week_dir
        print(f"\n{BOLD}{CYAN}🧪 Running Automated Tests for {week}...{RESET}\n")

    res = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", target],
        cwd=repo_dir,
        check=False,
    )
    return res.returncode == 0


def get_current_branch(repo_dir: str) -> str:
    """Return the name of the currently checked out git branch."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        return res.stdout.strip() or "main"
    except OSError:
        return "main"


def run_gh(repo_dir: str, args: list[str], body: str | None = None):
    result = subprocess.run(
        ["gh", *args], cwd=repo_dir, input=body, capture_output=True,
        text=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def ensure_committed(repo_dir: str):
    """Save exercise edits without resetting the persistent workspace branch."""
    switch_to_workspace(repo_dir)
    checked_git(["add", "exercises/"], repo_dir)
    status = checked_git(["status", "--porcelain", "exercises/"], repo_dir)
    if status.stdout.strip():
        checked_git(["commit", "-m", "Pre-submission snapshot", "--", "exercises/"], repo_dir)


def handle_submission(repo_dir: str, week: str):
    """Submit this week's files to the student's persistent course branch."""
    with workspace_lock(repo_dir):
        _submit(repo_dir, week)


def _submit(repo_dir: str, week: str):
    if week not in get_available_weeks(repo_dir):
        raise RuntimeError("Unknown exercise week.")
    # Resolve the actual fork owner, never a guessed Git identity or local branch.
    origin = checked_git(["remote", "get-url", "origin"], repo_dir).stdout.strip()
    fork = json.loads(run_gh(repo_dir, ["repo", "view", origin, "--json", "nameWithOwner,owner,parent,isFork"]))
    parent = fork.get("parent") or {}
    if not fork.get("isFork") or f"{parent.get('owner', {}).get('login', '')}/{parent.get('name', '')}".lower() != COURSE_REPOSITORY.lower():
        raise RuntimeError("Submit from your personal fork of the course repository.")
    username = student_login(fork["owner"]["login"])
    # The central action owns branch creation; student tokens need no course write access.
    try:
        run_gh(repo_dir, ["api", f"repos/{COURSE_REPOSITORY}/git/ref/heads/{username}"])
    except RuntimeError as error:
        raise RuntimeError(f"Your course branch '{username}' is not ready. Ask your instructor to run the course sync action.") from error

    ensure_committed(repo_dir)
    original_branch = get_current_branch(repo_dir)
    source = checked_git(["rev-parse", "HEAD"], repo_dir).stdout.strip()
    branch_name = f"submit/{week}"
    print(f"Preparing {username}:{branch_name} → {COURSE_REPOSITORY}:{username}")
    checked_git(["fetch", "origin", "+refs/heads/*:refs/remotes/origin/*"], repo_dir)
    checked_git(["fetch", f"https://github.com/{COURSE_REPOSITORY}.git", f"refs/heads/{username}"], repo_dir)
    try:
        checked_git(["checkout", "-B", branch_name, "FETCH_HEAD"], repo_dir)
        # Base each submission on the instructor's retained work; include only this week.
        checked_git(["restore", f"--source={source}", "--staged", "--worktree", "--", f"exercises/{week}"], repo_dir)
        changed = checked_git(["diff", "--cached", "--name-only"], repo_dir).stdout.strip()
        if not changed:
            print("This week's files already match your course branch; nothing new to submit.")
            return
        checked_git(["commit", "-m", f"Submission: {week}"], repo_dir)
        checked_git(["push", "--force-with-lease", "origin", f"HEAD:refs/heads/{branch_name}"], repo_dir)
        existing = json.loads(run_gh(repo_dir, [
            "api", "--method", "GET", f"repos/{COURSE_REPOSITORY}/pulls",
            "-f", "state=open", "-f", f"head={username}:{branch_name}",
        ]))
        if existing:
            pr = existing[0]
            if pr["base"]["ref"] != username:
                run_gh(repo_dir, ["pr", "edit", str(pr["number"]), "--repo", COURSE_REPOSITORY, "--base", username])
            print(f"Submission updated: {pr['html_url']}")
            return
        body = f"Automated submission for `{week}`.\n\nLocal challenge tests passed. Merge into `{username}` to retain this student's work.\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md") as body_file:
            body_file.write(body)
            body_file.flush()
            url = run_gh(repo_dir, [
                "pr", "create", "--repo", COURSE_REPOSITORY,
                "--head", f"{username}:{branch_name}", "--base", username,
                "--title", f"Submission: {week} ({username})", "--body-file", body_file.name,
            ])
        print(f"Submission successful: {url}")
    finally:
        checked_git(["checkout", original_branch], repo_dir)


def main():
    parser = argparse.ArgumentParser(
        description="ACU CSE 101 - Test Runner & Submission Launcher"
    )
    parser.add_argument(
        "--week",
        help="Target week to test/submit (e.g., 'week_01_intro')",
    )
    parser.add_argument(
        "--test-only",
        action="store_true",
        help="Only run tests without creating a submission branch",
    )

    args = parser.parse_args()
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    target_week = select_week(repo_dir, args.week)
    passed = run_tests(repo_dir, target_week)

    if not passed:
        print(f"\n{RED}{BOLD}❌ Some tests failed.{RESET}")
        print(
            f"{YELLOW}Please review the test failures above, fix your code, and run submission again.{RESET}\n"
        )
        sys.exit(1)

    print(f"\n{GREEN}{BOLD}✅ All tests for {target_week} PASSED!{RESET}")

    if args.test_only:
        print("Test run completed.")
        sys.exit(0)

    try:
        handle_submission(repo_dir, target_week)
    except (RuntimeError, ValueError) as error:
        print(f"{RED}Submission could not finish:{RESET} {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
