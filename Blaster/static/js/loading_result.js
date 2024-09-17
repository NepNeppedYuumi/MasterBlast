/** 
 * This file contains the functions used to manage the loading page 
 * for the blast job.
 * 
 * If the loading page is wanted to be used more globally, rather than only
 * for blast jobs, the functions within this file need to be more generalized.
 * 
 * Globally kept are:
 *  Variables used to keep track of the time elapsed since opening the webpage.
 *  Job_id is the current job, and is retrieved from the hyperlink.
*/

let total_time = 0;
let retrying_in = 10;
const job_id = window.location.href.split("/").at(-1);


/**
 * updateTimer is meant to be called on a timer of a 1 second interval.
 * 
 * Every second it will update the timers on the page:
 * a. The total time elapsed since opening the page
 * b. The time left until it will ask the server for the job status.
 * 
 * If the time left for retrying reaches zero, it will call `requestStatus`
 * to request the status of the current job.
*/
function updateTimer(){
    document.getElementById("total-time").innerText = total_time;
    document.getElementById("time-left").innerText = retrying_in;

    if (retrying_in <= 0){
        requestStatus();
        retrying_in = 10;
    }

    total_time += 1;
    retrying_in -= 1;
}


/** 
 * requestStatus sends an ajax request to the server to retrieve the status
 * of the current job.
 * 
 * The current job is defined as the job_id.
 * The job_id will be used to ask the server if that job has been processed yet.
 * 
 * If the job has been processed the webpage will redirect itself to the blast_result
 * of the current job.
*/
function requestStatus(){
    $.ajax({
        url: `get_processed_status/${job_id}`,
        type: 'GET',
        success: function(response){
            if (response["status"] === true){
                window.location.pathname = `blast_result/${job_id}`;
            }
        },
    });
}

updateTimer();
setInterval(updateTimer, 1000);