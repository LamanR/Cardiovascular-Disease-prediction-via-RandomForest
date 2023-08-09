# Getting know the data
SELECT * FROM cardio;

# Look for duplicates:
SELECT COUNT(*) AS duplicate_count
FROM cardio
GROUP BY id
HAVING COUNT(*) > 1;
-- No duplicates

# Look for na/null values
SELECT count(*)
FROM cardio
WHERE
  id IS NULL OR
  age IS NULL OR
  gender IS NULL OR
  height IS NULL OR
  weight IS NULL OR
  ap_hi IS NULL OR
  ap_lo IS NULL OR
  cholesterol IS NULL OR
  gluc IS NULL OR
  smoke IS NULL OR
  alco IS NULL OR
  active IS NULL OR
  cardio IS NULL;
-- No null values

# age column is in days, to change it add column age_years also additional bmi column for further purposes
ALTER TABLE cardio
ADD COLUMN age_years INT,
ADD COLUMN bmi FLOAT;

# Updating data by finding age in years and bmi
UPDATE cardio
SET age_years = FLOOR(age / 365.25),
    bmi = ROUND(weight / ((height / 100) * (height / 100)), 2);

# Count the number of men and women
SELECT gender, COUNT(*) AS count_gender
FROM cardio
GROUP BY gender;

# Calculate the mean of age_years, height, weight and pressure per gender
SELECT
    gender,
    AVG(age_years) AS avg_age_years,
    AVG(height) AS avg_height,
    AVG(weight) AS avg_weight,
    AVG(ap_hi) AS avg_ap_hi,
    AVG(ap_lo) AS avg_ap_lo
FROM cardio
GROUP BY gender;

# Find min and max values of age, height, weight and pressure columns
SELECT 
	MIN(age_years) AS min_age, MAX(age_years) AS max_age,
	MIN(height) AS min_height, MAX(height) AS max_height,
	MIN(weight) AS min_weight, MAX(weight) AS max_weight,
    MIN(ap_hi) AS min_ap_hi, MAX(ap_hi) AS max_ap_hi,
    MIN(ap_lo) AS min_ap_lo, MAX(ap_lo) AS max_ap_lo
FROM cardio;

-- See that min weight is 10, however min age is 29 it has to be error
-- Also max height is 250 and max weight is 200, they could be outliers
-- We would deal with them in Python
-- Min ap_lo and ap_hi is negative they are errors
-- Max ap_hi is 16020 is an error

# Systolic pressure should always be greater than diastolic one
# Look if there rows where systolic is lower than diastolic 
SELECT COUNT(*) 
FROM cardio
WHERE ap_lo > ap_hi;
-- There are 1234 inaccurate rows, let's delete them

DELETE FROM cardio
WHERE ap_lo > ap_hi OR ap_lo < 0 or ap_hi < 0;

# Drop id and age columns 
ALTER TABLE cardio
DROP COLUMN id,
DROP COLUMN age;




