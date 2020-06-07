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

Create `runstack.yaml`, with your test cases to run over an interval

Pass the filepath to `runstack.yaml` with `-t` or `--testfile`.

Example: `python main.py --config config.json -t runstack.yaml`

    # Example runstack.yaml
    runtime: 5  # in seconds
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

`python main.py -c config.json`

---

## Generators
Generators describe what the behavior of the modules on the satellite will be. This influences what kind of data pFS will read and put into the SFR. 

| Generator name | APRS |  Iridium | Antenna Deployer | EPS |
|:----------:|:-------------|:------|:------|:------|
| BOOT | No uplink |  |  | | 
| STARTUP | Uplink when downlink |  |  | | 
| NORMAL | Uplink commands sent through runstack / interactive ;; Uplink random requests for SFR entries, beacons, and dumps |  |  | | 
| LOW_POWER | Uplink commands sent through runstack / interactive ;; Uplink random requests for SFR entries, beacons, and dumps |  |  | | 
| DANGER | APRS serial throws exception |  |  | | 


## Commands
Commands are run through the interactive shell or runstack. They help pull out information from pFS to examine what is actually occurring during simulations. 

| Headers   |      Args      |  What it does |
|:----------:|:-------------:|:------:|
| print | module | Prints all the stuff in the module |
| sfr | state field name | Prints the value of the state field in the SFR |
| flag | error flag name | Prints the status of the error flag in the SFR | 
| action | action name | Triggers the action |


## Actions
Actions are events which could occur during flight. Triggering an action simulates the event in orbit. Actions can be run via commands or the runstack.

| Action name   |      Module      |  What it does |
|:----------:|:-------------:|:------:|
| brownout | EPS | Simulates a brownout event where the battery voltage drops significantly |




