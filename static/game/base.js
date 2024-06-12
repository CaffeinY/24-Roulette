 
// //add shadow effect to card element when hover
// $(document).ready(function() {
//     $( ".card" ).hover(
//         function() {
//             $(this).addClass('shadow-lg').css('cursor', 'pointer'); 
//         }, 
//         function() {
//             $(this).removeClass('shadow-lg');
//         }
//     ); 
// });


// //copy room information to clipboard
// function copy(){
//     var id = document.getElementById("roomID").innerHTML;
//     var pw = document.getElementById("password").innerHTML;
//     var message = "RoomID: " + id + ", Password: " + pw;
//     navigator.clipboard.writeText(message);
// }


// // require data from models every 1 second.
// function getData() {
//     var dataNow = new Date();
//     var databefore = new Date(dataNow.getTime() - 5000);
//     var isotime = databefore.toISOString();
//     $.ajax({
//         url: "/game/refresh-page",
//         data: "last_refresh="+isotime,
//         dataType : "json",
//         success: updateComments
//     });
// }



// //update comments board.
// function updateComments(response) {
//     console.log("get data")
//     var roomID = $("#roomID").val();
//     var userID =
//     console.log("At roomID = " + roomID )
//     length = response.length;

//     var roomPk = 0;   //index of the data we want in the response.
//     if (roomID != null) {
//         for (i = 0; i < response.length; i++) {
//             if (response[i].model == "game.room") {
//                 if (response[i].pk == roomID) {
//                     var numberOfPlayers = response[i].fields.numOfPlayer;
//                     roomPk = i;
//                 }
//             }
//         }
//     }


//     //update the comment and game-log in the main game page and data is from the response.
//     if ($("#comment-board").val() != null) {
//         console.log(response[roomPk].fields.comment_board);
//         $("#comment-board").text(response[roomPk].fields.comment_board);
//         $("#game-log").text(response[roomPk].fields.game_log);
//         console.log($("#comment-board").val());
//         console.log($("#game_log").val());
//     }


//     if (roomID != null) {
//         if (response[roomPk].fields.game_log == "wolf starts kill.") {
//             setTimeout(function() { wolf_kill(response); }, 2000);
//             updateStatus(response);
//         }

//         //let the wolf choose the same victim.
//         if (response[roomPk].fields.game_log == "wolf choose again.") {
//             setTimeout(function() { wolf_kill_again(response); }, 2000);
//             updateStatus(response);

//         }

//         if (response[roomPk].fields.game_log == "wolves finished killing.") {
//             setTimeout(function() { doctor(response); }, 2000);
//             updateStatus(response);
//         }

//         if (response[roomPk].fields.game_log == "seer has checked one role's id.") {
//             setTimeout(function() { day_conclude_wolf(response); }, 2000);
//             updateStatus(response);

//         }

//         //when the game log becomes seers starts to work, execute function seer();
//         if (response[roomPk].fields.game_log == "seer starts to work.") {
//             setTimeout(function() { seer(response); }, 2000);
//             updateStatus(response);
//         }

//        if (response[roomPk].fields.game_log == "Day conclude wolf killing part finished.") {
//            day_speak(response);
//            display_audio(response);
//            updateStatus(response)
//        }

//        if (response[roomPk].fields.game_log == "Finish speaking.") {
//            setTimeout(function() { vote_day(response);}, 2000);
//            updateStatus(response);
//        }

//        if (response[roomPk].fields.game_log == "vote finish.") {
//            setTimeout(function() { end_game(response); }, 2000);
//            updateStatus(response);

//        }
//        if (response[roomPk].fields.game_log == "not end") {
//             setTimeout(function() { start_game(response); }, 2000);
//             updateStatus(response);
//        }
//     }
// }


// window.onload = getData;
// window.setInterval(getData, 1000);


// function updateStatus(response) {
//     var roomID = $("#roomID").val();
//     var player_id = []
//     var player_status = []
//     for (var i = 0; i < response.length; i++) {
//         if (response[i].fields.currentRoom == roomID) {
//             player_id.push(response[i].pk)
//             player_status.push(response[i].fields.status_txt)
//         }
//     }
//     console.log(player_status)
//     console.log(player_id)
//     var userID = $("#currentUserId").val();
//     for (var i = 0; i < player_id.length; i++) {
//         $("#status_" + player_id[i]+ "_" + roomID).text("Status: " + player_status[i]);
//     }
// }


// var map = new Map();
// function getPlayers(roomID) {
//     var readyNum;
//     map.set(roomID, []);
//     $.ajax({
//         url: "/game/get-players/" + roomID,
//         dataType : "json",
//         async: false,
//         success: function(response) {
//             readyNum = response.length;
//             for(i = 0; i < response.length; i++) {
//                 var userID = response[i].fields.user;
//                 var username = getUsername(userID);
//                 map.get(roomID).push(username);
//             }
//         }
//     });
//     $("#ready-num_"+roomID).text(readyNum);
//     //compute missing number of players
//     var total = $("#totalplayers_"+roomID).text();
//     var missing = parseInt(total) - parseInt(readyNum);
//     $("#missing_"+roomID).text(missing);
//     //update room members information
//     $("#members_"+roomID).empty();
//     for(i = 0; i < map.get(roomID).length; i++) {
//         $("#members_"+roomID).append("<span class='room_members'>"+map.get(roomID)[i]+"</span><br>");
//     }
//     if (missing > 0) {
//         $("#joinButton_" + roomID).show();
//         $("#startButton_" + roomID).hide();
//     }
//     if (missing == 0) {
//         $("#joinButton_" + roomID).hide();
//         $("#startButton_" + roomID).show();
//     }
// }


// function check_card(roomID, userID) {
//     $.ajax({
//     url:"/game/check_card/" + roomID,
//     dataType:"text",
//     async:false,
//     success: function(response) {
//         role = response;
//         }
//     });
//     $("#current_role").text(role);
//     $("#check_card_" + roomID + "_" + userID).hide();
//     console.log("check hide")
//     $("#check_card_" + roomID + "_" + userID).attr("disabled", true);
//     console.log("check disabled")
//     $("#check_txt_" + roomID + "_" + userID).hide();
//     console.log("check text hide")
//     $("#current_role").append("<div><input class='ready_button btn btn-dark' type = 'button' onclick='ready(" + roomID + "," + userID +")'"+ "id = 'ready_" + roomID + "_"+ userID + "' value='Ready'></div>");
// }



// function ready(roomID, userID) {
//     var readyNum;
//     $.ajax({
//     url:"/game/ready/" + roomID,
//     dataType:"json",
//     async:false,
//     success: function(response) {
//         }
//     });
//     $("#ready_" + roomID + "_" + userID).hide();
//     $("#ready_" + roomID + "_" + userID).attr("disabled", true);
// }





// function getCSRFToken() {
//     var cookies = document.cookie.split(";");
//     for (var i = 0; i < cookies.length; i++) {
//         c = cookies[i].trim();
//         if (c.startsWith("csrftoken=")) {
//             return c.substring("csrftoken=".length, c.length);
//         }
//     }
//     return "unknown";
// }



// function start_game(response) {
//     var roomID = $("#roomID").val();
//     var userID = $("#currentUserId").val();
//     $("#check_card_" + roomID + "_" + userID).hide();
//     console.log("check hide")
//     $("#check_card_" + roomID + "_" + userID).attr("disabled", true);
//     console.log("check disabled")
//     $("#check_txt_" + roomID + "_" + userID).hide();
//     console.log("check text hide")
//     $.ajax({
//         url: "/game/start_game_again/" + roomID,
//         dataType: "text",
//         async: false,
//         success: function(response) {
//             console.log(response)
//         }
//     });
// }


// function end_game(response) {
//     var roomID = $("#roomID").val();
//     var userID = $("#currentUserId").val();
//     for (var i = 0; i < response.length; i++) {
//         if (response[i].fields.currentRoom == roomID) {
//             if (response[i].fields.user == userID) {
//                 $("#status_" + userID + "_" + roomID).text(response[i].fields.status_txt);
//             }
//         }
//     }
//     $.ajax({
//     url: "/game/end_game/" + roomID,
//     dataType: "text",
//     async: false,
//     success: function(response) {

//     }
//     });


// }


// function getUsername(userID) {
//     var un;
//     $.ajax({
//         url: "/game/get-username/" + userID,
//         dataType : "text",
//         async: false,
//         success: function(response) {
//             un = response;
//         }
//     });
//     return un;
// }


// function getUserNumber(roomID) {
//     var num;
//     $.ajax({
//         url: "/game/get-Usernumber/" + roomID,
//         dataType: "text",
//         async: false,
//         success: function(response) {
//             num = response;
//         }
//     });
//     return num;
// }


// function getRole(userID) {
//     var role;
//     $.ajax({
//         url: "/game/get-role/" + userID,
//         dataType: "text",
//         async: false,
//         success: function(response) {
//             role = response;
//         }
//     });
//     return role;
// }


// function searchRoom() {
//     $(".errors").text('');
//     id = $("#room-id").val();
//     pw = $("#room-pw").val();
//     //search by room id and password
//     var roomID;
//     if(id != '' && pw != '') {
//         $.ajax({
//             url: "/game/search-by-id/" + id + "/" + pw,
//             dataType : "json",
//             async: false,
//             success: function(response) {
//                 if(response.length == 0) {
//                     $(".errors").text('No room found with room id = ' + id + ' , password = ' + pw);
//                 }
//                 else {
//                     roomID = response[0].pk;
//                     $(".all-rooms").each(function() {
//                         room_id = $(this).attr("id").substring(5);
//                         if(room_id != id){
//                             $(this).remove();
//                         }
//                     });
//                 }
//             }
//         });
//         $("#room-id").val('');
//         $("#room-pw").val('');
//     }
//     else {
//         diff = $("#room-difficulty").val();
//         num = $("#room-players").val();
//         $.ajax({
//             url: "/game/search-by-mode/" + diff + "/" + num,
//             dataType : "text",
//             async: false,
//             success: function(response) {
//                 if(response.length == '') {
//                     $(".errors").text('No room found with difficulty = ' + diff + ' , number of players = ' + num);
//                 }
//                 else {
//                     idList = response.split(",");
//                     $(".all-rooms").each(function() {
//                         room_id = $(this).attr("id").substring(5);
//                         if(!idList.includes(room_id)){
//                             $(this).remove();
//                         }
//                     });  
//                 }
//             }
//         });
//         $("#room-difficulty").val('All');
//         $("#room-players").val('All');
//     }
// }


// function refreshLobby() {
//     $.ajax({
//         url: "/game/refresh-lobby",
//         dataType : "json",
//         success: updateLobby
//     });
// }

// function updateLobby(updates) {
//     $(updates).each(function() {
//         if(this.model == "game.room"){
//             id = "room_" + this.pk;
//             if(document.getElementById(id) == null) {
//                 $("#rooms-all").prepend(
//                     '<div id="room_'+this.pk+'" class="all-rooms col-4"> <div class="card"> <div class="card-container">' +
//                     '<img id="'+this.pk+'" src="'+this.fields.pictureURL+'" class="card-img-top card-image" onload="getPlayers('+this.pk+')">' +
//                     '<div class="card-body">' + 
//                     '<h5 class="card-title">'+this.fields.difficulty+' &nbsp;| &nbsp; <span id="totalplayers_'+this.pk+'">'+this.fields.numOfPlayers+'</span> Players</h5>' +
//                     '<p class="card-text"><span id="ready-num_'+this.pk+'"></span> players ready. Waiting for <span id="missing_'+this.pk+'" class="missing-player"><b>'+this.fields.numOfPlayers+'</b></span> more players.</p>' +
//                     '</div><div class="overlay"><div class="overlay-text">Room members</div><br>' +
//                     '<div id="members_'+this.pk+'" class="members"></div>' +
//                     '<form method="POST" action="/game/join-room/'+this.pk+'">' +
//                     '<button class="btn btn-outline-warning overlay-button" id="joinButton_'+this.pk+'">Join</button>' +
//                     '<input type="hidden" name="csrfmiddlewaretoken" value="'+getCSRFToken()+'">' +
//                     '</form><form method="POST" action="/game/start/'+this.pk+'">' +
//                     '<button class="btn btn-outline-warning overlay-button" id = "startButton_'+this.pk+'">Start</button>' +
//                     '<input type="hidden" name="csrfmiddlewaretoken" value="'+getCSRFToken()+'">' +
//                     '</form> <form method="POST" action="/game/exit-room/'+this.pk+'">' +
//                     '<button class="btn btn-outline-warning overlay-button" id="exitButton_'+this.pk+'">Exit</button>' +
//                     '<input type="hidden" name="csrfmiddlewaretoken" value="'+getCSRFToken()+'">'+
//                     '</form></div></div></div></div>'
//                 );
//             }
//             else {
//                 imageElement = document.getElementById(this.pk);
//                 getPlayers(this.pk);
//                 imageElement.innerHTML = '<img id="'+this.pk+'" src="'+this.fields.pictureURL+'" class="card-img-top card-image" onload="getPlayers('+this.pk+')">';
//             }
//             //remove the room if it is empty
//             var readyNum = getReadyPlayer(this.pk);
//             if(readyNum == 0) {
//                 console.log("*******");
//                 $("#"+id).remove();
//                 $.ajax({
//                     url: "/game/remove_empty_room",
//                     type: "POST",
//                     data: "roomID="+this.pk+"&csrfmiddlewaretoken="+getCSRFToken(),
//                     dataType: "text",
//                     success: function(response) {
//                         console.log(response);
//                     }
//                 });
//             }
//         }
//     })
// }

// function getReadyPlayer(roomID) {
//     var readyNum;
//     $.ajax({
//         url: "/game/get-players/" + roomID,
//         dataType : "json",
//         async: false,
//         success: function(response) {
//             readyNum = response.length;
//         }
//     });
//     return readyNum;
// }
