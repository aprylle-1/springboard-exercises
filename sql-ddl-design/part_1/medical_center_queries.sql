-----------------EXERCISES------------------------

---1. Select all the patients(concat first and last name, label as patient) and their corresponding doctors (concat first and last name, label as doctor)

SELECT concat(p.first_name,' ',p.last_name) as patient,
concat(d.first_name, ' ', d.last_name) as doctor
FROM patient_doctor pd
JOIN patients p
ON pd.patient_id = p.id
JOIN doctors d
ON pd.doctor_id = d.id
ORDER BY patient, doctor;

---2. Select all patient records and count how many doctors they have. Order by number of doctors ASC, then patient name

SELECT concat(p.first_name, ' ', p.last_name) as patient, COUNT(*) as doctor_count
FROM patient_doctor pd
JOIN patients p
ON pd.patient_id = p.id
GROUP BY patient
ORDER BY doctor_count, patient;

---3. Select all patient records and their corresponding diseases -----

SELECT concat(p.first_name, ' ', p.last_name) as patient, disease_name
FROM patient_diseases pdi
JOIN patients p
ON pdi.patient_id = p.id
JOIN diseases d
ON pdi.disease_id = d.id
ORDER BY patient, disease_name;

---. Select all patient records and count how many diseases they have. Order by number of diseases, then patient name

SELECT concat(p.first_name, ' ', p.last_name) as patient, COUNT(*) as diseases_count
FROM patient_diseases pdi
JOIN patients p
ON pdi.patient_id = p.id
JOIN diseases d 
ON d.id = pdi.disease_id
GROUP BY patient
ORDER BY diseases_count, patient;