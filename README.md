# News Comparison with Real-time Data Crawling

<b>Description:</b>
This is the final project for data mining course [CSCI 4502], it is consists of 2 parts:
  1. data crawling (retrieve articles from specified websites)
  2. data analysis (use several algorithms to analysis the relation between data)
  
 <b>Run:</b>
  1. Automation.py (at least Windows 7 SP1 x64 with Visual C++ 2015 patch)<br/>
    a. crawl articles through Google Chrome<br/>
    b. store articles under "result" directory as the form of json file<br/>
    c. file name is unique; the sha256 value of the "article identity," which is the combination of the article name and link<br/>
    
  2. json_to_csv.py<br/>
    a. combine all articles under each News category into a single csv file for further data analysis<br/>
    b. csvs are stored under "result_csv" directory<br/>
    
  3. article_analysis.py<br/>
    a. read the csv files from "result_csv" directory<br/>
    b. analysis articles and generate graphs under "result_img" directory<br/>
    
 <b>Dependencies:</b> (may required to install through pip command)
  1. Python Library for article_analysis.py<br/>
    a. pandas<br/>
    b. mlxtend<br/>
    c. matplotlib<br/>
    d. numpy<br/>
    e. sklearn<br/>
    
  2. Python Library for Automation.py<br/>
    a. selenium<br/>
    b. pytest-shutil<br/>
    c. csv<br/>
    d. pywin32<br/>
    e. typing<br/>
    
   3. Browser<br/>
    a. The entire binary executable Google Chrome under "C:\chrome\chrome.exe"<br/>
    b. ChromeDriver, which is included under "Tools\Chrome_Driver" directory<br/>
    c. Chrome version "76.0.3809.100" and ChromeDriver version "76.0.3809.126" are required for stable running<br/>
