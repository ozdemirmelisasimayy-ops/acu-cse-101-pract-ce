# 🎓 ACU CSE 101: Introduction to Programming — Practice & Workshops

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Krr0ptioN/acu-cse-101-pract-ce)

Welcome to the official student practice workspace for **CSE 101: Introduction to Programming** at **Acıbadem University (2026 Academic Year)**.

This repository is aligned with the textbook **_Think Python_ by Allen B. Downey** and configured for instant, zero-setup programming in **GitHub Codespaces**.

---

## Quickstart (Get Coding in 2 Minutes)

### Step 1: Fork this Repository
Click the **Fork** button at the top-right of this repository page to create your personal copy under your GitHub account.

### Step 2: Open in GitHub Codespaces
In your forked repository, click the green **Code** button, select the **Codespaces** tab, and click **Create codespace on main**.
*(Everything is pre-installed for you: Python 3.12, VS Code extensions, test runners, and auto-save).*

### Step 3: Start Coding & Check
1. Open the current week's folder in the left sidebar: [`exercises/week_01_intro/practice.py`](exercises/week_01_intro/practice.py).
2. Write your code and calculations directly in `practice.py`.
3. Use the **`$(checklist) Course Tasks`** menu on the left side of the bottom status bar:
   - **`Run Tests`** checks your answers.
   - **`Submit`** sends your practice work to the TAs after your tests pass.
   - **`Sync Course`** downloads newly released weekly exercises.
   - **`Play`** runs the Python file currently open in the editor.

---


## 📅 Course Curriculum & Progressive Weekly Releases

Exercises are released progressively week by week. Each week's challenge folder is kept in an independent release module:

| Week | Directory | Think Python Chapters | Topic Summary | Status |
|:---:|:---|:---|:---|:---:|
| **01** | [`exercises/week_01_intro/`](exercises/week_01_intro/) | Ch. 1 & 2 | The Way of the Program & Basic Arithmetic | **Released** |
| **02** | `exercises/week_02_variables/` | Ch. 2 | Variables, Expressions and Statements | *Weekly Release* |
| **03** | `exercises/week_03_functions/` | Ch. 3 | Functions, Parameters and Return Values | *Weekly Release* |
| **04** | `exercises/week_04_conditionals_recursion/` | Ch. 5 | Conditionals, Booleans & Recursion | *Weekly Release* |
| **05** | `exercises/week_05_iteration/` | Ch. 7 | Iteration, Loops, Newton's Square Root | *Weekly Release* |
| **06** | `exercises/week_06_strings_lists/` | Ch. 8 & 10 | Strings, Indexing, Slicing & Lists | *Weekly Release* |
| **07** | *Midterm I Review* | Ch. 1–10 | Comprehensive Practice Review | *In Class* |
| **08** | `exercises/week_08_dictionaries_tuples/` | Ch. 11 & 12 | Dictionaries and Tuples | *Weekly Release* |
| **09** | `exercises/week_09_files/` | Ch. 14 | File Reading, Writing and Exceptions | *Weekly Release* |
| **10** | `exercises/week_10_classes_objects/` | Ch. 15 | Classes, Objects and 2D Geometry | *Weekly Release* |
| **11** | `exercises/week_11_classes_functions/` | Ch. 16 | Classes, Time and Pure Functions | *Weekly Release* |
| **12** | `exercises/week_12_classes_methods/` | Ch. 17 | Object-Oriented Methods & Operator Overloading | *Weekly Release* |
| **13** | `exercises/week_13_inheritance/` | Ch. 18 | Inheritance & Card Deck Polymorphism | *Weekly Release* |
| **14** | *Midterm II Review* | Ch. 11–18 | Comprehensive OOP & Data Structures Review | *In Class* |
| **15** | *Final Project Prep* | All | Course Synthesis & Final Project | *In Class* |

---

## 🔄 Automatic Course Updates

Codespaces automatically check for new course materials at startup and every five
minutes while running. Published weeks appear in the workspace without student
action. The background watcher saves exercise changes before syncing, keeps
student answers when updates overlap, and backs up the working branch to the
student fork. Temporary network or backup failures are logged and retried.

The **Sync Course** action in **Course Tasks** is also available for an immediate
check. Instructor diagnostics are recorded in `.git/auto_commit.log`.

Existing Codespaces that still run the old save-only watcher require a one-time
instructor-managed rollout of the updated scripts. Publishing to the course
repository alone cannot replace a process already running in a student Codespace.

## Instructor automation and student submissions

The **Sync course and prepare student branches** GitHub Action runs on pushes to
course `main`, every Monday at **14:30 Istanbul time** (11:30 UTC), and by manual dispatch. It creates a persistent branch
named after each fork owner's GitHub username. Existing student branches are
never reset. It also redirects older `submit/week_*` PRs from `main` to the
student's username branch.

Submissions contain only the selected week's exercise folder. The Submit action
opens a PR from `student:submit/week_03_functions` into
`Krr0ptioN/acu-cse-101-pract-ce:student`. Instructor merges retain each student's
work on that branch. Automated grading uses the published course tests and the
bundled TA action, with results in the Actions job summary. Read-only fork tokens
may prevent posting a PR comment; they do not prevent grading.

### Automatic fork synchronization

Each fork's scheduled workflow uses GitHub's built-in `GITHUB_TOKEN` with
`contents: write` to update **its own** `main` and `workspace`. Students do not
configure tokens or secrets. The sync tool attempts an atomic Git push; a real
push rejection fails the run instead of being hidden behind a success message.
Repository metadata permission flags are not used to reject installation tokens.

The course repository's workflow provisions username branches and routes PRs.
It delegates normal fork updates to the workflow running inside each fork, since
its own token cannot write other repositories. For instructor-managed deployments
only, an optional `COURSE_SYNC_TOKEN` can authorize central writes to forks that
have already granted that credential access. That is not required for student
fork workflows.

The workflow merges course `main` into each fork's `main` and `workspace`,
preferring existing student content when edits overlap. New files and weeks are
added. Both branches are pushed atomically; concurrent pushes or unresolved
conflicts fail safely and are retried on the next run. It never force-pushes
student branches and never executes student code during synchronization.

After students bring in this update and run **Sync Course** once, the sync tool
also updates their fork's `main` and `workspace`, enables GitHub Actions when
needed, and activates the scheduled workflow using their existing GitHub login.
Each fork then updates itself every **Monday at 14:30 Istanbul time** using its
own `GITHUB_TOKEN`. Students do not need a shared instructor token or recurring
manual repository syncs. If GitHub refuses the initial activation because the
login lacks permissions, the tool reports that setup failed; this must be
resolved once before automatic updates can run.

GitHub can delay scheduled jobs during service load and disables inactive public
repository schedules after 60 days. The scheduled workflow runs from the fork's
default branch, which is why the first setup updates `main` as well as `workspace`.

Remote branch updates do not change files in a running Codespace. The course's
background watcher fetches updates every five minutes once its updated version
has been installed. Older save-only watchers still need instructor-managed
installation; a GitHub Action cannot replace a running process in a Codespace.
