# MasterBlast user guide

MasterBlast is a Django-based application designed to facilitate and enhance the biological analysis of sequence alignments through [NCBI BLAST (Basic Local Alignment Search Tool)](https://blast.ncbi.nlm.nih.gov/Blast.cgi), supporting both blastn and blastp modes. Its primary goal is to provide a user-friendly platform where users can perform sequence alignment searches against a large-scale genomic database. This enables biologists and bioinformaticians to identify similar sequences, understand genetic differences between sequences and discover evolutionary relationships between different organisms.

The application is particularly useful for academic researchers, geneticists and students in molecular biology and genetics. It provides a valuable tool for those involved in genomic research, evolutionary biology studies or any other scientific activity that requires detailed DNA or protein sequence analysis.

MasterBlast not only allows for performing BLAST queries, but also for easily storing and retrieving previously conducted jobs from a user's account. Jobs can later be accessed by the user and shared among other users of MasterBlast, also called Blast Buddies. This collaborative feature enhances productivity by enabling users to access and continue from others' analyses. Additionaly, the application includes vizualisation tools that represent the alignment data, making complex information managable and more clear.

---

## Table of contents

- [MasterBlast user guide](#masterblast-user-guide)
  - [Table of contents](#table-of-contents)
  - [Installation](#installation)
  - [Running the application](#running-the-application)
    - [Starting the application](#starting-the-application)
    - [Closing the application with docker](#closing-the-application-with-docker)
  - [Screens](#screens)
    - [BLAST page](#blast-page)
      - [BLAST form](#blast-form)
      - [Loading page](#loading-page)
    - [BLAST results page](#blast-results-page)
      - [BLAST job card](#blast-job-card)
      - [Share job and Comparison buttons](#share-job-and-comparison-buttons)
      - [BLAST results table](#blast-results-table)
    - [BLAST hit page](#blast-hit-page)
      - [Header](#header)
      - [BLAST hit table](#blast-hit-table)
      - [Genbank display](#genbank-display)
      - [Export menu](#export-menu)
    - [Comparison page](#comparison-page)
      - [Comparison graphs](#comparison-graphs)
      - [Comparison table](#comparison-table)
    - [Signup page](#signup-page)
    - [Login page](#login-page)
    - [Recent page](#recent-page)
      - [Filter jobs](#filter-jobs)
    - [Personalia page](#personalia-page)
      - [Account information \& change password](#account-information--change-password)
      - [User stats](#user-stats)
      - [My Blast Buddy Club](#my-blast-buddy-club)
      - [Shared MasterBlast jobs](#shared-masterblast-jobs)
    - [Known limitations](#known-limitations)
      - [Technical limitations](#technical-limitations)
      - [Performance limitations](#performance-limitations)
      - [Bugs](#bugs)
      - [Future features](#future-features)


---

## Installation

This application is based on the python programming language, and uses a lot other third party resources, 
both python and none python resources.
It is recommended to setup the application through the programming Docker, you need to [download Docker](https://www.docker.com/products/docker-desktop/).
After downloading Docker, it is possible that a large amount of RAM is suddenly used up, this can be resolved [following this guide](https://www.aleksandrhovhannisyan.com/blog/limiting-memory-usage-in-wsl-2/).

If it's not possible to solve docker related tech problems, it's advises to look at the developer installation guide for an alternate way of installing and using the application.
A detailed guide on installing the application can be found [here](/.README/README.Installation.md).

## Running the application

We will presume you are using docker. If you are not able to get docker running, we would
like to refer you to the [developer usage guide](/.README/README.Usage.md).

All commands are performed in a commandline terminal opened in the root directory unless stated otherwise.
[See how to open a terminal in a directory.](https://www.lifewire.com/open-command-prompt-in-a-folder-5185505)
The root directory of the application would be in the directory BBC-app/ in this case.

When the application is started it will open at the url http://127.0.0.1:8000.
This url can then be used in the searchbar of the browser to go to the website.

### Starting the application

First you open a terminal

In the terminal run the command:
`docker compose up --build`.

The application will now run at http://127.0.0.1:8000 on docker-desktop.

### Closing the application with docker

There are 2 options.
It's possible to press `ctr + C` in the terminal where docker is running. It's also possible to close the application go to 
the docker-desktop app and go to containers, and click on the link to the running container.
In the top right of the page click on the blue button stop.

---

## Screens

### BLAST page

![Blast page image](/readme_media/readme_images/BLAST_page.png)

The BLAST page is MasterBlast's landing page, where the user can perform a
BLAST job.

#### BLAST form

The form has buttons to select either BLASTn (nucleotide sequences) or BLASTp
(amino acid sequences). The user can give a title to their job through a text
input. If the user enters an incorrect query, or misuses the form in any
other way, an error message is displayed.

The video below shows how the BLAST form can be used.

![Blast job video](/readme_media/readme_videos/perform_BLAST_job.mov)

#### Loading page

If MasterBlast is installed with all of its dependencies, which is recommended
(see [Docker](/.README/README.Docker.md) to learn how to install MasterBlast), a loading screen
will be displayed as soon as the user performs their BLAST job. The loading
screen shows how long the job title and has been running for. Every ten seconds
the server retries to fetch the job's results, which is also shown by a
counter.

The video below shows the loading page.

![Loading page video](/readme_media/readme_videos/loading_page.mov)

When the results of the BLAST job have successfully loaded, the user is sent
to the BLAST results page.

### BLAST results page

![Blast results page image](/readme_media/readme_images/BLAST_results_page.png)

#### BLAST job card

The BLAST results page displays the result of a BLAST job run on MasterBlast.
All of the following information about a BLAST job is shown in a card on the
top of the BLAST results page:

- Title
- Query length
- Hit count
- Date
- Time
- User

It's worth mentioning that a user can run BLAST jobs without logging in to
their account, in which case the value for user will be "unkown".

#### Share job and Comparison buttons

On the top right of the page, there are two buttons: "Share job" and
"Comparison". Clicking the "Share job" button allows a logged in user to share
their BLAST job with a user in their BlastBuddyClub. Clicking the "Comparison"
button takes the user to the comparison page, where BLAST hits can be compared.
At least two hits must be selected through the checkboxes in the BLAST results
table below, or an error message will be displayed.

![Blast results buttons video](/readme_media/readme_videos/BLAST_results_buttons.mov)

#### BLAST results table

For each hit, the following information is displayed in a table below the BLAST
job card and the "Share job" and "Comparison" buttons. The table contains the
following columns:

- Description
- Organism
- BLAST score
- Query coverage
- Bit score
- E-value
- Percentage identity
- Alignment
- Select

The "Description" and "Organism" column headers can be clicked to
_alphabetically_ sort the column. The "BLAST score", "Query coverage",
"Bit score", "E-value" and "Percentage identity" column headers can be clicked
to _numerically_ sort the column. The "Alignment" column is not sortable.
By default, the table is sorted by ascending E-value. The "Select" column
contains checkboxes that allow the user to select a hit to take to the
comparison page. Its column header can be clicked to select all of the hits in
the table by checking all the checkboxes inside the column.

The values in the "Description" column are clickable links to the BLAST hit's
respective BLAST hit page.

The video below shows how to interact with the BLAST results table.

![Blast results table video](/readme_media/readme_videos/BLAST_results_table.mov)

### BLAST hit page

![Blast hit page image](/readme_media/readme_images/BLAST_hit_page.png)

#### Header

The BLAST hit page displays a header on the top of the page where the BLAST
hit's "description" is displayed. This is the same text as is shown in the
results table on NCBI BLAST.

#### BLAST hit table

Below the header, a table displays the BLAST hit's attributes in the columns
"Accession", "Query length", "Organism", "Percentage identity", "Query
coverage" and "E-value".

#### Genbank display

If the hit has a Genbank file available, it is displayed on the center-left of
the page under the "Genbank" header.

#### Export menu

On the center-right of the page, a dropdown selection menu is headed by the
text "Export to file". The menu is set to "Genbank" by default. The only other
option is "FASTA". Clicking the "Export" button below the dropdown menu will
export the BLAST hit's file of the type selected in the menu.

The video below demonstrates usage of the export menu.

![Export Blast hit video](/readme_media/readme_videos/export_BLAST_hit.mov)

### Comparison page

![Comparison page image](/readme_media/readme_images/comparison_page.png)

#### Comparison graphs

After selecting hits and clicking the Comparison button on the BLAST result page,
the user will be sent to the comparison page. Here, a number of graphs can be shown
containing different information. The following graphs can be shown:

- Sequence length barchart
- Percentage identity barchart
- Query coverage barchart
- E-value piechart

The three barcharts display the differences in sequence data across the range of
selected BLAST hits.
The E-value piechart displays the grades of significance among the selected BLAST hits.
This gives a good insight whether the BLAST job returned reliable hits.

All graphs can be exported, simply by clicking the Save button in the top right of the plot.

The video below shows how to interact with the comparison graphs.

![Comparison graphs video](/readme_media/readme_videos/comparison_graphs.mp4)

#### Comparison table

The comparison table displays information of the hits selected on the BLAST
result page for more thorough analysis.
The table contains the following columns:

- Description
- Accession
- Length
- Organism
- Query coverage
- Percentage identity
- E-value

The "Description", "Accession" and "Organism" column headers can be clicked to
_alphabetically_ sort the column. The "Length", "Query coverage",
"Percentage identity" and "E-value" column headers can be clicked
to _numerically_ sort the column. The table is sorted the same as the
[BLAST results table](#blast-results-table), so by ascending E-value.

The "Description" rows can be clicked, they will redirect the user to the
corresponding BLAST hit page.

The video below shows how to interact with the comparison table.

![Comparison table video](/readme_media/readme_videos/comparison_table.mp4)

### Signup page

In the middle of the page, the signup box is displayed. This box has three input fields:
the username, email adress and the password.

- The username has to be unique, so choose a username that has not been taken already.
- Choose your email adress. The same email adress can be used multiple times by different users.
- The account needs a password. There are no requirements to the password. The password can be changed later by the user.

When all input fields are filled in, click the "Sign up" button to register.
The "Log in" button brings the user back to the login page.

The video below demonstrates the usage of the signup page.

![Signup page video](/readme_media/readme_videos/signup.mp4)

### Login page

In the middle of the page, the login box is displayed. This box has two input fields:
the username and the password.

- To log in you must fill in your username with the corresponding password.
- After filling in the input fields, click the "Log in" button to log in.

After successful log in you will be taken to the BLAST page.
Logged in users have access to more pages and functionality

The button "To sign up" is also shown.
This button brings you to the signup page in case you have no account yet.

The video below demonstrates the usage of the login page.

![Login page video](/readme_media/readme_videos/login.mp4)

### Recent page

![Recent page image](/readme_media/readme_images/recent_page.png)

#### Filter jobs

The recent page shows by default the ten most recent BLAST jobs that have been performed.

The BLAST jobs can be filtered by a variety of factors. These are the following:

- Name
- Minimal query length
- Maximum query length
- Date

When filtering on the job name, the query does not have to match
exactly with the name of the job searched for. The system searches
for jobs that contain the term in the "Name contains" field.
The miminal and maximum filtering is particularly useful for distinguishing
short and long query sequences. Date filtering can be applied for
searching jobs ran on certain dates.

After filling in the desired filter(s) and clicking the Filter button, all
BLAST jobs that match the filter(s) are displayed. The table columns can be
sorted ascending and descending by clicking the table headers. The table is
sorted on date - time by default.

The video below shows how to interact with the recent job page and filter jobs.

![Recent filtering video](/readme_media/readme_videos/recent_filtering.mp4)

### Personalia page

To go to this page you have to be logged in.

#### Account information & change password

On the leftside of the page, a box titled "Account information?" is displayed.
This box shows you the username and email of your account.
Below, three input fields are shown to change your password.
The first field demands your current password that needs to be changed.
The remaining two fields are for the new password. These two passwords have to match.

#### User stats

On the top right is the box "User stats".
This box shows some interesting facts about the user.
The following statistics are displayed:

- The amount of jobs ran by the user.
- The amount of days since signup on the MasterBlast app.
- The total length of all queries ran by the user.
- The average hits found per job.
- The longest query submitted by the user.

#### My Blast Buddy Club

The box "My Blast Buddy Club" shows a list of all the buddies you have.
On the right side of the list the button "👤-" gets shown for each buddy.
This can be used to remove the user as a buddy.
The bottom of the box shows an input field to search for users to add
as a buddy.
To search for a user you need to have to search for the exact username
you're looking for. Then click on the "🔍︎" button to search for the user.
If the username was correct, the user gets displayed. On the right side,
click the button "👤+" to add the user as a buddy.

#### Shared MasterBlast jobs

The box at the bottom of the page shows the jobs that have been shared
with you by other users.
The following information about the shared jobs is displayed:

- Job title
- Hit count
- Date
- Time
- The user who shared the job with you

Click on the job title names to see the shared job.
When you are on the BLAST results page from a job shared with you,
it is not possible to share that job further with your buddies.

The video below demonstrates the usage of the personalia page.

![Personalia page video](/readme_media/readme_videos/personalia.mp4)

---

### Known limitations

In this section, we describe some of the known problems and restrictions you might
encounter while using the MasterBlast application. Our goal is to be
transparent about the application's capabilities. This way, you can use it
more effectively and understand which parts are still up for development.
If any unexpected behaviour occurs, that does not match any of the described problems,
please mail them to <InsecureBicepAndy@gmail.com>, so you can help us diagnose the issue.

#### Technical limitations

- **File input handling**:
  The application allows input of any file type. If there is an issue with
  the file format, an "Invalid sequence" error message will be shown rather
  than specifying the real format issue.

- **Zero hits handling**:
  A query may return zero hits for various reasons. A query may actually have
  zero hits or there is a problem with the NCBI server. The actual reason for
  not capturing hits is not collected, the application simply display 0
  hits without announcing the reason.

- **Hit limitation**:
  A maximum of 50 hits can be retrieved in a BLAST job, even if the actual
  hit count is higher than 50.

- **JavaScript dependency**:
  The application requires JavaScript to function properly, which means that
  it may not work correctly on devices where JavaScript is disabled or unsupported.

- **Visual inconsistency across devices**:
  The appearance of a screen may differ when the screen dimensions are adjusted.
  There might be visual differences among different devices. This has been resolved
  in most places to avoid significant differences, but it may still occur.
  As a result of the appearance is managed, it does not have proper mobile phone support.

#### Performance limitations

- **Slow BLAST processing**:
  BLAST searches can take up quite some time, especially during peak usage times
  of the NCBI server. This is because direct users of the official BLAST webpage
  have higher priority than API users.

- **Job interruption**:
  There is no mechanism to resume or manage running BLAST jobs that are
  interrupted by unexpected closure of the application.

#### Bugs

- **Logging in and out**:
  If you're on the login or registration page while already logged in on
  another tab, you can accidentally log out of your current session without
  realizing it. This happens because the system lets you log in or sign up
  again with a different account, which automatically logs out the current user.

- **Account information**:
  There is a question mark in the "Account information" box. This is not supposed to be there.

- **Genbank sequence display**:
  The Genbank display section on the BLAST hit page is in the standard app font.
  This causes the sequence to be misaligned on two adjacent lines. The standard
  font for displaying sequences is Courier New, where all characters are the
  same size so the sequence is properly aligned.

- **Decimal display**:
  In some cases, especially in the user statistics section, numbers might
  not display with the correct decimal precision.

#### Future features

- **Job recovery**:
  Introducing a way to easily recover or continue interrupted BLAST
  jobs without losing any progress.

- **Recent job filters**:
  Applied filters disappear after clicking the Filter button. Stacking filters
  after clicking the Filter button is not possible, all filters have to be
  applied manually again. This might be a small adjustment that improves user experience.

- **Interactive tooltips**:
  A feature that enhances the comparison graphs with clickable tooltips linking
  directly to the corresponding BLAST hit page.

- **Extend analysis functionalities**:
  Currently, MasterBlast is designed to only process one sequence at a time.
  Enabling the processing of multiple sequences allows for more complex
  analysis and increases efficiency. Apart from that, more BLAST programs could
  be added. The programs blastx or tblastn would immensely expand functionality.

- **Delete shared jobs**:
  It is not yet possible to delete shared MasterBlast jobs, which can result
  in a long list accumulating on your personalia page over time.
  This functionality could be added.
