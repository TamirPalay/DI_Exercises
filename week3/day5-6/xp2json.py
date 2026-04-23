import json
sampleJson = """{ 
   "company":{ 
      "employee":{ 
         "name":"emma",
         "payable":{ 
            "salary":7000,
            "bonus":800
         }
      }
   }
}"""
data = json.loads(sampleJson)
print("Salary:", data["company"]["employee"]["payable"]["salary"])
data["company"]["employee"]["birth_date"] = "1992-07-15"

with open("sample.json", 'w') as file_obj:
    json.dump(data, file_obj, indent=4)

print(data)


