import requests 

BASE = "http://127.0.0.1:5000/"

students = [
  {
    "name": "lolad",
    "age": 21,
    "gpa": 1
  },
  {
    "name": "Chayanne",
    "age": 24,
    "gpa": 3
  },
  {
    "name": "Luis Miguel",
    "age": 20,
    "gpa": 3
  },
  {
    "name": "Juand Gabriel",
    "age": 21,
    "gpa": 3
  }
]
"""
for i in range(len(students)):
    response = requests.post(BASE + "students/{0}".format(students[i]["name"]),students[i])"""
    

response = requests.put(BASE + "students/Luis Miguel",{"age": 51})

#response = requests.put(BASE + "students?studentID=1&gpa=1")
#print(response.json())