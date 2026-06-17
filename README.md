# 📊 School Dropout Prediction – Educational Management Support System

This project uses **Logistic Regression**, a Machine Learning algorithm, to predict the **risk of school dropout** based on students’ academic and behavior data.

The main goal is to help schools identify students who may leave school early, so teachers and staff can take actions before dropout happens.

This system does **not replace human decisions**. It works as a support tool to help educators make better decisions.

---

# 🎯 Project Goal

Create a predictive model that estimates the probability of student dropout using educational indicators.

The model analyzes information such as:

* Academic performance (grades)
* School attendance
* Number of absences
* Discipline records
* Teacher evaluation and recommendation

With this information, the system can detect students who may need additional support.

---

# 🧱 Project Structure

## 📥 Data Reading and Preparation

Input file:

`dados_alunos.xlsx`

Before training the model, the data goes through a preparation process.

### Data preprocessing steps:

### 1. Remove duplicate records

Duplicate student records are removed to avoid incorrect results.

### 2. Handle missing values

Empty or incomplete data is treated to improve model quality.

Examples:

* Fill missing values
* Remove incomplete rows when necessary

### 3. Standardize the dataset

Data is organized into a consistent format.

Examples:

* Same date format
* Numeric conversion
* Clean text values

---

## 🧮 Feature Creation

New variables are created from the original data to improve prediction quality.

Created features include:

### Average Grade

Calculates the student’s average academic performance.

### Attendance Percentage

Measures how often the student attends classes.

Formula:

Attendance (%) = Classes Attended ÷ Total Classes × 100

### Total Absences

Counts how many classes the student missed.

### Discipline Events

Counts behavior or discipline occurrences.

These variables help the model better understand student patterns.

---

## 📊 Student Statistics

After preparing the data, the system generates individual indicators for each student.

Examples of analysis:

* Student average performance
* Attendance level
* Number of absences
* Behavior indicators
* Risk comparison between students

This step creates a complete student profile.

---

# 🤖 Prediction Model

Algorithm used:

**Logistic Regression**

Why Logistic Regression?

* Easy to understand
* Fast training process
* Works well for classification problems
* Generates probability scores

Model output example:

* 0.10 → Low dropout risk
* 0.55 → Medium dropout risk
* 0.92 → High dropout risk

The final result shows the probability that a student may drop out.

---

# 📈 Model Evaluation

To measure model performance, the following metrics are used:

## Accuracy

Shows the percentage of correct predictions.

## Confusion Matrix

Displays:

* Correct predictions
* False alarms
* Missed predictions

## Precision

Measures how many predicted dropout cases were correct.

## Recall

Measures how many real dropout cases were detected.

## F1-Score

Balances Precision and Recall.

## AUC–ROC

Measures the model’s ability to separate students with low and high dropout risk.

Higher values indicate better model performance.

---

# 📉 Data Visualization

Charts are created to make the results easier to understand.

Visual analysis includes:

### Attendance vs Dropout

Shows how attendance affects dropout risk.

### Grades vs Dropout

Shows the relationship between academic performance and school dropout.

### Absence Analysis by Risk Group

Compares student groups with different dropout probabilities.

Visualizations help identify patterns and support decision-making.

---

# ⚙️ Requirements

Install the required libraries:

```bash
pip install pandas numpy matplotlib scikit-learn
```

Libraries used:

* pandas → data manipulation
* numpy → numerical operations
* matplotlib → charts and visualization
* scikit-learn → machine learning model

---

# 🚀 Expected Result

At the end of the project, the system will:

✔ Read and prepare student data
✔ Create educational indicators
✔ Train a Logistic Regression model
✔ Predict dropout probability
✔ Generate evaluation metrics
✔ Create charts for analysis

This project demonstrates how Machine Learning can support educational management and help schools act earlier to reduce dropout rates.
