def save_to_file(file_name, jobs): #file csv 저장 함수, file의 이름과 내용인 jobs를 받음
  file=open(f'{file_name}.csv', 'w')
  
  file.write("Position, Company, Location, URL\n")
  
  for job in jobs:
    file.write(f"{job['position']}, {job['company']}, {job['location']}, {job['link']}\n")
  
  file.close()
