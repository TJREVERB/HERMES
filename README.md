# HERMES Testing Environment
Local simulation of REVERB's EPS, SATT-4 Radio, Iridium Radio, and Antenna Deployer.

---
<b>H</b>ighly

<b>E</b>xpandable

<b>R</b>EVERB

<b>M</b>echanical

<b>E</b>nvironment (for)

<b>S</b>imulation

---

## How to run a set of tests

Create `runfile.hermes`, with your test cases to run over an interval

Pass the filepath to `runfile.hermes` with `-t` or `--testfile`.

Example: `python hermes.py --config config.json -t runfile.hermes`

    # Example runfile.hermes
    runtime: 5  # in seconds
    steady_state: normal  # what kind of data is expected
    modules:  # what modules to activate during the test period
        - APRS
        - Antenna_Deployer
        - EPS
        - Iridium
    actions: # [time_stamp, action_name]
        - [1, brownout]
        - [2, shutdown_aprs]
    commands: # [time_stamp, command_str]
        - [4, print EPS]
        - [1.5, sfr TIME]

## How to run interactive tests

Do not use the `-t` or `--testfile` flags when running `main.py`. 

---

## All actions
| Action name   |      Module      |  What it does |
|----------|:-------------:|------:|
| brownout | EPS | Simulates a brownout event where the battery voltage drops significantly |


## Command Structure
| Headers   |      Args      |  What it does |
|----------|:-------------:|------:|
| print | module | Prints all the stuff in the module |
| sfr | state field name | Prints the value of the state field in the SFR |
| flag | error flag name | Prints the status of the error flag in the SFR | 


