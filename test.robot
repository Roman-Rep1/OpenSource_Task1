*** Settings ***
Documentation    Automated UI tests for WSB Pizzeria search
Library    SeleniumLibrary

Suite Setup       Open Browser    ${URL}    chrome
Suite Teardown    Close All Browsers
Test Setup        Go To    ${URL}


*** Variables ***
${URL}    http://127.0.0.1:5000/


*** Test Cases ***
Search Pizza By Name
    Input Text    id=search-input    PePpErOnI

    Element Should Be Visible
    ...    css:.pizza-item[data-name="pepperoni"]

    Element Should Not Be Visible
    ...    css:.pizza-item[data-name="margherita"]

    Element Should Not Be Visible
    ...    css:.pizza-item[data-name="capricciosa"]


Search With No Matching Results
    Input Text    id=search-input    sushi

    Element Should Not Be Visible
    ...    css:.pizza-item[data-name="margherita"]

    Element Should Not Be Visible
    ...    css:.pizza-item[data-name="pepperoni"]

    Element Should Not Be Visible
    ...    css:.pizza-item[data-name="capricciosa"]

    Element Should Not Be Visible
    ...    css:.pizza-item[data-name="hawaiian"]
