import pandas as pd

def process_hospitals(df: pd.DataFrame) -> pd.DataFrame:
        
        """Process hospital-specific data, extract relevant columns, and add accepted insurance information."""
        hospitals_df = df[['OSHPD_ID', 'FacilityName', 'FacilityType', 'Address', 'Address2', 'City', 'State',
            'ZIP', 'county', 'FACILITY_LEVEL_DESC', 'TOTAL_NUMBER_BEDS', 
            'ER_SERVICE_LEVEL_DESC', 'FACILITY_STATUS_DESC', 'LICENSE_TYPE_DESC', 'LICENSE_CATEGORY_DESC']]

        df_cleaned = hospitals_df.drop_duplicates(subset=['FacilityName', 'FacilityType', 'Address', 'ZIP'], keep='first')
        df_cleaned = df_cleaned.drop_duplicates(subset=['OSHPD_ID'], keep='first')
        
        return df_cleaned

def process_taxonomy(df: pd.DataFrame) -> pd.DataFrame:
        taxonomy_df = df[['PROVIDER TAXONOMY CODE', 'MEDICARE PROVIDER/SUPPLIER TYPE DESCRIPTION', 
                'PROVIDER TAXONOMY DESCRIPTION:  TYPE, CLASSIFICATION, SPECIALIZATION', 'MEDICARE SPECIALTY CODE']]

        df_cleaned = taxonomy_df.drop_duplicates(subset=['PROVIDER TAXONOMY CODE'], keep='first')

        return df_cleaned

def process_ratings(df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(columns={"OSHPDID": "OSHPD_ID"})
        ratings_df = df[['OSHPD_ID', 'Performance Measure', '# of Adverse Events',
                        '# of Cases', 'Risk-adjusted Rate', 'Hospital Ratings']]
        
        return ratings_df

def save_to_csv(df: pd.DataFrame, filename: str):
        """Save the processed DataFrame to a CSV file."""
        print("inside save_to_csv() method")
        df.to_csv(filename, index=False)

if __name__ == "__main__":
        
        final_hospitals_data = pd.read_csv('hospitals_cleaned.csv')        
        final_hospitals_data = process_hospitals(final_hospitals_data)
        print(final_hospitals_data['OSHPD_ID'].is_unique)
        save_to_csv(final_hospitals_data, 'final_hospitals_data.csv')

# Load the doctors and hospitals datasets
        doctors_df = pd.read_csv("doctors_output.csv")
        hospitals_df = pd.read_csv("final_hospitals_data.csv")

# Merge doctors_df with hospitals_df to get 'OSHPD_ID' based on 'FacilityName'
        doctors_updated = doctors_df.merge(hospitals_df[['FacilityName', 'OSHPD_ID']], 
                                   on='FacilityName', how='left')

# Drop 'FacilityName' column
        doctors_updated['OSHPD_ID'].replace("", pd.NA, inplace=True)
        doctors_updated = doctors_updated.dropna(subset=['OSHPD_ID'])
        doctors_updated = doctors_updated.drop(columns=['FacilityName'])

        print("Updated doctors.csv with OSHPD_ID and removed FacilityName.")
        doctors_updated = pd.read_csv("final_doctors_data_before_cleaning.csv")

# Define a dictionary for replacement values
        replacement_dict = {'B': 'Both', 'N': 'No', 'O': 'Only'}

# Apply the replacement to the two specific columns
        doctors_updated[['SeesChildren', 'Telehealth']] = df[['SeesChildren', 'Telehealth']].replace(replacement_dict)

# Save the updated DataFrame
        doctors_updated.to_csv("final_doctors_data.csv", index=False)


        taxonomy_df = pd.read_csv("taxonomy.csv")
        final_taxonomy_data = process_taxonomy(taxonomy_df)
        final_taxonomy_data.to_csv("final_taxonomy_data.csv", index=False)


        df = pd.read_csv("hospital_ratings.csv", encoding="ISO-8859-1")
        final_hospital_ratings_data = process_ratings(df)
        final_hospital_ratings_data.to_csv("final_hospital_ratings_data.csv", index=False)