# MLflow-project-template
MLflow project template

## STEPS -

### STEP 01- Create a repository by using template repository

### STEP 02- Clone the new repository

### STEP 03- Create a conda environment after opening the repository in VSCODE

```bash
conda create --prefix ./env python=3.7 -y
```

```bash
conda activate ./env
```
OR
```bash
source activate ./env
```

### STEP 04- install the requirements
```bash
pip install -r requirements.txt
```

### STEP 05 - Create conda.yaml file -
```bash
conda env export > conda.yaml
```

### STEP 06- commit and push the changes to the remote repository

=================== **Explaination** ===============================

Flask app to predict item sales based on these factors (Item Weight,Item Fat Content,Item Visibility,Item Type,Item MRP,Outlet Size,Outlet Location Type,Outlet Type)

we create a full fledged MLops pipeline to smoothen the process and defined all individual layer. We have data in cassandra database we take the data and store in
pandas dataframe for further process

We create 7 seprate stages for each step.....

1) Get data from cassandra database
 
2) Handling missing values in data with drop and mode
 
3) Feature transformation as naming less frequent Item_Type as others and drop useless columns
 
4) Train 80% of data and rest 20% for testing 
 
5) Here we define pipeline and column transform and do all the preprocessing of data before training them as encode them impute missing values and then train
	using GradientBoosting Regressor algorithm 
  
6) Tuning hyperparameters of GradientBoosting model pipeline using Randomized Search Cross-Validation
  
7) create the final pipeline for prediction and dump using joblib file
 
We also consider the situation if we stuck anywhere by creating log files for each and every steps for each stage
