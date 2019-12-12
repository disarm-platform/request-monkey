# Request-monkey

## Description

- Is containerised function that takes a function name and does the following:

    * checks if requests to the function are successful.

    * measures the execution time of the function

## Steps to deploying

1. open the CLI and run clone the repo using the command `git clone https://github.com/disarm-platform/request-monkey.git`

1. Change to the cloned directory using command`cd request-monkey`

1. Build the function using the command `faas build`

1. Deploy the function to the required gateway using
`faas deploy --gateway <gateway>`.

## Usage

- The request-monkey takes a a json object of the form: 
    ```JSON
    { "funct_name": "value" }
    ```
    where value can be any of the following:

        -  a function name in which case it returns the information of that particular function.
        
        - "all" in which case it sends request to all the deployed  function and returns their infomation in a json array.

        - "random", picks a random function, sends a request and returns the information

## Progress

- Works if you specify the function name

- Still implementing all and random options

## Blockers

- Some functions take to long to reply hence causing request monkey to hang