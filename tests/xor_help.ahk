
WinWait, Test_Vector_s_E.xlsx - Saved, 
IfWinNotActive, Test_Vector_s_E.xlsx - Saved, , WinActivate, Test_Vector_s_E.xlsx - Saved, 
WinWaitActive, Test_Vector_s_E.xlsx - Saved, 
Send, {CTRLDOWN}c{CTRLUP}{Right 1}
sleep, 100

WinWait, Boolean Logic Simplificator - Boole Calculator - Online Software Tool - Google Chrome, 
IfWinNotActive, Boolean Logic Simplificator - Boole Calculator - Online Software Tool - Google Chrome, , WinActivate, Boolean Logic Simplificator - Boole Calculator - Online Software Tool - Google Chrome, 
WinWaitActive, Boolean Logic Simplificator - Boole Calculator - Online Software Tool - Google Chrome, 
send, {Home}
sleep, 300
send, {Home}
sleep, 300
MouseClick, left,  600,  560
Sleep, 100
Send, {TAB}{CTRLDOWN}v{CTRLUP}{ENTER}
