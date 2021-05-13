**REST API for a system needing to assign students to classes**

* **Endpoints**
  * Students
    * '/students' : Students Endpoint - Methods: `GET` (all) | `POST`
    * '/students/<int:studentID>' : Students Endpoint - Methods: `GET` | `PUT` | `DELETE` (single by ID)
    * '/students/lastname/<string:last_name>' : Students Endpoint - Methods: `GET` (looking for each LASTNAME starting with the string)
    * '/students/firstname/<string:first_name>' : Students Endpoint - Methods: `GET` (looking for each FIRSTNAME starting with the string)
  * Classes
    * '/classes' : Classes Endpoint - Methods: `GET` (all) | `POST`
    * '/classes/<int:code>' : Classes Endpoint - Methods: `GET` | `PUT` | `DELETE` (single by ID)
    * '/classes/title/<string:title>' : Classes Endpoint - Methods: `GET` (looking for each TITLE starting with the string)
    * '/classes/description/<string:description>' : Classes Endpoint - Methods: `GET` (looking for each DESCRIPTION starting with the string)
  * Grades (Class made to join Students and Classes)
    * '/grades' : Grades Endpoint - Methods: `GET` (all) | `POST`
    * '/grades/classes/<int:code>' : Students of a Class Endpoint - Methods: `GET` (single by Class' Code)
    * '/grades/students/<int:studentID>' : Classes of a Student Endpoint - Methods: `GET` (single by Student's ID)

* **Data Params**

`POST` requests needs a body with data stablished for the determined Class without the PK:
  * Student:
    ```yaml
    {
      'last_name': String,
      'first_name': String
    }
    ```
  * Class:
    ```yaml
    {
      'title': String,
      'description': String
    }
    ```
  * Grade:
    ```yaml
    {
      'student_id': Integer,
      'class_id': Integer
    }
    ```
`PUT` requests needs a body with data that needs to be updated within the same parameters stablished for `POST`
 
* **Execute**

To execute the REST API just run the `main.py` and the flask app will execute on: `http://127.0.0.1:5000/`

**For more examples on check the `Postman_API_TESTs` file**
