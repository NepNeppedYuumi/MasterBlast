/**
 * Contains the tablesaw handler for the BLAST results, recent
 * and comparison pages.
 * This handler is automically triggered when all HTML elements are loaded.
 */

/**
 * Initializes the Tablesaw.js library's functionalities on loading the page.
 * jQuery is used to trigger tablesaw on the document.
 */
(document).ready(function() {
    $(document).trigger("enhance.tablesaw");
});