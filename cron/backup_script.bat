@echo off
REM Set PostgreSQL connection parameters
set PGHOST=localhost
set PGUSER=jieqiboh       REM Replace with your PostgreSQL username
set PGPASSWORD=postgres   REM Replace with your PostgreSQL password
set PGDATABASE=patients   REM Replace with your database name

REM Generate timestamp
for /f "tokens=2 delims==" %%I in ('"wmic os get localdatetime /value"') do set datetime=%%I
set TIMESTAMP=%datetime:~0,4%%datetime:~4,2%%datetime:~6,2%_%datetime:~8,2%%datetime:~10,2%%datetime:~12,2%

REM Define output path
set OUTPUT_PATH=C:\path\to\backups\%TIMESTAMP%_patientdata.csv REM Replace with the desired path for the output CSV file

REM Run the PostgreSQL query to export data to CSV
psql -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "\COPY (
SELECT
    a.id,
    a.vid,
    a.family_group AS a_family_group,
    a.reg_date AS a_reg_date,
    a.queue_no AS a_queue_no,
		a.name AS a_name,
		a.khmer_name AS a_khmer_name,
		a.dob AS a_dob,
		a.age AS a_age,
		a.gender AS a_gender,
		a.village AS a_village,
		a.contact_no AS a_contact_no,
		a.pregnant AS a_pregnant,
		a.last_menstrual_period AS a_last_menstrual_period,
		a.drug_allergies AS a_drug_allergies,
		a.sent_to_id AS a_sent_to_id,
		pmh.tuberculosis AS pmh_tuberculosis,
		pmh.diabetes AS pmh_diabetes,
		pmh.hypertension AS pmh_hypertension,
		pmh.hyperlipidemia AS pmh_hyperlipidemia,
		pmh.chronic_joint_pains AS pmh_chronic_joint_pains,
		pmh.chronic_muscle_aches AS pmh_chronic_muscle_aches,
		pmh.sexually_transmitted_disease AS pmh_sexually_transmitted_disease,
		pmh.specified_stds AS pmh_specified_stds,
		pmh.others AS pmh_others,
		sh.past_smoking_history AS sh_past_smoking_history,
		sh.no_of_years AS sh_no_of_years,
		sh.current_smoking_history AS sh_current_smoking_history,
		sh.cigarettes_per_day AS sh_cigarettes_per_day,
		sh.alcohol_history AS sh_alcohol_history,
		sh.how_regular AS sh_how_regular,
		vs.temperature AS vs_temperature,
		vs.spo2 AS vs_spo2,
		vs.systolic_bp1 AS vs_systolic_bp1,
		vs.diastolic_bp1 AS vs_diastolic_bp1,
		vs.systolic_bp2 AS vs_systolic_bp2,
		vs.diastolic_bp2 AS vs_diastolic_bp2,
		vs.avg_systolic_bp AS vs_avg_systolic_bp,
		vs.avg_diastolic_bp AS vs_avg_diastolic_bp,
		vs.hr1 AS vs_hr1,
		vs.hr2 AS vs_hr2,
		vs.avg_hr AS vs_avg_hr,
		vs.rand_blood_glucose_mmolL AS vs_rand_blood_glucose_mmoll,
    haw.height AS haw_height,
    haw.weight AS haw_weight,
    haw.bmi AS haw_bmi,
    haw.bmi_analysis AS haw_bmi_analysis,
    haw.paeds_height AS haw_paeds_height,
    haw.paeds_weight AS haw_paeds_weight,
    va.l_eye_vision AS va_l_eye_vision,
    va.r_eye_vision AS va_r_eye_vision,
    va.additional_intervention AS va_additional_intervention,
    d.clean_teeth_freq AS d_clean_teeth_freq,
    d.sugar_consume_freq AS d_sugar_consume_freq,
    d.past_year_decay AS d_past_year_decay,
    d.brush_teeth_pain AS d_brush_teeth_pain,
    d.drink_other_water AS d_drink_other_water,
    d.dental_notes AS d_dental_notes,
    d.referral_needed AS d_referral_needed,
    d.referral_loc AS d_referral_loc,
    d.tooth_11 AS d_tooth_11,
    d.tooth_12 AS d_tooth_12,
    d.tooth_13 AS d_tooth_13,
    d.tooth_14 AS d_tooth_14,
    d.tooth_15 AS d_tooth_15,
    d.tooth_16 AS d_tooth_16,
    d.tooth_17 AS d_tooth_17,
    d.tooth_18 AS d_tooth_18,
    d.tooth_21 AS d_tooth_21,
    d.tooth_22 AS d_tooth_22,
    d.tooth_23 AS d_tooth_23,
    d.tooth_24 AS d_tooth_24,
    d.tooth_25 AS d_tooth_25,
    d.tooth_26 AS d_tooth_26,
    d.tooth_27 AS d_tooth_27,
    d.tooth_28 AS d_tooth_28,
    d.tooth_31 AS d_tooth_31,
    d.tooth_32 AS d_tooth_32,
    d.tooth_33 AS d_tooth_33,
    d.tooth_34 AS d_tooth_34,
    d.tooth_35 AS d_tooth_35,
    d.tooth_36 AS d_tooth_36,
    d.tooth_37 AS d_tooth_37,
    d.tooth_38 AS d_tooth_38,
    d.tooth_41 AS d_tooth_41,
    d.tooth_42 AS d_tooth_42,
    d.tooth_43 AS d_tooth_43,
    d.tooth_44 AS d_tooth_44,
    d.tooth_45 AS d_tooth_45,
    d.tooth_46 AS d_tooth_46,
    d.tooth_47 AS d_tooth_47,
    d.tooth_48 AS d_tooth_48,
    fr.fall_worries AS fr_fall_worries,
    fr.fall_history AS fr_fall_history,
    fr.cognitive_status AS fr_cognitive_status,
    fr.continence_problems AS fr_continence_problems,
    fr.safety_awareness AS fr_safety_awareness,
    fr.unsteadiness AS fr_unsteadiness,
    fr.fall_risk_score AS fr_fall_risk_score,
    dc.well AS dc_well,
    dc.msk AS dc_msk,
    dc.cvs AS dc_cvs,
    dc.respi AS dc_respi,
    dc.gu AS dc_gu,
    dc.git AS dc_git,
    dc.eye AS dc_eye,
    dc.derm AS dc_derm,
    dc.others AS dc_others,
    dc.consultation_notes AS dc_consultation_notes,
    dc.diagnosis AS dc_diagnosis,
    dc.treatment AS dc_treatment,
    dc.referral_needed AS dc_referral_needed,
    dc.referral_loc AS dc_referral_loc,
    dc.remarks AS dc_remarks,
    NULL AS a_photo
    FROM admin a
    LEFT JOIN pastmedicalhistory pmh ON a.id = pmh.id AND a.vid = pmh.vid
    LEFT JOIN socialhistory sh ON a.id = sh.id AND a.vid = sh.vid
    LEFT JOIN vitalstatistics vs ON a.id = vs.id AND a.vid = vs.vid
    LEFT JOIN heightandweight haw ON a.id = haw.id AND a.vid = haw.vid
    LEFT JOIN visualacuity va ON a.id = va.id AND a.vid = va.vid
    LEFT JOIN dental d ON a.id = d.id AND a.vid = d.vid
    LEFT JOIN fallrisk fr ON a.id = fr.id AND a.vid = fr.vid
    LEFT JOIN doctorsconsultation dc ON a.id = dc.id AND a.vid = dc.vid
) TO '%OUTPUT_PATH%' WITH CSV HEADER;"
