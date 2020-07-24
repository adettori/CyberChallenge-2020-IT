An OTP authenticator device is a simple electronic device which is able to provide the customer with a random 6-digit hexadecimal number, used for authentication to an online platform (e.g., the bank system). 
The effectiveness of this devices depends on the secrecy of the initial seed with which the internal Linear Feedback Shift Register (LFSR) is loaded.
The LFSR is responsible of generating a sequence of random numbers.
The only exposed input pin of the circuit is the one used to turn on the display. 
Actually, we managed to unpack the device and find that there are hidden pins, inserted to test the circuit at the end of the production phase. 
Is there a way to control these pins and exfiltrate the 128-bit hardcoded seed by reading the fifth hidden pin?

The flag must be submitted in the form:

`CCIT{0xnnnn...}`

where n is an hexadecimal digit representing the 4 values assumed in a given 
clock cycle by the 4 hidden input pins, starting from RST going to S_IN.

E.g., the flag `CCIT{0x25ffa}` means that 5 clock cycle are used to exfiltrate the needed information, and the signals assume the following values:

```
RST   0 0 1 1 1  
INIT  0 1 1 1 0
N_T   1 0 1 1 1
S_IN  0 1 1 1 0
      2 5 f f a
```

NOTE: More than one flag is possible, as long as that sequence is able to exfiltrate the requested information.

Download: [OTP.zip](https://cyberchallenge.s3.eu-south-1.amazonaws.com/hardware/OTP.zip)
