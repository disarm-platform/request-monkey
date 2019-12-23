# Request-monkey

Request monkey is a containerised function that takes a parameter and does the following:

    * checks if requests to functions are successful.

    * measures the execution time of the functions.

## Steps to deploying

1. Clone all of the functions to the same directory.

1. Once all of the functions have been cloned, create a bash script which has the following content

    ```bash
    #!/bin/bash
    # Test Request Copier for Request Monkey

    test_reqs_paths="$(find . -type f -name test_req.json -not  -path './**/build/*')" 
    function_names="$(find . -type f -name test_req.json -not  -path './**/build/*' | cut -c 3- | awk -F '/' '{print $1}')"

    SAVEIFS=$IFS   # Save current IFS
    IFS=$'\n'      # Change IFS to new line
    names=($function_names) # split to array $names
    paths=($test_reqs_paths) # split to array $paths
    IFS=$SAVEIFS   # Restore IFS

    [[ -d dir ]] || mkdir "test_reqs" # if dir does not exits create it

    for (( i=0; i<${#names[@]}; i++ ))
    do
        cp ${paths[$i]} "test_reqs/${names[$i]}.json"
    done
    ```

1. Execute the created bash script.

1. A folder named `test_reqs` will be created if it does not already exist. The folder contains `<function_name>.json` for every function which is just the test_req.json for the corresponding function.

1. open the CLI and clone the repository using the command `git clone https://github.com/disarm-platform/request-monkey.git`

1. Copy the test_reqs folder to the `request_monkey/function` folder. 

1. Change to the `request monkey folder` directory using command `cd request-monkey`

1. Run the command `faas template pull https://github.com/disarm-platform/faas-templates.git` to pull the project template. 

1. Build the function using the command `faas build`

1. Deploy the function to the required gateway using
`faas deploy --gateway <gateway>`.


## Usage

- The request-monkey takes a a json object of the form: 
    ```JSON
    { "func_name": "value" }
    ```
    where `"value"` can be any of the following:

        -  <function name> in which case it returns the information of that particular function.
        
        - "all" in which case it sends request to all the deployed  function and returns their infomation in a json array.

        - "random", picks a random function, sends a request and returns the information.
