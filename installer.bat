
rem call curl  -o tesseract-ocr-w64-setup-5.3.3.20231005.exe https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe
rem call tesseract-ocr-w64-setup-5.3.3.20231005.exe
call curl -o Miniconda3-latest-Windows-x86_64.exe https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
call Miniconda3-latest-Windows-x86_64.exe
call conda create -n  tesseract python=3.9 
call conda activate tesseract
call pip install -r env.txt