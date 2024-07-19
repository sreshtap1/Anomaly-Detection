import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# Generate timestamp values for one day (12 hours, AM/PM format)
timestamps = np.arange(0, 24, 1)  # From 00:00 to 23:00

# Create an array to represent AM/PM
ampm = ['AM', 'PM'] * 12  # Alternates between AM and PM

# Generate normal data with a daily pattern
normal_data = np.sin(2 * np.pi * timestamps / 12) + np.random.randn(len(timestamps)) * 0.2

# Generate some anomalies at specific hours
anomaly_indices = [3, 8]
anomalies = np.random.uniform(low=-0.5, high=0.5, size=len(anomaly_indices))
timestamps_with_anomalies = timestamps[anomaly_indices]

# Combine normal data and anomalies
data = np.copy(normal_data)
data[anomaly_indices] += anomalies

# Create an isolation forest model
model = IsolationForest(contamination=0.2)  # Adjust the contamination parameter as needed

# Fit the model to the data
model.fit(data.reshape(-1, 1))

# Predict anomalies (1 for normal data, -1 for anomalies)
predictions = model.predict(data.reshape(-1, 1))

# Correct anomalies based on previous values
corrected_data = np.copy(data)
for i, prediction in enumerate(predictions):
    if prediction == -1:
        if i > 0:
            corrected_data[i] = (corrected_data[i - 1] + corrected_data[i + 1]) / 2
        else:
            corrected_data[i] = corrected_data[i + 1]

# Plot the value-time graph (with anomalies)
plt.figure(figsize=(12, 6))
plt.plot(timestamps, data, label='Value-Time (with Anomalies)')
plt.scatter(timestamps_with_anomalies, data[anomaly_indices], color='red', label='Anomalies')
plt.xlabel('Time (12-Hour Format)')
plt.ylabel('Value')
plt.xticks(ticks=timestamps, labels=[f'{hour}:00 {ampm[i]}' for i, hour in enumerate(timestamps)])
plt.legend()
plt.title('Value-Time Graph (with Anomalies)')

# Display the value-time graph
plt.show()

# Plot the anomaly-time graph
plt.figure(figsize=(12, 6))
plt.plot(timestamps, predictions, label='Anomaly-Time')
plt.xlabel('Time (12-Hour Format)')
plt.ylabel('Anomaly Detection (1 for Normal, -1 for Anomalies)')
plt.xticks(ticks=timestamps, labels=[f'{hour}:00 {ampm[i]}' for i, hour in enumerate(timestamps)])
plt.legend()
plt.title('Anomaly-Time Graph')

# Display the anomaly-time graph
plt.show()

# Plot the corrected value-time graph (with anomalies)
plt.figure(figsize=(12, 6))
plt.plot(timestamps, corrected_data, label='Corrected Value-Time')
plt.scatter(timestamps_with_anomalies, corrected_data[anomaly_indices], color='red', label='Anomalies (Corrected)')
plt.xlabel('Time (12-Hour Format)')
plt.ylabel('Corrected Value')
plt.xticks(ticks=timestamps, labels=[f'{hour}:00 {ampm[i]}' for i, hour in enumerate(timestamps)])
plt.legend()
plt.title('Corrected Value-Time Graph (with Anomalies)')

# Display the corrected value-time graph
plt.show()
