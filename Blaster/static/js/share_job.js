/**
 * Contains the handlers for the "Share job" button's functionalities.
 */

let kader = document.getElementById("share_kader");
let share_button = document.getElementById("share-btn");
let span = document.getElementById("share-close");

/**
 * Changes the css of the share pupop to block so it is visable
 */
function share_job_show() {
    kader.style.display = "block";
}

/**
 * Changes the css of the share pupop to none so it is not visable
 */
function share_job_close() {
    kader.style.display = "none";
}
