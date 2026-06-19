# RAuth - Reverse Engineering Writeup

**Author:** Empty(0mpty)
**Date:** 19.06.2026  
**Difficulty:** Easy  
**Category:** Reverse Engineering

---

## Tools Used

- Ghidra — static analysis
- edb (or gdb) — debugging
- netcat — remote connection

---

## Description

We are given a binary file that asks for a password and, upon successful authentication, prints the flag. The goal is to find the correct password and retrieve the flag.

---

## 1. Initial Analysis (Ghidra)

Open the binary in Ghidra. In the strings list, we see the following prompts:
Welcome to secure login portal!\nEnter the password to access the system:\n"
"Successfully Authenticated\nFlag:\n"

Searching for the password check logic leads to a function that uses `try_apply_keystream`. Static analysis reveals two code paths:

- `test BL, BL` → conditional jump to success or failure.
- Successful path prints the flag.

![Ghidra Analysis](screenshots/ghidra_analysis.png)

---

## 2. Patching (Bypassing the Check)

We patch the conditional jump (`jz`/`jnz`) to force success. After patching, the program outputs:
HTB{F4k3_f74g_4_t3s7ing}

This is a **fake flag** placed by the author to mislead anyone who stops at simple patching.

![Patching in Ghidra](screenshots/ghidra_patching.png)

---

## 3. Identifying the Algorithm

In the binary, we find the following constants:
0x61707865, 0x3320646e, 0x79622d32, 0x6b206574


These are the Salsa20/20 initialization constants (`"expand 32-byte k"`). Analyzing the internal state structure:

- Constants (4 words)
- 32-byte key
- 8-byte nonce
- Counter (usually 0)

![Salsa20 Constants](screenshots/salsa20_constants.png)

---

## 4. Extracting the Key via Debugger (edb)

We run the binary in `edb` and set a breakpoint after the Salsa20 state is initialized, before the encryption rounds.

In memory, we observe the state layout:
0x61707865 0x3320646e 0x79622d32 0x6b206574 ← constants
<key (16 bytes)>
<nonce (8 bytes)>
0x00000000 0x00000000 ← counter
<second half of key (16 bytes)>
0x61707865 0x3320646e 0x79622d32 0x6b206574 ← constants

The extracted key is:
TheCrucialRustEngineering@2021;)

This is a human-readable string, not a hash or raw binary data.

![edb Debugger Memory View](screenshots/edb_memory.png)

---

## 5. Testing on the HTB Server

We connect to the remote server:

```bash
nc 154.57.164.83 31770

Enter the password:
TheCrucialRustEngineering@2021;)

The server responds with:
Successfully Authenticated
Flag: HTB{...}
