def detect_anomalies(sensor_data: dict) -> list:
    """
    센서 데이터에서 이상치를 감지하는 함수.
    조건에 따라 Alert 메시지 리스트를 반환한다.

    Args:
        sensor_data (dict): 수신된 센서 데이터

    Returns:
        list: 이상치 발생 시 경고 메시지 리스트
    """
    alerts = []

    if sensor_data.get("temperature", 0) > 35:
        alerts.append(f"🔥 High Temperature Alert! {sensor_data['temperature']}°C")
    if sensor_data.get("humidity", 100) < 30:
        alerts.append(f"💧 Low Humidity Alert! {sensor_data['humidity']}%")
    if sensor_data.get("pm10", 0) > 80:
        alerts.append(f"🌫️ High PM10 Alert! {sensor_data['pm10']} μg/m³")
    if sensor_data.get("pm25", 0) > 50:
        alerts.append(f"🌫️ High PM2.5 Alert! {sensor_data['pm25']} μg/m³")
    if sensor_data.get("co2", 0) > 900:
        alerts.append(f"😷 High CO2 Alert! {sensor_data['co2']} ppm")

    return alerts
