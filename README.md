# LED HARP

For the final project we combined our love of music with our love of physics and engineering to
design and create a 5 stringed LED harp. The LED harp is meant to mock an ordinary harp
except instead of depending on string vibrations, our project uses a modulated light signal and
sensors to produce sound. We used a small single board computer (Raspberry Pi) and an analog
to digital converter (MCP3008) to monitor the output voltage of five photodetectors (OP805SL) designed with individual bandpass filters set to detect the individual light signals emitted by the
LED’s. In turn, the LEDs are driven by relaxation oscillator such that the light signal is emitted
at certain frequencies to account for the dispersion of light.

