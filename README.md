# Sales Performance Analysis API

This is a Flask API that analyzes sales performance based on various metrics from a CSV file.

## Features

- Analyze overall team performance
- View performance trends over different time periods
- Analyze individual employee performance

## Endpoints

1. **Employee Performance**
   - **URL**: `/analyze`
   - **Method**: `GET`
   - **Query Parameters**:
     - `input_type=employee_performance`
     - `employee_id={id}` (e.g., `183`)
   - **Example**:
     ```
     http://127.0.0.1:5000/analyze?input_type=employee_performance&employee_id=183
     ```

2. **Team Performance**
   - **URL**: `/analyze`
   - **Method**: `GET`
   - **Query Parameters**:
     - `input_type=team_performance`
   - **Example**:
     ```
     http://127.0.0.1:5000/analyze?input_type=team_performance
     ```

3. **Performance Trends**
   - **URL**: `/analyze`
   - **Method**: `GET`
   - **Query Parameters**:
     - `input_type=performance_trends`
     - `time_period={monthly|quarterly|yearly}`
   - **Example**:
     ```
     http://127.0.0.1:5000/analyze?input_type=performance_trends&time_period=monthly
     ```


