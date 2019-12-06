#include <iostream>
#include "BMS.h"

void SelectComPort() //added function to find the present serial 
{

    TCHAR lpTargetPath[5000]; // buffer to store the path of the COMPORTS
    DWORD test;
    bool gotPort=0; // in case the port is not found

    for(int i=0; i<255; i++) // checking ports from COM0 to COM255
    {
        CString str;
        str.Format(_T("%d"),i);
        CString ComName=CString("COM") + CString(str); // converting to COM0, COM1, COM2

        test = QueryDosDevice(ComName, (LPSTR)lpTargetPath, 5000);

            // Test the return value and error if any
        if(test!=0) //QueryDosDevice returns zero if it didn't find an object
        {
            m_MyPort.AddString((CString)ComName); // add to the ComboBox
            gotPort=1; // found port
        }

        if(::GetLastError()==ERROR_INSUFFICIENT_BUFFER)
        {
            lpTargetPath[10000]; // in case the buffer got filled, increase size of the buffer.
            continue;
        }

    }

    if(!gotPort) // if not port
    m_MyPort.AddString((CString)"No Active Ports Found"); // to display error message incase no ports found

}

int main(void) {
	
	BMS("COM0", 9600);
	cout << "HELLO WORLD";
}