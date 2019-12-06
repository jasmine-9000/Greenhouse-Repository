#define CRC8INIT 0x00
#define CRC8POLY 0x31 // = X^8+X^5+X^4+X^0
					  // Because our BMS system uses a CRC8 polynomial from Dallas, our polynomial is 0x31 in hex.
/*
CRC8 algorithm implementation I found.
Going to explain it with comments.
See Ben Eater's video for a better tutorial than my comments on how CRC8 works.
https://eater.net/crc
https://www.youtube.com/watch?v=izG7qT0EpBw
*/


uint8_t crc8(uint8_t *data, uint16_t size)
{
	uint8_t crc, i;
    crc = CRC8INIT;
	
    while (size--)
    {
		// feed the next piece of data into the CRC8 value, and then increment the data pointer to move it.
        crc ^= *data++;
        for (i = 0; i < 8; i++)
        {
			// if the most significant bit is 1, then flip all of the bits that are in the polynomial, and shift it 1 bit to the left.
			// if the most significant bit is 0, then shift the crc8 value 1 to the left. 
			// do this for each bit in in each data piece you feed it.
			// if there's no 
            if (crc & 0x80) {
				crc = (crc << 1) ^ CRC8POLY;
			} 
            else {
				crc <<= 1;
			}
        }
    }

    return crc;
}

// 2 character number: XY. 
uint8_t crc8_from2Chars(char X, char Y)
{
	return (hex2int(X) << 4) ^ hex2int(Y);
};
uint8_t hex2int(char Z) {
	switch(Z) {
		case '0':
		case '1': 
		case '2': 
		case '3': 
		case '4': 
		case '5': 
		case '6': 
		case '7': 
		case '8':
		case '9':
			return (uint8_t) (Z - '0');
			break;
		case 'a':
		case 'A':
			return 10;
			break;
		case 'b':
		case 'B':
			return 11;
			break;
		case 'c':
		case 'C':
			return 12;
			break;
		case 'd':
		case 'D':
			return 13;
			break;
		case 'e':
		case 'E':
			return 14;
			break;
		case 'f':
		case 'F':
			return 15;
			break;
		default: 
			return 0;
			break;
	}
}