"use strict";

function update_ratings(){
    $.ajax({
        url: "/get_ratings",
        method:"GET",
        success: function(data) {
            if (data != "False"){
                console.log(data);
                var vals = JSON.parse(data);
                console.log(vals);
                $("#table tbody > tr").remove();
                for (var key in vals){
                    $('#table tbody').append('<tr><td>' + key + '</td><td>' + 
                        vals[key][0] + '</td><td>' + vals[key][1] + 
                        '</td><td>' + vals[key][2] + '</td></tr>');
                }
                get_recommendations();
            } 
        }
    });
    
}

function get_recommendations(){
    $.ajax({
        url: "/get_recoms",
        method:"GET",
        success: function(data) {
            if (data != "False"){
                var vals = JSON.parse(data);
                console.log(vals);
                $("#table2 tbody > tr").remove();
                for (var key in vals){
                    $('#table2 tbody').append('<tr><td>' + 
                        vals[key][0] + '</td><td>' + vals[key][2] + '</td><td>' + vals[key][1] + '</td></tr>');
                }
            } 
        }
    });
}

function login(username) {
    $("#login").toggle();
    $("#main").toggle();
    $("#nav").toggle();
    $("#username_main").val(username);
    update_ratings();
    get_recommendations();

}

function logout(){
    $.ajax({
        url: "/logout",
        method:"POST",
        success: function(data) {
            if (data != "False"){
                logout_change();
            }
        }
        })
}

function logout_change(){
    $("#login").toggle();
    $("#main").toggle();
    $("#nav").toggle();
}


function update_label(value){
    if (value == "False"){
            $("#outLabel").html("The book was not found.");
    } else {
            $("#outLabel").html("That song has ID: " + value);
    }
}

function get_counties(){
    $.ajax({
        url: "/get_countries",
        method:"GET",
        success: function(data) {
            if (data != "False"){
                console.log(data);
                var vals = JSON.parse(data);
                console.log(vals);
                for (var key in vals){
                    var option = new Option(vals[key][1], vals[key][0]);
                    $(option).html(vals[key][1]);
                    $("#country_select").append(option);
                }
            } 
        }
    });
}


$( document ).ready(function(event){
    get_counties();

    $("#button").click( function() {
        logout();
    });
    $("#nation").click( function() {
        toggle_nation();
    });

    

    $("#button-logout").click( function() {
        $.ajax({
            url: "/logout",
            method:"post",
            success: function(data){
                location.reload()
            }
        });
    });

    $("#form_login").submit( function(event){
        event.preventDefault();
        var signup_val = 0;
        if ($('#signup').is(":checked")){
            signup_val = 1;
        };
        console.log(signup_val);
        $.ajax({
            url: "/login",
            data: {
                username: $("#username").val(),
                password: $("#password").val(),
                signup: signup_val
            },
            method:"get",
            success: function(data) {
                if (data != "False"){
                    login($("#username").val());
                } else {
                    window.alert("Incorrect username or password, please try again.")
                }
            }
          });
    });

    $("#form_country").submit(function (event){
        event.preventDefault();
        var val = $("#country_select").val();
        $.ajax({
            url: "/change_context",
            data:{
                country: val
            },
            method:"post",
            success: function(data) {
                get_recommendations();
            }

        })
    })

    $("#form_user").submit( function(event){
        event.preventDefault();
        var name = $("#username_main").val()
        $.ajax({
            url: "/update_details",
            data: {
                username: $("#username_main").val()
            },
            method:"post",
            success: function(data) {
                if (data != "False"){   
                    $("#username_main").val(name);
                }
            }
          });
    });

    $("#form-search").submit( function(event){
        event.preventDefault();
        $.ajax({
            url: "/search_tracks",
            data: {
                trackname: $("#searchname").val()
            },
            method:"get",
            success: function(data) {
                update_label(data);
            }
          });
    });

    $("#form_rating").submit( function(event){
        event.preventDefault();
        console.log($("#bookid").val());
        console.log($("#rating").val());
        $.ajax({
            url: "/make_rating",
            data: {
                bookid: $("#bookid").val(),
                rating: $("#rating").val()
            },
            method:"post",
            success: function(data) {
                update_ratings();
            }
          });
    });

    $("#form_book").submit( function(event){
        event.preventDefault();
        console.log($("#name").val());
        console.log($("#genre").val());
        $.ajax({
            url: "/add_book",
            data: {
                bookname: $("#name").val(),
                genre: $("#genre").val()
            },
            method:"post",
            success: function(data) {
                window.alert("Book has been added. ID:"+data)
            }
          });
    });
})