# Assignment-3: TOPSIS Implementation, PyPI Package and Web Service

## Objective
The objective of this assignment is to implement the **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** algorithm and deploy it as:
1. A command-line Python program  
2. A Python package uploaded to PyPI  
3. A web service  

---

## Part I: TOPSIS Command Line Program

The TOPSIS algorithm ranks alternatives based on their distance from the ideal best and ideal worst solutions.

### Command Line Usage
```bash
python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>
```

### Example
```bash
python topsis.py data.csv "1,1,1,2,1" "+,+,-,+,-" result.csv
```

---

## Input File Format

- The input file must be a CSV file.
- The first column contains alternative names (non-numeric).
- All remaining columns contain numeric criteria values.

Example `data.csv`:
```csv
Fund Name,P1,P2,P3,P4,P5
M1,0.67,0.45,6.5,42.6,12.56
M2,0.60,0.36,3.5,53.3,14.47
M3,0.82,0.67,3.8,63.1,17.10
M4,0.60,0.36,3.5,69.2,18.42
```

---

## Output File Format

The output CSV file contains all original columns along with two additional columns:
- **Topsis Score**
- **Rank**

A higher Topsis Score indicates a better alternative.

---

## Validations Performed

- Correct number of command-line arguments
- Input file existence check
- Minimum of three columns in input file
- Numeric values in criteria columns
- Number of weights equals number of criteria
- Number of impacts equals number of criteria
- Impacts must be either `+` or `-`

---

## Part II: PyPI Package

The TOPSIS implementation is packaged and published on PyPI.

### Installation
```bash
pip install Topsis-Lakshay-102303872
```

### CLI Usage After Installation
```bash
topsis <InputDataFile> <Weights> <Impacts> <OutputResultFileName>
```

---

## Part III: Web Service

A web service interface is implemented to:
- Upload input CSV file
- Enter weights and impacts
- Provide an email address
- Compute TOPSIS ranking
- Send the result CSV to the provided email

---

## Author

Lakshay  
Roll Number: 102303872

---

## License

MIT License