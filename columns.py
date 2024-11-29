# Maps CSV cols to Data Sheet cols
from enum import Enum
import csv

required_admin_columns = {
    "id": "Registration ID",
    "vid": "Visit ID",
    "a_family_group": "Family Group",
    "a_reg_date": "Date",
    "a_queue_no": "Queue number",
    "a_name": "Name",
    "a_khmer_name": "Khmer name",
    "a_dob": "DOB",
    "a_age": "Age",
    "a_gender": "Gender",
    "a_village": "Village",
    "a_contact_no": "Contact No.",
    "a_pregnant": "Pregnant?",
    "a_last_menstrual_period": "If N or unsure, Last Menstrual Period",
    "a_drug_allergies": "Drug Allergies",
    "a_sent_to_id": "Sent to Infectious Disease?",
}
required_pastmedicalhistory_columns = {
    "pmh_tuberculosis": "Tuberculosis",
    "pmh_diabetes": "Diabetes",
    "pmh_hypertension": "Hypertension",
    "pmh_hyperlipidemia": "Hyperlipidemia",
    "pmh_chronic_joint_pains": "Chronic Joint Pains",
    "pmh_chronic_muscle_aches": "Chronic Muscle Aches",
    "pmh_std": "Sexually transmitted disease",
    "pmh_specified_stds": "If Y to STD, specify:",
    "pmh_others": "Others",
}
required_socialhistory_columns = {
    "sh_past_smoking_history": "Past smoking history",
    "sh_no_of_years": "If Y, no. of years",
    "sh_current_smoking_history": "Current smoking history",
    "sh_cigarettes_per_day": "If Y, how many cigarettes per day",
    "sh_alcohol_history": "Alcohol history",
    "sh_how_regular": "If Y, how regularly?",
}
required_vitalstatistics_columns = {
    "vs_temperature": "Temperature",
    "vs_spo2": "SpO2",
    "vs_systolic_bp1": "Systolic BP1",
    "vs_diastolic_bp1": "Diastolic BP1",
    "vs_systolic_bp2": "Systolic BP2",
    "vs_diastolic_bp2": "Diastolic BP2",
    "vs_avg_systolic_bp": "Avg Systolic BP",
    "vs_avg_diastolic_bp": "Avg Diastolic BP",
    "vs_hr1": "HR1",
    "vs_hr2": "HR2",
    "vs_avg_hr": "Avg HR",
    "vs_rand_blood_glucose_mmolL": "Random Blood Glucose (mmol/L)",
}
required_heightandweight_columns = {
    "haw_height": "Height (cm)",
    "haw_weight": "Weight (kg)",
    "haw_bmi": "BMI",
    "haw_bmi_analysis": "BMI Analysis",
    "haw_paeds_height": "Paeds: Height %",
    "haw_paeds_weight": "Paeds: Weight %",
}
required_visualacuity_columns = {
    "va_l_eye_vision": "L eye vision (6/)",
    "va_r_eye_vision": "R eye vision (6/)",
    "va_additional_intervention": "Additional Intervention",
}
required_fallrisk_columns = {
    "fr_history_of_fall": "History of fall within past 12 months",
    "fr_cognitive_status": "Cognitive status",
    "fr_continence_problems": "Continence problems",
    "fr_safety_awareness": "Safety Awareness",
    "fr_unsteadiness": "Unsteadiness when standing, transferring and/or walking",
}
required_dental_columns = {
    "d_clean_teeth_freq": "How many days per week do you clean your child’s teeth or supervise/monitor them brush with fluoride toothpaste twice a day?",
    "d_sugar_consume_freq": "On average, how many times daily does your child consume starch or sugar (food or drinks) between meals?",
    "d_past_year_decay": "Has anyone in the immediate family (including a caregiver) had tooth decay or lost a tooth from tooth decay in the past year?",
    "d_brush_teeth_pain": "Oral symptoms question: Does your child complain of tooth pain or bleeding gums when they brush their teeth?",
    "d_drink_other_water": "Does your child wake up to drink anything other than water throughout the night?",
    "d_dental_notes": "Dental notes?",
    "d_referral_needed": "Referral needed?",
    "d_dental_referral_loc": "Referral location?",
    "d_tooth_11": "Tooth11",
    "d_tooth_12": "Tooth12",
    "d_tooth_13": "Tooth13",
    "d_tooth_14": "Tooth14",
    "d_tooth_15": "Tooth15",
    "d_tooth_16": "Tooth16",
    "d_tooth_17": "Tooth17",
    "d_tooth_18": "Tooth18",
    "d_tooth_21": "Tooth21",
    "d_tooth_22": "Tooth22",
    "d_tooth_23": "Tooth23",
    "d_tooth_24": "Tooth24",
    "d_tooth_25": "Tooth25",
    "d_tooth_26": "Tooth26",
    "d_tooth_27": "Tooth27",
    "d_tooth_28": "Tooth28",
    "d_tooth_31": "Tooth31",
    "d_tooth_32": "Tooth32",
    "d_tooth_33": "Tooth33",
    "d_tooth_34": "Tooth34",
    "d_tooth_35": "Tooth35",
    "d_tooth_36": "Tooth36",
    "d_tooth_37": "Tooth37",
    "d_tooth_38": "Tooth38",
    "d_tooth_41": "Tooth41",
    "d_tooth_42": "Tooth42",
    "d_tooth_43": "Tooth43",
    "d_tooth_44": "Tooth44",
    "d_tooth_45": "Tooth45",
    "d_tooth_46": "Tooth46",
    "d_tooth_47": "Tooth47",
    "d_tooth_48": "Tooth48",
}
required_doctorsconsultation_columns = {
    "dc_well": "WELL",
    "dc_msk": "MSK",
    "dc_cvs": "CVS",
    "dc_respi": "Respi",
    "dc_gu": "GU",
    "dc_git": "GIT",
    "dc_eye": "EYE",
    "dc_derm": "DERM",
    "dc_others": "OTHERS",
    "dc_consultation_notes": "Consultation Notes",
    "dc_treatment": "Treatment",
    "dc_diagnosis": "Diagnosis",
    "dc_referral_needed": "Referral Needed?",
    "dc_referral_loc": "Referral Location",
    "dc_remarks": "Remarks (anything that doesn't fit)"
}
required_columns = {
    **required_admin_columns,
    **required_pastmedicalhistory_columns,
    **required_socialhistory_columns,
    **required_vitalstatistics_columns,
    **required_heightandweight_columns,
    **required_visualacuity_columns,
    **required_fallrisk_columns,
    **required_dental_columns,
    **required_doctorsconsultation_columns
}
# Print the length of each subhashmap
# print(f"Length of required_admin_columns: {len(required_admin_columns)}")
# print(f"Length of required_pastmedicalhistory_columns: {len(required_pastmedicalhistory_columns)}")
# print(f"Length of required_socialhistory_columns: {len(required_socialhistory_columns)}")
# print(f"Length of required_vitalstatistics_columns: {len(required_vitalstatistics_columns)}")
# print(f"Length of required_heightandweight_columns: {len(required_heightandweight_columns)}")
# print(f"Length of required_visualacuity_columns: {len(required_visualacuity_columns)}")
# print(f"Length of required_fallrisk_columns: {len(required_fallrisk_columns)}")
# print(f"Length of required_dental_columns: {len(required_dental_columns)}")
# print(f"Length of required_doctorsconsultation_columns: {len(required_doctorsconsultation_columns)}")
#
# print(len(required_columns))

### Maps columns to their column ranges for data validation
range_admin_columns = {
    "id": "A1:A1048576",
    "vid": "B1:B1048576",
    "a_family_group": "C1:C1048576",
    "a_reg_date": "D1:D1048576",
    "a_queue_no": "E1:E1048576",
    "a_name": "F1:F1048576",
    "a_khmer_name": "G1:G1048576",
    "a_dob": "H1:H1048576",
    "a_age": "I1:I1048576",
    "a_gender": "J1:J1048576",
    "a_village": "K1:K1048576",
    "a_contact_no": "L1:L1048576",
    "a_pregnant": "M1:M1048576",
    "a_last_menstrual_period": "N1:N1048576",
    "a_drug_allergies": "O1:O1048576",
    "a_sent_to_id": "P1:P1048576",
}
range_pastmedicalhistory_columns = {
    "pmh_tuberculosis": "Q1:Q1048576",
    "pmh_diabetes": "R1:R1048576",
    "pmh_hypertension": "S1:S1048576",
    "pmh_hyperlipidemia": "T1:T1048576",
    "pmh_chronic_joint_pains": "U1:U1048576",
    "pmh_chronic_muscle_aches": "V1:V1048576",
    "pmh_std": "W1:W1048576",
    "pmh_specified_stds": "X1:X1048576",
    "pmh_others": "Y1:Y1048576",
}
range_socialhistory_columns = {
    "sh_past_smoking_history": "Z1:Z1048576",
    "sh_no_of_years": "AA1:AA1048576",
    "sh_current_smoking_history": "AB1:AB1048576",
    "sh_cigarettes_per_day": "AC1:AC1048576",
    "sh_alcohol_history": "AD1:AD1048576",
    "sh_how_regular": "AE1:AE1048576",
}
range_vitalstatistics_columns = {
    "vs_temperature": "AF1:AF1048576",
    "vs_spo2": "AG1:AG1048576",
    "vs_systolic_bp1": "AH1:AH1048576",
    "vs_diastolic_bp1": "AI1:AI1048576",
    "vs_systolic_bp2": "AJ1:AJ1048576",
    "vs_diastolic_bp2": "AK1:AK1048576",
    "vs_avg_systolic_bp": "AL1:AL1048576",
    "vs_avg_diastolic_bp": "AM1:AM1048576",
    "vs_hr1": "AN1:AN1048576",
    "vs_hr2": "AO1:AO1048576",
    "vs_avg_hr": "AP1:AP1048576",
    "vs_rand_blood_glucose_mmolL": "AQ1:AQ1048576",
}
range_heightandweight_columns = {
    "haw_height": "AR1:AR1048576",
    "haw_weight": "AS1:AS1048576",
    "haw_bmi": "AT1:AT1048576",
    "haw_bmi_analysis": "AU1:AU1048576",
    "haw_paeds_height": "AV1:AV1048576",
    "haw_paeds_weight": "AW1:AW1048576",
}
range_visualacuity_columns = {
    "va_l_eye_vision": "AX1:AX1048576",
    "va_r_eye_vision": "AY1:AY1048576",
    "va_additional_intervention": "AZ1:AZ1048576",
}
range_fallrisk_columns = {
    "fr_history_of_fall": "BA1:BA1048576",
    "fr_cognitive_status": "BB1:BB1048576",
    "fr_continence_problems": "BC1:BC1048576",
    "fr_safety_awareness": "BD1:BD1048576",
    "fr_unsteadiness": "BE1:BE1048576",
}
range_dental_columns = {
    "d_clean_teeth_freq": "BF1:BF1048576",
    "d_sugar_consume_freq": "BG1:BG1048576",
    "d_past_year_decay": "BH1:BH1048576",
    "d_brush_teeth_pain": "BI1:BI1048576",
    "d_drink_other_water": "BJ1:BJ1048576",
    "d_dental_notes": "BK1:BK1048576",
    "d_referral_needed": "BL1:BL1048576",
    "d_dental_referral_loc": "BM1:BM1048576",
    "d_tooth_11": "BN1:BN1048576",
    "d_tooth_12": "BO1:BO1048576",
    "d_tooth_13": "BP1:BP1048576",
    "d_tooth_14": "BQ1:BQ1048576",
    "d_tooth_15": "BR1:BR1048576",
    "d_tooth_16": "BS1:BS1048576",
    "d_tooth_17": "BT1:BT1048576",
    "d_tooth_18": "BU1:BU1048576",
    "d_tooth_21": "BV1:BV1048576",
    "d_tooth_22": "BW1:BW1048576",
    "d_tooth_23": "BX1:BX1048576",
    "d_tooth_24": "BY1:BY1048576",
    "d_tooth_25": "BZ1:BZ1048576",
    "d_tooth_26": "CA1:CA1048576",
    "d_tooth_27": "CB1:CB1048576",
    "d_tooth_28": "CC1:CC1048576",
    "d_tooth_31": "CD1:CD1048576",
    "d_tooth_32": "CE1:CE1048576",
    "d_tooth_33": "CF1:CF1048576",
    "d_tooth_34": "CG1:CG1048576",
    "d_tooth_35": "CH1:CH1048576",
    "d_tooth_36": "CI1:CI1048576",
    "d_tooth_37": "CJ1:CJ1048576",
    "d_tooth_38": "CK1:CK1048576",
    "d_tooth_41": "CL1:CL1048576",
    "d_tooth_42": "CM1:CM1048576",
    "d_tooth_43": "CN1:CN1048576",
    "d_tooth_44": "CO1:CO1048576",
    "d_tooth_45": "CP1:CP1048576",
    "d_tooth_46": "CQ1:CQ1048576",
    "d_tooth_47": "CR1:CR1048576",
    "d_tooth_48": "CS1:CS1048576",
}
range_doctorsconsultation_columns = {
    "dc_well": "CT1:CT1048576",
    "dc_msk": "CU1:CU1048576",
    "dc_cvs": "CV1:CV1048576",
    "dc_respi": "CW1:CW1048576",
    "dc_gu": "CX1:CX1048576",
    "dc_git": "CY1:CY1048576",
    "dc_eye": "CZ1:CZ1048576",
    "dc_derm": "DA1:DA1048576",
    "dc_others": "DB1:DB1048576",
    "dc_consultation_notes": "DC1:DC1048576",
    "dc_treatment": "DD1:DD1048576",
    "dc_diagnosis": "DE1:DE1048576",
    "dc_referral_needed": "DF1:DF1048576",
    "dc_referral_loc": "DG1:DG1048576",
    "dc_remarks": "DH1:DH1048576",
}
range_columns = {
    **range_admin_columns,
    **range_pastmedicalhistory_columns,
    **range_socialhistory_columns,
    **range_vitalstatistics_columns,
    **range_heightandweight_columns,
    **range_visualacuity_columns,
    **range_fallrisk_columns,
    **range_dental_columns,
    **range_doctorsconsultation_columns
}

class DataType(Enum):
    INTEGER = "INTEGER"          # INTEGER
    TEXT = "TEXT"                # TEXT
    VARCHAR = "VARCHAR(1)"       # VARCHAR(1) M/F
    BOOLEAN = "BOOLEAN"          # BOOLEAN
    DATE = "DATE"                # DATE
    NUMERIC = "NUMERIC(5, 1)"    # NUMERIC(5, 1)
    BYTEA = "BYTEA"              # BYTEA

class FieldDescriptor:
    """
    Describes a field
    """
    def __init__(self, sql_name: str, go_name: str, json_name: str, datasheet_name: str, datatype: str, required: bool = False, datasheet_range: str = None):
        self.required = required                # Whether the field is required
        self.sql_name = sql_name                # SQL column name
        self.go_name = go_name                  # Go struct field name
        self.json_name = json_name              # JSON field name
        self.datasheet_name = datasheet_name    # DataSheet column name
        self.datatype = datatype                # Data type of the field (Loosely follows SQL type)
        self.datasheet_range = datasheet_range  # Range of the column in the datasheet

    def __repr__(self):
        return self.sql_name

class CategoryDescriptor:
    """
    Describes a Category
    """
    def __init__(self, name: str, fields: list):
        self.name = name
        self.fields = fields  # fields is expected to be a list of Field objects

    def __repr__(self):
        return self.name

class Types:
    def __init__(self, csv_path: str):
        self.categories = []
        self._load_from_csv(csv_path)

    def _load_from_csv(self, csv_path: str):
        # Dictionary to store category-to-fields mapping
        category_map = {}

        with open(csv_path, mode="r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Extract data for the field
                category = row["Category Dropdown"]
                sql_name = row["SQL Name"]
                go_name = row["Go Name"]
                json_name = row["JSON Name"]
                datasheet_name = row["Datasheet Name"]
                datatype = row["Data Type"]
                required = row["Required"].strip().upper() == "TRUE"

                # Create a FieldDescriptor
                field = FieldDescriptor(
                    sql_name=sql_name,
                    go_name=go_name,
                    json_name=json_name,
                    datasheet_name=datasheet_name,
                    datatype=datatype,
                    required=required
                )

                # Add the field to the appropriate category
                if category not in category_map:
                    category_map[category] = []
                category_map[category].append(field)

        # Convert category_map to CategoryDescriptors
        for category, fields in category_map.items():
            self.categories.append(CategoryDescriptor(name=category, fields=fields))

    def __repr__(self):
        return f"Types(categories={self.categories})"

if __name__ == "__main__":
    types = Types("types.csv")

    # Print header with increased padding
    print(f"{'Category':<25} {'Field':<30} {'DataType':<25} {'Required':<10}")
    print("=" * 90)

    for category in types.categories:
        for field in category.fields:
            print(f"{category.name:<25} {field.sql_name:<30} {field.datatype:<25} {str(field.required):<10}")

