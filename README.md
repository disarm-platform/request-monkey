# Request Monkey

A containerised function that if a function is up and running well.

## RequestMonkey

- Takes function name

- Finds the corresponding  test_req folder

- Sends requests to `http://gateway:8080/function_name`

- Checks if:

    - request was successful

    - how long the request took
    
- If no function name is given, pick a random function or test all.


