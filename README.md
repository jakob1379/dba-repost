# dba-repost

<p align="center">
  <img src=".github/assets/repost-flow.svg" width="920" alt="Three inactive dba.dk ads move one at a time into a Firefox window controlled by Selenium, the repost button is clicked, and each ad lands in the reposted column while the console progress bar fills up and prints Finished reposting 3 ads!">
</p>

Repost all of your inactive ads on [dba.dk](https://www.dba.dk) in one run.
The script logs in to your account in Firefox, opens your inactive ads and
clicks repost on each one until the list is empty.

## How it works

1. Asks for your dba.dk email and password in the terminal. The password is
   read without echo and is never written to disk.
2. Opens Firefox through Selenium and logs in at `dba.dk/log-ind/`.
3. Opens `min-dbadk/mine-annoncer/inaktive-annoncer/` and collects every
   repost link.
4. Opens each link, clicks the repost button and waits for the ad page to
   load, with a progress bar in the terminal.
5. Reloads the inactive ads page and repeats until no inactive ads are left,
   then prints `Finished reposting N ads!` and closes the browser.

## Requirements

- Python 3.6 or newer
- Firefox and [geckodriver](https://github.com/mozilla/geckodriver) on your
  `PATH`
- `selenium` below 4.3 (the script uses `find_element_by_xpath`, which
  Selenium 4.3 removed)
- `progressbar2`

## Install

```bash
git clone https://github.com/jakob1379/dba-repost.git
cd dba-repost
pip install "selenium<4.3" progressbar2
```

## Usage

```bash
python src/main.py
```

```
usage: main.py [-h] [-t [time]]

dba-repost is a script to repost all ads which are due date from dba.dk

optional arguments:
  -h, --help            show this help message and exit
  -t [time], --timeout [time]
                        max time to wait for content to appear in webpage
```

| Option          | Default | What it does                                              |
| --------------- | ------- | --------------------------------------------------------- |
| `-t`, `--timeout` | `5`     | Seconds to wait for a dba.dk page to load before giving up |

If a page does not load in time, the script prints `Max timeout reached!` and
exits. On a slow connection, raise the timeout:

```bash
python src/main.py --timeout 15
```

The script finds buttons and lists by their position in dba.dk's HTML. If
dba.dk changes its page layout, those lookups stop matching and the script
needs updating.

## License

[MIT](LICENSE.md)
