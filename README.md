# Beequip_Test

For Beequip i will be making the data engineer test which is included for reference. All documentation about the application and datamodel is presented below. It also explains the progress i made to achieve the desired results in order of execution.

## Assessing Non-functional and functional requirements

The first step was to understand and translate all functional and non functional requirements and make key choises before i could start building the application and data model.

### Non-functional requirements

1. Application needs to be backed by a SQL server and explain your db server choice
   - I have chosen a PostgreSQL databases hosted on Microsoft Azure. I chose this type of server because i have heard it was already being used at Beequip. For this small test database PostgreSQL can handle all requirements. I chose to host this database on Azure because i already have a private account there.  
2. Use the data in the `data/` directory to create the database schema and records and explain how you did this
   - TODO: By running the create.py file in create_database
3. Respond to the API requests in JSON
   - TODO: By using Flask and JSON
4. No API authentication is required
   - I will implement a standard basic security to the database but include the authorization in the repository, so it will not be secure at all.

### Functional requirements

1. What's the outstanding for a lease given a reference and date?
   - TODO
2. What's the total outstanding for a organisation given a Camber of Commerce number and date?
   - TODO
3. What's the total outstanding per team and lane given a date?
   - TODO
4. What's the average outstanding at the start of the lease per team and lane?
   - TODO
5. What's the total daily outstanding given a year?
   - TODO    

Of the 5 functional requirements i first created a use case diagram, just to get a visual overview of what is asked.

![Use Case Diagram](docs/20211207_Use_Cases.png)    


>## Data engineer test
>
>We'll be using this test to assess your skill level as data engineer. This test is designed to covered a wide variety of skills that are needed in the day-to-day job of a data engineer at [Beequip](https://www.beequip.nl/). We expect you to spend a maximum of eight hours on this test. Don't worry when you run out of time though, we would still like to see what you came up with!
>
>### Objectives and requirements
>
>Create a Python web application that provides API endpoints to return the following information:
>
>- What's the outstanding for a lease given a reference and date?
>- What's the total outstanding for a organisation given a Camber of Commerce number and date?
>- What's the total outstanding per team and lane given a date?
>- What's the average outstanding at the start of the lease per team and lane?
>- What's the total daily outstanding given a year?
>
>Some of the requirements are:
>
>- Application needs to be backed by a SQL server and explain your db server choice
>- Use the data in the `data/` directory to create the database schema and records and explain how you did this
>- Respond to the API requests in JSON
>- No API authentication is required
>
>
>### Definitions
>
>In order to help you understand which data you need to use to provide the information you can use the definitions below.
>
>| Term | Definition |
>| --- | --- |
>| `t` | Loans are repaid in terms, this is the number of the term. |
>| `installment` | Amount that's paid in that month. |
>| `principal` | Amount that's repaid of the loan in that month. |
>| `interest` | Amount that's paid as interest on the loan in that month. | 
>| `outstanding` | Amount that's still remaining to be paid on a loan. |
>
>
>### Deliverables
>
>Send us a link to the hosted repository with your code. It can be hosted anywhere e.g. Github, Gitlab as long as you provide us access. Include all the code and instructions that are necessary to run the application and make the API requests.
>
>### Questions
>
>In case you have questions about the test you can contact Jan van der Pas (`jan.vanderpas@beequip.nl`).

