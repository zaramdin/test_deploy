from flask import Flask, request, jsonify
import pandas as pd
from g4f.client import Client
import json
app = Flask(__name__)

# Load the CSV file
csv_file_path = 'sales_performance_data.csv'  # Update with your CSV file path
data = pd.read_csv(csv_file_path)

# Ensure 'dated' column is in datetime format
data['dated'] = pd.to_datetime(data['dated'])

@app.route('/analyze', methods=['GET'])
def analyze_performance():
    input_type = request.args.get('input_type')
    
    if not input_type:
        return jsonify({"error": "Input type is required"}), 400
    
    input_type = input_type.strip().lower()

    if input_type == "team_performance":
        # Overall team performance
        key_metrics = {
            "Total Tours Booked": data['tours_booked'].sum(),
            "Total Applications Processed": data['applications'].sum(),
            "Total Revenue Confirmed": data['revenue_confirmed'].sum(),
            "Total Revenue Pending": data['revenue_pending'].sum(),
            "Total Tours in Pipeline": data['tours_in_pipeline'].sum(),
            "Average Deal Value (Last 30 Days)": data['avg_deal_value_30_days'].mean(),
            "Average Close Rate (Last 30 Days)": data['avg_close_rate_30_days'].mean()
        }

        question = f"""
        Can you analyze the overall team performance based on the following key metrics?

        - Total Tours Booked: {key_metrics["Total Tours Booked"]}
        - Total Applications Processed: {key_metrics["Total Applications Processed"]}
        - Total Revenue Confirmed: {key_metrics["Total Revenue Confirmed"]}
        - Total Revenue Pending: {key_metrics["Total Revenue Pending"]}
        - Total Tours in Pipeline: {key_metrics["Total Tours in Pipeline"]}
        - Average Deal Value (Last 30 Days): {key_metrics["Average Deal Value (Last 30 Days)"]}
        - Average Close Rate (Last 30 Days): {key_metrics["Average Close Rate (Last 30 Days)"]}
          give short feed back and summary.

        """

    elif input_type == "performance_trends":
        time_period = request.args.get('time_period', '').strip().lower()

        # Grouping based on the specified time period
        if time_period == "monthly":
            performance_trends = data.resample('M', on='dated').sum()
        elif time_period == "quarterly":
            performance_trends = data.resample('Q', on='dated').sum()
        elif time_period == "yearly":
            performance_trends = data.resample('Y', on='dated').sum()
        else:
            return jsonify({"error": "Invalid time period. Please choose from monthly, quarterly, or yearly."}), 400

        question = f"""
        Can you analyze the performance trends over the {time_period} period based on the following key metrics?

        - Total Tours Booked: {performance_trends['tours_booked'].to_dict()}
        - Total Applications Processed: {performance_trends['applications'].to_dict()}
        - Total Revenue Confirmed: {performance_trends['revenue_confirmed'].to_dict()}
        - Total Revenue Pending: {performance_trends['revenue_pending'].to_dict()}
        - Total Tours in Pipeline: {performance_trends['tours_in_pipeline'].to_dict()}
        - Average Deal Value (Last 30 Days): {performance_trends['avg_deal_value_30_days'].to_dict()}
        - Average Close Rate (Last 30 Days): {performance_trends['avg_close_rate_30_days'].to_dict()}
          please also give details.
        """

    elif input_type == "employee_performance":
        employee_id = request.args.get('employee_id', '').strip()

        # Individual employee performance
        if not employee_id:
            return jsonify({"error": "Employee ID is required for individual performance."}), 400

        # Check if the employee_id exists in the data
        employee_data = data[data['employee_id'] == int(employee_id)]

        # Check if employee data is found
        if employee_data.empty:
            return jsonify({"error": f"No employee found with the ID '{employee_id}'."}), 404
        else:
            employee_info = employee_data.iloc[0]  # Get the first matching record

            key_metrics = {
                "Tours Booked": employee_info['tours_booked'],
                "Applications Processed": employee_info['applications'],
                "Revenue Confirmed": employee_info['revenue_confirmed'],
                "Revenue Pending": employee_info['revenue_pending'],
                "Tours in Pipeline": employee_info['tours_in_pipeline'],
                "Average Deal Value (Last 30 Days)": employee_info['avg_deal_value_30_days'],
                "Average Close Rate (Last 30 Days)": employee_info['avg_close_rate_30_days']
            }

            question = f"""
            Can you analyze {employee_id}'s performance based on the following key metrics?

            - Tours Booked: {key_metrics["Tours Booked"]}

            - Applications Processed: {key_metrics["Applications Processed"]}

            - Revenue Confirmed: {key_metrics["Revenue Confirmed"]}

            - Revenue Pending: {key_metrics["Revenue Pending"]}

            - "Tours in Pipeline": {key_metrics["Tours in Pipeline"]}
            
            - Average Deal Value (Last 30 Days): {key_metrics["Average Deal Value (Last 30 Days)"]}
            - Average Close Rate (Last 30 Days): {key_metrics["Average Close Rate (Last 30 Days)"]}
              Please provide a brief short performance summary and any quick short recommendations for improvement not too much long.
              please make summary,recommendations.
              
            """

    else:
        return jsonify({"error": "Invalid input type. Please use 'team_performance', 'performance_trends', or 'employee_performance'."}), 400

    # Initialize the GPT client
    client = Client()

    # Generate a response based on the question
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )

        # Check for a valid response
        if response.choices:
            return jsonify({"response": json.dumps(response.choices[0].message.content, indent=4)}), 200
        else:
            return jsonify({"error": "No valid response received from the model."}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred while communicating with the model: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

