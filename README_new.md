# pfRICH Translation Stage Control

Python scripts for serial control of a **Thorlabs KDC101 K-Cube DC Servo Controller** driving a motorized translation stage, developed for the pfRICH (proximity-focusing Ring Imaging Cherenkov) detector project. Targets Linux Debian.

Communication uses the [Thorlabs APT binary serial protocol](https://www.thorlabs.com/Software/Motion%20Control/APT_Communications_Protocol.pdf).

---

## Hardware Requirements

- Thorlabs KDC101 K-Cube DC Servo Controller
- USB connection to host machine (FTDI-based USB-to-serial adapter)
- Linux Debian host (serial port appears as `/dev/ttyUSB0`)

---

## Dependencies

- Python 3
- [`pyserial`](https://pypi.org/project/pyserial/)

Install with:

```bash
pip install pyserial
```

---

## Repository Structure

| File | Description |
|------|-------------|
| `setup.py` | Opens the serial port, defines all protocol constants, and initializes the controller (IDENTIFY + ENABLE) |
| `home.py` | Homes the stage and reports final position |
| `move.py` | Sets velocity parameters and moves the stage to an absolute position |
| `getposition.py` | Queries and prints the current stage position in device units and mm |
| `home+move.py` | Monolithic script: homes the stage, performs a two-phase move, and reports position (no external dependencies) |

---

## Configuration

Key parameters are defined in `setup.py` and `home+move.py`:

| Constant | Value | Description |
|----------|-------|-------------|
| Serial port | `/dev/ttyUSB0` | Change if your device maps differently (check with `dmesg \| grep tty`) |
| `Device_Unit_SF` | 34304.96 | Position scale factor (device units per mm) |
| `Device_Unit_Vel` | 772981.3692 | Velocity scale factor |
| `Device_Unit_Acc` | 263.8443072 | Acceleration scale factor |
| `AbsDistance` | 20 mm | Target absolute move distance (edit in `move.py` or `home+move.py`) |
| `MaxVelocity` | 1.5 mm/s | Maximum move velocity (edit in `move.py`) |
| `Acceleration` | 1.0 mm/s² | Move acceleration (edit in `move.py`) |

Scale factors are sourced from page 34 of the APT Communications Protocol PDF (Issue 23).

---

## Setup

### 1. Verify USB connection

```bash
sudo dmesg | grep -i usb
```

If the device is not detected, try a different USB port. If the `ftdi_sio` kernel module is not loaded:

```bash
lsmod | grep ftdi_sio        # should show ftdi_sio if loaded
sudo modprobe ftdi_sio       # load the module if the above returns nothing
sudo dmesg | grep -i usb     # verify detection
```

### 2. Activate the Python virtual environment

```bash
cd /home/rhig
source translation/bin/activate
```

### 3. Verify the interpreter in VS Code (first time only)

1. Press `Ctrl+Shift+P` and select **Python: Select Interpreter**
2. Click **Enter interpreter path...**
3. Run `which python` in the activated terminal to get the path, then paste it into VS Code

---

## Usage

Run each script from within the activated virtual environment. If you encounter a permissions error on `/dev/ttyUSB0`, prefix with `sudo`.

### Home the stage

```bash
python home.py
```

Sends `MGMSG_MOT_MOVE_HOME`, waits for the `MGMSG_MOT_MOVE_HOMED` confirmation, prints position, then disables the channel and closes the port.

### Move to absolute position

```bash
python move.py
```

Sets velocity parameters, sends `MGMSG_MOT_MOVE_ABSOLUTE` (default: 20 mm), waits for `MGMSG_MOT_MOVE_COMPLETED`, prints position, then disables the channel and closes the port.

### Query current position

```bash
python getposition.py
```

Sends `MGMSG_MOT_REQ_USTATUSUPDATE` and prints the stage position in both device units and mm.

### Home then move (monolithic)

```bash
python home+move.py
```

Runs the full sequence in a single self-contained script: initialize → home → move (phase 1 at 0.5 mm/s) → move (phase 2 at 1.5 mm/s) → report position → close.

---

## APT Protocol Reference

All commands follow the Thorlabs APT binary serial protocol. Relevant message IDs used in these scripts:

| Message | Hex ID | Purpose |
|---------|--------|---------|
| `MGMSG_MOD_IDENTIFY` | `0x0223` | Flash controller LED |
| `MGMSG_MOD_SET_CHANENABLESTATE` | `0x0210` | Enable / disable channel |
| `MGMSG_MOT_MOVE_HOME` | `0x0443` | Begin homing sequence |
| `MGMSG_MOT_MOVE_HOMED` | `0x0444` | Confirmation: homing complete |
| `MGMSG_MOT_SET_VELPARAMS` | `0x0413` | Set velocity profile |
| `MGMSG_MOT_MOVE_ABSOLUTE` | `0x0453` | Move to absolute position |
| `MGMSG_MOT_MOVE_COMPLETED` | `0x0464` | Confirmation: move complete |
| `MGMSG_MOT_REQ_USTATUSUPDATE` | `0x0490` | Request status/position update |

Full protocol documentation: [APT Communications Protocol PDF](https://www.thorlabs.com/Software/Motion%20Control/APT_Communications_Protocol.pdf)

---

## Deactivating the Environment

When finished:

```bash
deactivate
```
