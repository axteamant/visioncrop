call conda activate tesseract
REM set /p screen=Inserisci quale schermo usare : 
REM if not defined screen set "screen=0"
set screen=0
set /p file=Inserisci il file output :
if not defined file set "file=out.txt"
set /p half=metà schermo (sinistra)? (1 = true, 0 = false default = 0 ) :
if not defined half set "half=0"
call python ./tesseract.py --screen %screen% --file %file% --half %half%