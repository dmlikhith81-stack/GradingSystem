# Grading System (Streamlit App)

A data-driven web application that performs **relative grading using normal distribution (Z-score normalization)** and provides **interactive analytics & visualization**.

Built using:

- Python 
- Streamlit 
- Pandas 
- NumPy 
- Matplotlib 

---

## Features

### 1. File Upload

- Supports both **CSV** and **Excel (.xlsx)** files
- Automatically loads and previews dataset

### 2. Column-Based Grading

- Select any subject/column dynamically
- Works for multi-subject datasets

### 3. Relative Grading (Z-score Based)

- Computes:

  - Mean (μ)
  - Standard deviation (σ)
  - Z-score normalization

- Assigns grades based on distribution:

| Z-score Range | Grade |
| ------------- | ----- |
| ≥ 1.5         | A+    |
| 1.0 – 1.5     | A     |
| 0.5 – 1.0     | B+    |
| 0 – 0.5       | B     |
| -0.5 – 0      | C     |
| -1.0 – -0.5   | D     |
| < -1.0        | F     |

---

### 4. Max Marks Normalization

- User-defined **maximum marks input**
- Scales dataset accordingly before grading

---

### 5. Data Visualization

The app generates:

- Marks Distribution
- Grade Distribution
---

### 6. Download Results

- Export graded dataset as **CSV**
- Includes:

  - Normalized Marks
  - Z-score
  - Assigned Grade

---

## How It Works

The system uses **Z-score normalization**:

[
Z = \frac{X - \mu}{\sigma}
]

Where:

- (X) = student's marks
- (\mu) = mean marks
- (\sigma) = standard deviation

This converts raw scores into a **relative performance scale**.

---

## Project Structure

```
relative-grading-system/
│
├── main.py              # Main Streamlit application
├── sample data/ sample_data.csv     # Sample dataset
├── README.md           # Project documentation
└── requirements.txt    # Dependencies
```

---

## Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/GradingSystem
cd gradingsystem
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Application

```bash
streamlit run app.py
```

---

## Sample Input Format

```csv
Student_ID,Name,Maths,Physics,Chemistry
101,Aarav,78,82,75
102,Diya,92,89,94
```

---

## Limitations

- Assumes **approximately normal distribution**
- Performance may degrade with:

  - Small datasets
  - Highly skewed marks
  - Extreme outliers

In such cases, **percentile-based grading** is recommended.

---

## Future Improvements

* Multi-column grading (all subjects at once)
* Custom grade boundaries (UI sliders)
* Percentile-based grading system
* Gaussian curve overlay on histogram
* Student performance dashboard
* Deployment on Streamlit Cloud

---




