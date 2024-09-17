A group project cloning NCBI's blast functionality.


# MasterBlast developer's guide

## Introduction

MasterBlast is a django application which mirrors the abilities of NCBI's
blastn and blastp, and gives a user the functionality to retain their blast
results. It can be used as a tool by bioinformaticians or biologists.

This application relies on Django, and blasts through NCBI. It uses Celery with RabbitMQ as broker to perform tasks asynchronously, however if the broker is not available, the application is configured to perform tasks synchronously, which could affect user experience and allow for tasks to be cancelled in the middle.

## Installation & dependencies & usage

The [installation](/.README/README.Installation.md) document describes in detail how MasterBlast is installed.

MasterBlast's most notable dependencies are:

- NCBI blast API (through BioPython)
- Django
- Celery 
- RabbitMQ 

A full list of dependencies including versions can be found in the [requirements](/requirements/dev.txt).

Instructions on how to use the application can be found on the [usage instructions](/.README/README.Usage.md)

If there is a need to initalize the application with an intact database, an short explanation of the database fixtures provided with MasterBlast can be found in [Fixtures](/.README/fixtures/README.Fixtures.md).

## Screens

All of the different screens (pages) that MasterBlast offers are described in detail in the [screens](README.Screens.md) resource.

## Unit testing

Testing of the application is performed using [pytest](https://docs.pytest.org/en/latest/contents.html).

The tests can be found in the [testing module](/testing).

Documentation for test usage and coverage can be found in [test documentation](/testing/README.testing.md)

## Development status

All of the requirements and nice-to-haves that were envisioned for this first version of
MasterBlast have been successfully implemented. Users are able to log in, run
BLAST jobs, view the results and share them with other users.

### Bugs

#### Matching BLAST website output

The hits that are found in a BLAST job do not 100% match what is displayed on NCBI's BLAST in the browser. This is due to how Biopython is used. The output of MasterBlast does match NCBI in most cases. The only way to overcome this shortcoming, would
be to not use Biopython.

#### Session management

Logging in or registering from a new URL (http://127.0.0.1:8000/login) overwrites the existing session without properly logging out the previous user.

#### Visual

- When loading the comparison page with a very narrow screen, the graph will be hidden until the screen is resized.
- The "Log out" button on the navbar might resize when the screen is very narrow.
- On the personalia page, the green patches in the "User stats" section will touch on a lot of screens.
- On the personalia page, there is a question mark in the "Account information" box. This is not supposed to be there.
- On the personalia page, when the average hits per job in the user stats has two decimal places with a trailing zero, it is displayed with only one decimal place instead of two.
- On the loading page, the loading animation is placed on the left side of the screen.
- On the BLAST hit page, the Genbank sequence section is not in Courier New, the standard font for displaying sequences. This has to be changed to improve readability of the sequence.

### Future features

#### Systematical changes

- **Improving BLAST speed**:
  MasterBlast currently uses Biopython to perform BLAST queries using the NCBI BLAST API.
  This comes with the disadvantage of long waiting times when traffic on
  NCBI's servers is high. A BLAST query on MasterBlast typically runs between 3-60 minutes.
  To reduce the running time of a BLAST job a local version of BLAST can be run.
  This would make MasterBlast completely independent of NCBI's API, and the power of
  the hardware MasterBlast is running on would be the limiting factor.

- **Removing or recovering unprocessed BLAST jobs**:
  For every running BLAST job, MasterBlast creates an UnprocessedBlastJob object
  while it is running. However, MasterBlast only removes the Unprocessed version of
  the BlastJob object when the job has been successfully run. This means a large
  amount of UnprocessedBlastJob objects could accumulate and take up storage. A
  routine removal of UnprocessedBlastJob objects could be added to prevent this.

  On the other hand, users currently can't access Unprocessed BLAST jobs again. A way to easily
  recover or continue interrupted BLAST jobs could also be a good addition to reduce
  the amount of UnprocessedBlastJob objects in the database.

- **Adding BLAST programs**:
  Currently, MasterBlast only supports BLASTn and BLASTp. Further BLAST programs,
  such as BLASTx and tBLASTn, could be added to the application to expand its functionality.

- **Extend to multiple sequence analysis**:
  MasterBlast is designed to only process one sequence at a time. However, enabling the
  processing of multiple sequences has significant advantages. It allows for more complex
  analysis and increases efficiency by handling batch processing. This would save time and
  resources compared to running single queries for each sequence.

#### Smaller changes

- **Zero hits clarification**:
  When a query returns zero hits after running, there is no clear reason shown why there are no
  hits for the BLAST job. The reason for this could be problems with NCBI's server on which
  MasterBlast relies on, either could the reason be that the query sequence actually has zero
  hits. It would be a good development to distinguish these two differences and show the user
  why their BLAST job did not succeed.

- **Viewing query sequences**:
  The application currently does not provide any way to view the query sequence of
  a BLAST job. This could be added to the BLAST result page in a future version.

- **Recent job filters**:
  On the recent jobs page, a range of filters can be applied to filter and display BlastJob objects.
  After submitting the filter form, the input fields get emptied. If the user wants to apply
  more filters to the current filtered list shown, they have to fill in the filters manually
  all over again. For a boost of user experience, the earlier applied filters should stay
  filled in so more filters can be stacked. Then there should also be a button which clears
  the input fields for when the user wishes to see the default list again.

- **Interactive tooltips**:
  When hovering over the bars in the comparison bar charts, the tooltips could be linking
  to the BLAST hit page of the current hit the user is hovering over.

- **Hit limitation awareness**:
  When working with the BLAST API, a maximum of 50 hits get returned, even when the query actually
  has more hits. Enhance the BLAST job functionality by reporting or notifying the user when the
  actual hit count exceeds the retrievable limit of 50 hits. This alerts the user that the results
  might not be fully complete.

- **Delete shared jobs**:
  SharedJobs objects can't be deleted by the user. When then user receives a lot of jobs shared by
  other users, a long list of shared jobs accumulates on the personalia page of the user. A good
  future feature might be a button that enables the user to delete shared jobs, placed in a new
  column in the shared_jobs table.
