## Testing

Testing of the application is performed using [pytest](https://docs.pytest.org/en/latest/contents.html).

The tests can be found in the [testing module](../testing/).

- [Testing](#testing)
- [Test usage](#test-usage)
- [Test guidelines](#test-guidelines)
- [Test coverage and knows issues](#test-coverage-and-knows-issues)
  - [Forms](#forms)
    - [Index ~](#index-)
    - [Login ~](#login-)
    - [Signup -](#signup--)
    - [Change password ~](#change-password-)
    - [Search user +](#search-user-)
  - [Models](#models)
  - [NCBI](#ncbi)
  - [Views](#views)


## Test usage

To test all tests, one can simply (in a dev environment) run `pytest` in the terminal.
This will proceed to run all unittests in the whole project.

It's also possible to run a subset of the unittests, or a specific unit test in isolation.
The syntax for this is:
`pytest path/<module>/<filename>::<testcase_function>`

This would for example turn out to be:
`pytest testing/test_models/test_create_BlastJob.py::test_blast_job_user_assignment`

## Test guidelines

All tests should be provided proper documentation, preferably also documenting what they
do not test if it could be expected that they might test it.
They should all be provided of typehint just like the rest of the code.

We should aim to split up our tests as much as possible, while this is not always easy, it should
make it easier to change only parts of the test, while leaving other parts untouched when changes
happen.


## Test coverage and knows issues

It is important to know what part of the application is tested.
A summary is listed of all known parts of the application that are currently tested, and what they test.
This part serves as a summary/appendix to the documentation on tests and hopes to provide
extra insights for what is lacking or may be useful to add/change.
For more insight on sub sections it's advised to look at the documentation of the particular
test case(s). In the case of conflicts in the documentation, docstrings take precedence.

All sub sections will be marked with a symbol to indicate the level of test coverage.

|  | description |
|-------| ------- |
| +     | full test coverage|
| ~     | some test coverage is missing    |
| -     | no or insufficient test coverage   |
### Forms

Currently, tests exist for the following forms
 - Index (blast form) ~
 - Login ~
 - Signup -
 - Change password ~
 - Search user +

#### Index ~
Testing for the index form validation. It tests if all input variables for the index page function.
The validation should have full test coverage.

However, the index form also has methods for processing the actual input. These are not tested.
The code for validation and processing are decoupled from one another in a way, and
makes a lot of assumptions of the developer. Coupling them and restructuring the code would allow testing
to achieve a better flow, and would make testing subparts more structured and allow for a better code flow.

#### Login ~

The login form is tested from a view level, which allows a more solid reliance on it 
to function in the application.
The test itself however has a gap in the test. It does not test all cases in which a login should fail, 
nor does it test if the expected user is actually logged in.

#### Signup -

The signup form also tests from a view level.
The success of a signup is currently not tested, so it's lacking in test coverage.

#### Change password ~

The password change is tested from a view level.
It properly tests changing successfully.
It however only tests 1 way changing could fail, it does not test if the new 
password fields need to be the same.

It could also do to split up the tests, so the expectations can be tested separately.

#### Search user +

The search user form tests from a view level.
It tests that the user shows up or does not show up. 
The tests could however be seperated in separate tests.


### Models

Currently, the models themselves do not really get tested. We use the django orm 
for the database and make the assumptions that those parts function. 
In that way unless stated or required otherwise, there is decided that this is not something 
that needs to be particularly tested.

There are some models which alter the behaviour of creating a row, however that is currently
no more than performing a calculation, or the logic to determine a variable is followed properly.
With the current structure of the codebase, these tests require database writes.
It would be better in the future if these parts of the codebase are functioned out, so the specific parts
are easier to test without unneeded overhead.

Parts that are tested:
 - hit calculate percentage identity +
 - hit calculate query coverage +
 - job create title +
 - job assign user +
 - unprocessed job creation +
 - unprocessed job deletion +

The coverage of the tests is good, and the parts above here are description enough.
However, as stated earlier, most tests should test a function, rather than a database write, which
would reduce code complexity greatly.

Besides the models themselves, there are also functions defined for queries, which are currently
seperate from the models, functionality that is tested:
 - get blast job +
 - get entrez accession +
 - get blast hit from id +
 - get blast hit from job id +
 - get blast job is processed +

All tests relating to the current functionality test both yes, no or nonexistent properly if
applicable. It is better to read their specific documentation to get a better feel.

### NCBI

The app majorly depends on usage of NCBI, however it is currently under tested, in relation
to its importance. It is advised that more tests are added that test the API
No parts of the actual NCBI API is tested. Only functionality surrounding the API is tested.

What is tested:
 - determining entrez program +

### Views

There is not a lot of tests going on with the views themselves, there is
a start for testing the permissions of hits, and navigation to pages.

The tests relating directly to the views, can be considered low quality and practically
non-existent.

A main part of interest would be checking that all views check for access permissions properly,
as it would go against the requests of the clients if the permissions are incorrect on pages
that require authentication.