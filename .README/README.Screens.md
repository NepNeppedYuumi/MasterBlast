## Screens

### Table of contents

- [Screens](#screens)
  - [Table of contents](#table-of-contents)
  - [Files](#files)
  - [Navigation](#navigation)
    - [Navbar](#navbar)
  - [BLAST page](#blast-page)
    - [Query input](#query-input)
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
  - [Recent job page](#recent-job-page)
  - [Personalia page](#personalia-page)
    - [Account information \& change password](#account-information--change-password)
    - [User stats](#user-stats)
    - [My Blast Buddie Club](#my-blast-buddie-club)
  - [Shared MasterBlast jobs](#shared-masterblast-jobs)


### Files

The HTML files for all the screens can be found in the folder
`Blaster/templates/pages/`. These HTML files also use the file
`templates/base.html` to load things that are 
used on all pages, like the header. The error page HTML file are found in the
same folder as the base.html.

The folder `Blaster/static/` contains all CSS, JavaScript and image files
needed to use MasterBlast. This includes the `css/base.css` file, which has all
the css for the appearance of the pages. The two files in the folder `img/` are
used for the logo in the header and to show a loading animation on the loading
page.

The files needed to load the pages are in the folder `Blaster/views/`, with each
file having the name of the page, and the error pages are in a separate folder
called errors in this folder. The database models can be found in the folder
`Blaster/models/`, again with each model having its own file.

There are also back-end Python scripts from which functions are imported
throughout the application. Barring any scripts related to Celery, they can all
be found in the `Blaster/utils/` folder.

An overview of the JavaScript files used by different screens is
given in the table below.

|**page**|**.js files**|
|-|:-:|
| loading | loading_result | 
| BLAST results| blast_result_error, share_jobs, select-all, enhance-tablesaw, format-e-value |
| BLAST hit | export-hit, format-e-value |
| comparison | comparison-graphs, enhance-tablesaw, format-e-value |
| recent | enhance-tablesaw |
| personalia | blastbuddie |

### Navigation

MasterBlast's index page is the BLAST page, which offers two logical paths
of navigation to the user. The user performs a query on the BLAST page and
waits until the application takes the user to the BLAST results page. From
there, they can either view a single hit, or take multiple hits to the
comparison page. From the comparison page, one can go and view a single hit.

On every page, the navbar is displayed. It allows the user to go to the recent,
personalia, log in and BLAST pages. All of the possible navigation paths
are shown in the image below.

![alt text](/readme_media/readme_images/page_navigation.png)

#### Navbar

The navigation bar (navbar) is visible on all screens and is the main way to
navigate through different portions of the application.

When the user is not logged in, the navbar shows:
- MasterBlast logo, this button brings the user to the BLAST page.
- "Login", this button sends the user to the login page.

When the user is logged in, the navbar shows:
- "Recent", this button brings the user to the recent BLAST jobs page.
- "Personalia", this button brings the user to the personalia page where
  different account information is visible.
- "Logout", this button replaces the Login button when the user is logged in.
  It logs the user out and then brings them to the Blast page.

### BLAST page

`http://127.0.0.1:8000/`

The BLAST page is MasterBlast's landing page, where the user can perform a
BLAST job.

The form has buttons to select either BLASTn (nucleotide sequences) or BLASTp
(amino acid sequences). The user can give a title to their job through a text
input. When no title is given, the FASTA format header is used as job title by
default. When no FASTA format header is included with the query sequence, the
name _"MasterBlast[Job_id]"_ is used as job title.

#### Query input

If the user enters an incorrect query or misuses the form in any
other way, an error message is displayed.
The user can input any file for the queries. This can create problems if the
file is not able to be decoded to normal string, This will most
likely give the error stating the sequence is invalid, rather than
the file type being wrong.
The application is also only build to handle 1 query to be BLAST at the same
time. There are multiple reasons why the BLAST API could work better in the
scope of this application, sometimes making the run time of the BLAST jobs very
long. The application doesn't pick up the reason why a job gives zero hits,
this could be caused by a server problem or a query actually doesn't return
any hits.

### Loading page

`http://127.0.0.1:8000/loading_result/<job_id>`

If MasterBlast is installed with all of its dependencies, which is recommended
(see [Docker](/.README/README.Docker.md) to learn how to install MasterBlast),
a loading screen will be displayed as soon as the user performs their BLAST job.
The loading screen shows the job title and how long it has been running for.
Every ten seconds the server retries to fetch the job's results, which is also
shown by a counter. When the results of the BLAST job have successfully loaded,
the user is sent to the BLAST results page.

### BLAST results page

`http://127.0.0.1:8000/blast_result/<job_id>`

#### BLAST job card

The BLAST results page displays the result of a BLAST job run on MasterBlast.
All of the following information about a BLAST job is shown in a card on the
top left of the BLAST results page:

- Title
- Query length
- Hit count
- Date
- Time
- User

It's worth mentioning that a user can run BLAST jobs without logging in to
their account, in which case the value for user will be "unkown".

#### Share job and Comparison buttons

On the top right of the page, there are two buttons: "Share job" (which is
hidden if not logged in) and "Comparison". Clicking the "Share job" button
allows a logged in user to share their BLAST job with a user in their BlastBuddyClub.
The user can choose a Blast Buddie to share the job with. This job will become
a SharedJob object in the account of the Blast Buddie.

Clicking the "Comparison" button takes the user to the comparison page, where
BLAST hits can be compared. At least two hits must be selected through the
checkboxes in the BLAST results table below, or an error message will be displayed.

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


The sorting of the table is done through Tablesaw.js. The E-values are
reformatted to a numerical notation in Javascript to allow for Tablesaw
to sort, but displayed in scientific notation.

The values in the "Description" column are links to the BLAST hit's
respective BLAST hit page.

### BLAST hit page

`http://127.0.0.1:8000/blast_hit`

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
the page under the "Genbank" header. This has minimal styling and can
get very long. The size of the file can make the page very slow.

#### Export menu

On the center-right of the page, a dropdown selection menu is headed by the
text "Export to file". The menu is set to "Genbank" by default. The only other
option is "FASTA". Clicking the "Export" button below the dropdown menu will
export the BLAST hit's file of the type selected in the menu.

### Comparison page

`http://127.0.0.1:8000/comparison`

#### Comparison graphs

After selecting hits and clicking the "Comparison" button on the BLAST results
page, the user will be sent to the comparison page. Here, a number of graphs
can be shown containing different information. The following graphs can be
shown:

- Sequence length barchart
- Percentage identity barchart
- Query coverage barchart
- E-value piechart

The 4 graphs are made using bokeh. Later on there could be more plots made to be shown.
All graphs can be exported, by clicking the Save button in the top right of the plot.
This save botton is a standard save button from Bokeh. The initial idea was to make a
custom export function, this did not succeed in the short development period of the application.
The Savetool function from Bokeh could not be used easily for own benefit.

#### Comparison table

The comparison table displays information of the hits selected on the BLAST
result page for more thorough analysis. The table contains the following columns:

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
All the sorting of the tabel uses Tablesaw. The E-values are reformatted to
a numerical notation in Javascript to order, but displayed in scientific notation.

The "Description" rows will redirect the user to the corresponding BLAST hit page.

### Signup page

`http://127.0.0.1:8000/signup`

In the middle of the page, the signup box is displayed. This box has
three input fields: username, email address and password.
All input fields have to filled in to be able to register. The only
requirement is to choose a username that has not been taken already.
The "Log in" button sends the user back to the login page.

The page uses the basic Django signup form for users. This also creates the
table BlastBuddies for the user. The table is needed to prevent some errors
later in the application. The user gets logged in automatically after
a successful signup.

### Login page

`http://127.0.0.1:8000/login`

In the middle of the page, the login box is displayed. This box has
two input fields: the username and the password.
After successful log in the user will be taken to the BLAST page.
Logged in users have access to more pages and functionality.
The button "To sign up" is also shown. This button brings the user
to the signup page in case the user doesn't have an account yet.
The login uses to standard django login functions.

### Recent job page

`http://127.0.0.1:8000/recent`

The recent page shows the ten most recent BLAST jobs that have been performed by default.

The BLAST jobs can be filtered by a variety of factors. These are the following:
- Name
- Minimal query length
- Maximum query length
- Date

When filtering on the job name, the system searches for jobs that contain the
term in the "Name contains" field. The 2 length filters are used for minimal
an maximal query lengths. The date filters for the exact date.

After filling in the desired filter(s) and clicking the Filter button, all
BLAST jobs that match the filter(s) are displayed. The table columns can be
sorted ascending and descending by clicking the table headers. The table is
sorted on date - time by default. The sorting of the table uses Tablesaw.

### Personalia page

`http://127.0.0.1:8000/personalia`

To go to this page the user needs to be logged in.

#### Account information & change password

On the left side of the page, a box titled "Account information?"
is displayed. This box shows the username and email of the user's account.
Below, three input fields are shown to change your password. The first field
demands your current password that needs to be changed. The remaining two
fields are for the new password. These two passwords have to match.

The password change then uses the standard Django password change.
The password can now also change back to same password as the old password.

#### User stats

On the top right is the frame "User stats".
This frame shows some interesting facts about the user.
In the user stats frame on the left is the amount of jobs you have run.
Right from the jobs done is the amount of days since you have logged in.
In the middle of the frame is the total length of all queries you have run.
Right from the total length is the average hits per job.
This calculates how many hits you have gotten per job, and shows the result
by two decimals.

#### My Blast Buddie Club

The frame "My Blast Buddie Club" shows a list of all the buddies you have.
On the right of each buddie there is the button "👤-" which can be used to
remove the user as a buddie from the user's BlastBuddie table.
On the bottom of the frame is an input field to search for users to add
as a buddie. To search for a user you need to have an exact user name and
then click on the button "🔍︎" to see the user.
If the username was correct you see the username and on the right of it the
button "👤+" to add the user as a buddie. If the username was not correct,
is the user or is already a buddie then there will be a message saying
why the user cannot be added.

### Shared MasterBlast jobs

The bottom frame shows the jobs that have been shared with you by other users.
The jobs are shown with the job title, hit count, date, time and the user
that shared the job with you. The title names take the user to the blast job.
When you are on the BLAST results page from a job shared with you,
then it is not possible to share that job further with your buddies.
The list of jobs shared with the user can get very long, and has no way to
filter or remove jobs your not interested in anymore.