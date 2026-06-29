# UZEV Carrier — Bring-Up Boot Flow

**Date:** 2026-04-29  
**Applies to:** UZEV ADRV9009 Carrier Rev 1 + Avnet UltraZed-EV SOM (AES-ZU7EV-1-SOM-G)  
**Boot hardware:** SOM onboard 256Mb Micron QSPI flash (PS MIO0–5, soldered on module)  
**Bring-up interface:** J7 JTAG header → Digilent JTAG-HS3 programmer (DEC-015)

> **Source attribution:** Procedures are derived from Xilinx/AMD UG1283 (Vitis Unified
> Software Platform), UG1137 (Zynq UltraScale+ MPSoC Software Developer Guide),
> UG1144 (PetaLinux Tools Reference Guide), and ZCU106 bring-up documentation.
> Specific command syntax marked **[INFERRED]** should be verified against your
> installed Vitis/PetaLinux version before use. Vitis 2022.2 is the target toolchain.

---

## 1. Prerequisites

| Item | Version / Part |
|------|---------------|
| Vivado | 2022.2 Standard Edition |
| Vitis | 2022.2 |
| PetaLinux | 2022.2 |
| JTAG programmer | Digilent JTAG-HS3 |
| Host OS | Ubuntu 20.04 recommended (PetaLinux requirement) |
| XSA file | `system_top.xsa` from Vivado implementation (WNS=+0.438ns, verified) |

---

## 2. Boot mode selection on UltraZed-EV SOM

The UltraZed-EV SOM boot mode is set by a DIP switch on the SOM (SW1, 4-bit).
Two modes are used during bring-up:

| Mode | SW1 setting | Use |
|------|-------------|-----|
| JTAG | All OFF (0000) | Initial bring-up, FSBL load, QSPI programming |
| QSPI32 | 0010 (ON-OFF-ON-OFF) | Production / flight boot from onboard QSPI |

> **[INFERRED]** Confirm exact SW1 bit positions against Avnet UltraZed-EV Designer's
> Guide Table for boot mode pins (MIO[0:3] boot mode encoding, UG1085 §Boot Mode).
> The ZCU106 equivalent is SW6 with the same QSPI32 encoding (0010).

---

## 3. Phase 1 — Initial JTAG bring-up

### 3.1 Hardware setup

1. Set SOM SW1 to JTAG mode (all OFF).
2. Connect Digilent JTAG-HS3 to J7 (6-pin header, 2.54mm).
   J7 pinout (DEC-015, Convention B — Digilent compatible):

   | J7 Pin | Signal |
   |--------|--------|
   | 1 | TCK |
   | 2 | TDI |
   | 3 | TDO |
   | 4 | TMS |
   | 5 | GND |
   | 6 | VREF (3.3V) |

3. Apply 12V DC to J5 barrel jack.
4. Verify power-good LED D1 illuminates.

### 3.2 Vivado hardware server

```bash
# Start Vivado hardware server on host
hw_server
```

### 3.3 Load and run FSBL from Vitis (no persistent programming)

This verifies JTAG connectivity and DDR training before programming QSPI.

```tcl
# In Vitis xsct console [INFERRED — verify against Vitis 2022.2 xsct reference]
connect
targets
# Identify the ZCU7EV target; note its target number (usually target 2 = APU/A53)
targets 2
rst
dow /path/to/fsbl/Debug/fsbl.elf
con
after 3000
stop
```

Expected: FSBL prints to UART (J6) at 115200 8N1. Output should show:
```
Xilinx Zynq MP First Stage Boot Loader
...
InitDone
```

If UART output is absent: verify J6 wiring, check UART0 MIO pin assignment in
board.dtsi / XSA, confirm 3.3V level on J6 VREF pin.

---

## 4. Phase 2 — Build BOOT.BIN

### 4.1 Components

BOOT.BIN for QSPI boot contains (in order):

| Component | Source | Notes |
|-----------|--------|-------|
| FSBL | Vitis platform project | Built from XSA |
| PMU firmware | Vitis (auto-generated or custom) | Required for ZCU |
| PL bitstream | `system_top.bit` from Vivado | Optional at first boot; include for ADRV9009 |
| U-Boot | PetaLinux build | `u-boot.elf` |

### 4.2 PetaLinux build

```bash
# Create PetaLinux project [INFERRED — verify paths for 2022.2]
petalinux-create --type project --template zynqMP --name uzev_carrier
cd uzev_carrier
petalinux-config --get-hw-description /path/to/system_top.xsa

# Configure for QSPI boot
petalinux-config
# In menuconfig: DTG Settings → MACHINE_NAME → set to "zcu106-reva" or custom
# In menuconfig: Subsystem AUTO Hardware Settings → Advanced Bootable Images → Boot Image Settings
# → Image Storage Media → primary flash (QSPI)

petalinux-build
petalinux-package --boot --fsbl images/linux/zynqmp_fsbl.elf \
    --pmufw images/linux/pmufw.elf \
    --fpga images/linux/system.bit \
    --u-boot images/linux/u-boot.elf \
    --out images/linux/BOOT.BIN
```

> **[INFERRED]** The `petalinux-config` machine name and boot media settings may differ
> from ZCU106 defaults. Cross-reference UG1144 §Configuring PetaLinux for your hardware
> and the UltraZed-EV BSP if available from Avnet. An Avnet BSP for the UltraZed-EV
> SOM may be available at `avnet.me/zynq` — use it if present to avoid manual DTS work.

### 4.3 Bootgen (manual, without PetaLinux)

```
# boot.bif [INFERRED]
the_ROM_image:
{
    [fsbl_config] a53_x64
    [bootloader, destination_cpu=a53-0] fsbl.elf
    [pmufw_image] pmufw.elf
    [destination_cpu=a53-0, exception_level=el-3, trustzone] bl31.elf
    [destination_cpu=a53-0, exception_level=el-2] u-boot.elf
    [destination_device=pl] system.bit
}
```

```bash
bootgen -image boot.bif -arch zynqmp -o BOOT.BIN -w on
```

---

## 5. Phase 3 — Program SOM QSPI flash

The SOM QSPI is a Micron 256Mb (32MB) device. BOOT.BIN offset 0x0.
Maximum: 32MB total — FSBL+PMU+bitstream+u-boot must fit. A full ADRV9009 bitstream
is ~10MB; standard FSBL+PMU+u-boot is ~3MB. Total well within 32MB.

### 5.1 Via Vitis Flash Programmer (GUI)

1. Vitis → Xilinx → Program Flash.
2. Image file: `BOOT.BIN`.
3. Flash type: `qspi-x4-single` (or `qspi-x4-dual` — check SOM datasheet; Micron
   N25Q256A supports both; UltraZed-EV Designer's Guide specifies the wiring).
4. Offset: `0x0`.
5. FSBL: select `zynqmp_fsbl.elf` (Vitis uses this to initialize the PS before flash).
6. Click Program.

### 5.2 Via xsct (scriptable, preferred for CI/field re-flash)

```tcl
# xsct console [INFERRED — verify flash_type string against your SOM configuration]
connect
targets 1
# Target 1 = DAP; FSBL running on A53 is needed for flash init
program_flash -f BOOT.BIN \
              -offset 0 \
              -flash_type qspi-x4-single \
              -fsbl /path/to/zynqmp_fsbl.elf \
              -blank_check \
              -verify \
              -cable type xilinx_tcf url TCP:localhost:3121
```

Expected output:
```
...
Flash Operation Successful
```

> If `program_flash` fails with "Flash not detected": verify boot mode is JTAG (not
> QSPI), verify FSBL path is correct, and confirm flash_type matches the SOM's QSPI
> wiring (see Designer's Guide). The most common failure is using `qspi-x4-dual` on
> a board wired for `qspi-x4-single`.

---

## 6. Phase 4 — Boot from QSPI

1. Power off.
2. Set SOM SW1 to QSPI32 mode (see Section 2 table).
3. Power on. UART J6 should show FSBL → PMU → U-Boot → Linux boot sequence.

Expected UART output sequence:
```
Xilinx Zynq MP First Stage Boot Loader
...
U-Boot 2022.01 ...
...
Starting kernel ...
...
PetaLinux <version>
```

If Linux prompt does not appear:
- U-Boot hangs at `Loading Image`: rootfs partition not found — check QSPI partition
  table in u-boot env (`printenv`) and PetaLinux storage configuration.
- FSBL fails: SOM power rail issue — verify D1 LED, check UART for power-good errors.

---

## 7. Recovery — QSPI corruption or failed flash

If QSPI is corrupted or BOOT.BIN programming fails:

### 7.1 Recovery via JTAG (primary recovery path)

1. Set SOM SW1 to JTAG mode.
2. Connect JTAG-HS3 to J7.
3. Re-run Phase 3 (program_flash) with a known-good BOOT.BIN.
4. JTAG boot is always available regardless of QSPI state — JTAG mode bypasses QSPI.

This is the reason JTAG header J7 is kept on the flight carrier (DEC-015).
The 6-pin header occupies minimal board area and is the unconditional recovery path.

### 7.2 Recovery via SD card (secondary, when carrier SD slot is populated)

When the carrier SD card slot is installed (ADD_REV1 per DEC-021/022, Step 2):

1. Set SOM SW1 to SD boot mode.
   > **[INFERRED]** Confirm SW1 encoding for SD1 (PS MIO46–51) in Designer's Guide.
   > SD0 and SD1 have different boot mode encodings in UG1085 §Boot Mode table.
2. Prepare recovery SD card: FAT32, copy BOOT.BIN and `image.ub` to root.
3. Boot, then from U-Boot or Linux re-program QSPI:
   ```bash
   # From Linux, using mtd-utils [INFERRED]
   flashcp -v BOOT.BIN /dev/mtd0
   ```

### 7.3 SD not available (flight build with DNP SD slot)

For flight builds where SD slot is DNP: JTAG is the only recovery path.
This is acceptable for the UAV mission profile — JTAG recovery requires
physical access to the vehicle, which is assumed for any maintenance operation.

---

## 8. Reference documents

| Document | Number | Relevant sections |
|----------|--------|------------------|
| Zynq UltraScale+ MPSoC Software Developer Guide | UG1137 | Boot flow, FSBL, PMU firmware |
| PetaLinux Tools Reference Guide | UG1144 | Build, configuration, boot packaging |
| Vitis Unified Software Platform Doc | UG1283 | xsct, program_flash, debug |
| Zynq UltraScale+ MPSoC TRM | UG1085 | Boot modes (Ch.11), SD MIO (Ch.29), QSPI (Ch.24) |
| ZCU106 Evaluation Board User Guide | UG1244 | Board bring-up reference (§Getting Started) |
| Avnet UltraZed-EV Designer's Guide | UGAESZU7EVSOMGV1_2.pdf | SOM QSPI/eMMC wiring, boot mode SW1, MIO on JX3 |

> **Note on INFERRED items:** Sections marked [INFERRED] reflect expected behavior based
> on ZCU106 reference documentation and Zynq UltraScale+ toolchain conventions. They
> should be verified against the specific Vitis 2022.2 / PetaLinux 2022.2 release notes
> and the UltraZed-EV BSP before the first bring-up session. File any discrepancies as
> new DEC entries in DECISIONS_LOG.md.

---

*Created DEC-022 (2026-04-29). Update as bring-up proceeds.*
