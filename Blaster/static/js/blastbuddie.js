/**
 * Searches if the user from user_self is a user, is not yourself or
 * already in your blast buddie club. and shows the apropriate message if
 * the user cannot be added as buddie or shows the user with the option 
 * to add it as buddie.
 * @param {string} user_self - the username of the user to be added
 * as buddie
 */
function search_user(user_self) {

    let name = document.getElementById("search_name").value;

    let currentBuddies = document.getElementsByName("buddie_username");
    currentBuddies = Array.from(currentBuddies).map(input => input.innerHTML);

    document.getElementById("user_list").innerHTML = ""
    $.ajax({
        url: '/search_user/',
        type: 'GET',
        data: {name: name},
        success: function(response) {
                if (response.users.length === 0) {
                    $('#user_list').append('<tr><td>Could not find user.</td></tr>');
                }
            response.users.forEach(function(user) {
                if (user.username !== user_self) {
                    if (currentBuddies.includes(user.username)) {
                        $('#user_list').append('<tr><td>This user is already in your blast buddie club.</td></tr>');
                    } else {
                        $('#user_list').append('<tr><td>' + user.username + 
                        '</td><td><button type="submit" id="searched_buddie" onclick="addBuddie(' + "'" + user.username + "'" + ')" class="rem_buddie">&#128100;<span style="font-size: 25px;">+</span></button></td></tr>');
                    }
                } else {
                    $('#user_list').append('<tr><td>Cannot be a blast buddie with yourself.</td></tr>');
                };
            });
        },
        error: function(xhr, errmsg, err) {
            console.log(errmsg);
        }
    });
  }

/**
 * function to call the url to call the view function to add a buddie
 * to the list
 *
 * @param {string} buddie_username - the username of the user to be added
 *  as buddie
 */
function addBuddie(buddie_username) {
    console.log(buddie_username)
    let url = `/add_buddie/${buddie_username}`;
    window.location.href = url;
}
