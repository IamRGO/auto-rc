import glob
import matplotlib.pyplot as plt
import data

bucket_list = []
bucket_size = 10

for i in range (0, 105, bucket_size):
  r = range(i, i + 4)
  bucket_list.append(
    [r, 0]
  )

file_list = glob.glob("processed_temp/*png")
file_index = 0
for image_path in file_list:
  i = image_path[len("processed_temp/frame_"):-4]
  file_index += 1

  data_path = "processed_temp/data_" + i + ".txt"
  output_data = data.read_output(data_path)
  steering = output_data[0] * 100
  bucket_index = int(steering / bucket_size)

  if bucket_list[bucket_index][1] > 250:
    continue

  bucket_list[bucket_index][1] += 1

chart_label_list = []
chart_value_list = []

for bucket in bucket_list:
  chart_label_list.append(str(bucket[0]))
  chart_value_list.append(bucket[1])

print("Total data size:", sum(chart_value_list))

fig = plt.figure()
plt.bar(chart_label_list, chart_value_list, width = 0.4)
plt.xlabel("steering")
plt.xticks(rotation="vertical")
plt.ylabel("count")
plt.title("Weeee")
plt.show()