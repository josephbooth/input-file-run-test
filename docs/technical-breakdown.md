# **ACS Table Rendering Tester - Technical Documentation**  

## **Overview**  
The ACS Table Rendering Tester automates the process of verifying whether ACS tables successfully render on `data.census.gov`. Instead of manually checking each table and geography combination, the program:  
- **Reads test cases from an input file** (`test_cases.csv` or `test_cases.json`).  
- **Generates valid `data.census.gov` URLs** for testing.  
- **Opens each URL in a browser** to check if the table renders.  
- **Records the results** in an output file for review.  

This approach eliminates API dependencies and enables users to quickly test multiple geographies and tables with minimal effort.   

---

## **1. Input File Handling**  

### **Input File Format**  
The program accepts input files in **CSV or JSON format**, containing test cases structured as follows:  

| Column | Description | Example |
|--------|------------|---------|
| `dataYear` | The ACS data year being tested | `2023` |
| `dataset` | The dataset type (`acs1` or `acs5`) | `acs1` |
| `tableGroup` | The table group ID (from Census API) | `B01001` |
| `geographyID` | The formatted geography identifier | `050XX00US18039` |

### **Example CSV Input File (`test_cases.csv`)**  

dataYear,dataset,tableGroup,geographyID  
2023,acs1,B01001,050XX00US18039  
2023,acs1,DP02,160XX00US0410670  
2023,acs5,S0101,010XX00US  

### **Example JSON Input File (`test_cases.json`)**  

[  
    {"dataYear": "2023", "dataset": "acs1", "tableGroup": "B01001", "geographyID": "050XX00US18039"},  
    {"dataYear": "2023", "dataset": "acs1", "tableGroup": "DP02", "geographyID": "160XX00US0410670"},  
    {"dataYear": "2023", "dataset": "acs5", "tableGroup": "S0101", "geographyID": "010XX00US"}  
]  

### **Handling the Input File**  
- The program **validates the input file** to ensure all required fields are present.  
- If an error is found, the program **alerts the user and exits** instead of running invalid tests.  
- Users can **reuse existing test case files** for repeated test runs without re-entering data.  

---

## **2. Generating data.census.gov URLs**  

### **URL Construction Logic**  
The program dynamically generates URLs using the following structure:  

https://data.census.gov/table/{datasetPrefix}{dataYear}.{tableGroup}?g={geographyID}&tid={datasetPrefix}{dataYear}.{tableGroup}  

| URL Component | Value Source | Example |
|--------------|-------------|---------|
| `{datasetPrefix}` | Derived from dataset type (`acs1`, `acs5`) | `ACSDT1Y`, `ACSDP1Y`, `ACSST1Y` |
| `{dataYear}` | Provided in input file | `2023` |
| `{tableGroup}` | From input file | `B01001`, `DP02` |
| `{geographyID}` | From input file | `050XX00US18039` |

### **Example Generated URLs**  
- **Detailed Tables Test**:  
  https://data.census.gov/table/ACSDT1Y2023.B01001?g=050XX00US18039&tid=ACSDT1Y2023.B01001  
- **Data Profiles Test**:  
  https://data.census.gov/table/ACSDP1Y2023.DP02?g=160XX00US0410670&tid=ACSDP1Y2023.DP02  
- **Subject Tables Test**:  
  https://data.census.gov/table/ACSST5Y2023.S0101?g=010XX00US&tid=ACSST5Y2023.S0101  

### **Validation & Error Handling**  
- If an invalid geography ID or table group is detected, the program **skips that test case** and logs the issue.  
- Ensures the **correct dataset prefix** is used based on `acs1` or `acs5`.  

---

## **3. Running Tests & Checking Table Rendering**  

### **Execution Process**  
1. **For each test case, open the generated URL** in a browser.  
2. **Check if the table successfully renders**:  
   - Detect expected table elements.  
   - Look for error messages (e.g., "Table not found").  
3. **Log the result** as successful or failed.  

### **Testing Methods**  
- **Standard Browser Execution**: Open each URL manually or via an automated script.  
- **Headless Browser Automation** (optional): Use a tool like Selenium to check rendering without opening a visible browser.  

### **Timeout & Error Handling**  
- If a page takes too long to load, **set a timeout** and mark it as a failure.  
- Handle unexpected redirects or missing content gracefully.  

---

## **4. Recording Test Results**  

### **Output File Formats**  
Test results are stored in **CSV, JSON, and optional HTML format**.  

#### **Example CSV Output (`test_results.csv`)**  

dataYear,dataset,tableGroup,geographyID,url,result  
2023,acs1,B01001,050XX00US18039,https://data.census.gov/table/ACSDT1Y2023.B01001?g=050XX00US18039,Success  
2023,acs1,DP02,160XX00US0410670,https://data.census.gov/table/ACSDP1Y2023.DP02?g=160XX00US0410670,Failure  

#### **Example JSON Output (`test_results.json`)**  

[  
    {  
        "dataYear": "2023",  
        "dataset": "acs1",  
        "tableGroup": "B01001",  
        "geographyID": "050XX00US18039",  
        "url": "https://data.census.gov/table/ACSDT1Y2023.B01001?g=050XX00US18039",  
        "result": "Success"  
    },  
    {  
        "dataYear": "2023",  
        "dataset": "acs1",  
        "tableGroup": "DP02",  
        "geographyID": "160XX00US0410670",  
        "url": "https://data.census.gov/table/ACSDP1Y2023.DP02?g=160XX00US0410670",  
        "result": "Failure"  
    }  
]  

### **Summary Report**  
At the end of execution, the program provides:  
- **Total test cases executed**  
- **Number of successful vs. failed tests**  
- **A log of failed test cases for troubleshooting**  

---

## **5. Execution & User Interface**  

### **CLI-Based Execution**  
- The program runs as a **command-line tool**.  
- Displays **real-time progress** as test cases are processed:  

  [1/50] Testing table B01001 for geography 050XX00US18039... Success!  
  [2/50] Testing table DP02 for geography 160XX00US0410670... Failure!  

### **User Options**  
- Users can specify command-line options for:  
  - **Custom input file** (`--input test_cases.csv`)  
  - **Output format** (`--output-format json`)  
  - **Enable headless browser mode** (`--headless true`)  
  - **Set a timeout for page loads** (`--timeout 10`)  

### **Error Handling & Recovery**  
- If a test case **fails due to a connection issue**, the program retries up to a set number of times (`--retries 3`).  
- If the input file is **incorrectly formatted**, an error message is displayed and execution is halted.  
- If a test case **fails due to an invalid geography or table ID**, the issue is logged, and execution continues.  

---

## **6. Future Enhancements**  

To improve usability, a **browser-based user interface** may be developed in future versions. This would:  

- Provide an **interactive interface** for users to upload input files, start tests, and view results.  
- Display **real-time test progress** in a web-based dashboard.  
- Allow users to **filter and analyze test results** directly in the browser.  
- Enable **exporting reports** in multiple formats (CSV, JSON, or HTML).  

This UI would make the tool more accessible to users who prefer a **visual, point-and-click** experience instead of a command-line interface.  
    
  
